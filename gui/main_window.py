import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from qfluentwidgets import (
    FluentIcon,
    FluentWindow,
    PrimaryPushButton,
    PushButton,
    ProgressBar,
    TitleLabel,
    SubtitleLabel,
    InfoBar,
    InfoBarPosition,
)

from .worker import ExportWorker


def get_default_download_dir() -> Path:
    """跨平台获取默认下载文件夹。"""
    if sys.platform == "win32":
        return Path.home() / "Downloads"
    elif sys.platform == "darwin":
        return Path.home() / "Downloads"
    else:
        xdg_download = os.environ.get("XDG_DOWNLOAD_DIR")
        if xdg_download:
            return Path(xdg_download)
        return Path.home() / "Downloads"


def open_folder(path: Path) -> None:
    """跨平台打开文件夹。"""
    path_str = str(path)
    if sys.platform == "win32":
        os.startfile(path_str)
    elif sys.platform == "darwin":
        subprocess.run(["open", path_str], check=False)
    else:
        subprocess.run(["xdg-open", path_str], check=False)


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Claude 中文对话导出工具")
        self.resize(500, 350)

        self.input_path: str | None = None
        self.output_dir: Path = get_default_download_dir() / "Claude_Visual_History"
        self._output_dir: Path | None = None
        self._worker: ExportWorker | None = None

        self._init_ui()

    def _init_ui(self):
        interface = QWidget()
        interface.setObjectName("main_interface")
        layout = QVBoxLayout(interface)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = TitleLabel("Claude 中文对话导出")
        layout.addWidget(title)

        subtitle = SubtitleLabel("将 Claude 导出的 conversations.json 转换为 Markdown")
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        self.import_btn = PrimaryPushButton("选择 JSON 文件")
        self.import_btn.setIcon(FluentIcon.FOLDER)
        self.import_btn.clicked.connect(self._select_file)
        layout.addWidget(self.import_btn)

        self.file_label = SubtitleLabel("未选择文件")
        self.file_label.setStyleSheet("color: gray;")
        layout.addWidget(self.file_label)

        layout.addSpacing(4)

        self.export_btn = PushButton("开始导出")
        self.export_btn.setIcon(FluentIcon.SEND)
        self.export_btn.setEnabled(False)
        self.export_btn.clicked.connect(self._start_export)
        layout.addWidget(self.export_btn)

        self.progress_bar = ProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.progress_label = SubtitleLabel("")
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        layout.addSpacing(4)

        self.open_btn = PushButton("打开导出文件夹")
        self.open_btn.setIcon(FluentIcon.FOLDER)
        self.open_btn.setEnabled(False)
        self.open_btn.clicked.connect(self._open_output_folder)
        layout.addWidget(self.open_btn)

        layout.addStretch()

        self.addSubInterface(interface, FluentIcon.HOME, "主页")

    def _select_file(self):
        """选择 JSON 文件，限制只能选 .json。"""
        default_dir = str(get_default_download_dir())
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择 conversations.json",
            default_dir,
            "JSON 文件 (*.json);;所有文件 (*)",
        )

        if not file_path:
            return

        path = Path(file_path)

        if not path.exists():
            self._show_error("文件不存在")
            return

        if path.suffix.lower() != ".json":
            self._show_error("请选择 .json 格式的文件")
            return

        try:
            import json
            with open(path, "r", encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError:
            self._show_error("JSON 格式无效，请检查文件内容")
            return
        except Exception as e:
            self._show_error(f"读取文件失败: {e}")
            return

        self.input_path = file_path
        self.file_label.setText(f"已选择: {path.name}")
        self.file_label.setStyleSheet("color: black;")
        self.export_btn.setEnabled(True)

    def _start_export(self):
        """开始导出。"""
        if not self.input_path:
            return

        self.export_btn.setEnabled(False)
        self.import_btn.setEnabled(False)
        self.open_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.progress_label.setText("正在解析...")
        self.progress_label.setVisible(True)

        self._worker = ExportWorker(self.input_path, str(self.output_dir))
        self._worker.progress.connect(self._on_progress)
        self._worker.finished.connect(self._on_finished)
        self._worker.error.connect(self._on_error)
        self._worker.start()

    def _on_progress(self, current: int, total: int):
        """更新进度。"""
        percent = int(current / total * 100) if total > 0 else 0
        self.progress_bar.setValue(percent)
        self.progress_label.setText(f"正在导出: {current}/{total} ({percent}%)")

    def _on_finished(self, output_dir: Path, count: int):
        """导出完成。"""
        self.progress_bar.setValue(100)
        self.progress_label.setText(f"完成！共导出 {count} 个会话")
        self.export_btn.setEnabled(True)
        self.import_btn.setEnabled(True)
        self.open_btn.setEnabled(True)
        self._output_dir = output_dir

        InfoBar.success(
            title="导出成功",
            content=f"已导出 {count} 个会话",
            parent=self,
            position=InfoBarPosition.TOP,
            duration=5000,
        )

    def _on_error(self, message: str):
        """导出出错。"""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.export_btn.setEnabled(True)
        self.import_btn.setEnabled(True)
        self._show_error(message)

    def _open_output_folder(self):
        """打开导出文件夹。"""
        if self._output_dir and self._output_dir.exists():
            open_folder(self._output_dir)

    def _show_error(self, message: str):
        """显示错误信息。"""
        InfoBar.error(
            title="错误",
            content=message,
            parent=self,
            position=InfoBarPosition.TOP,
            duration=3000,
        )
