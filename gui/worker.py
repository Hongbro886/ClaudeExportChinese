from pathlib import Path

from PySide6.QtCore import QThread, Signal


class ExportWorker(QThread):
    """后台执行导出任务，避免阻塞 UI。"""

    progress = Signal(int, int)  # (current, total)
    finished = Signal(Path, int)  # (output_dir, count)
    error = Signal(str)

    def __init__(self, input_path: str, output_dir: str):
        super().__init__()
        self.input_path = input_path
        self.output_dir = output_dir

    def run(self):
        try:
            from claude_export_chinese.loader import load_conversations
            from claude_export_chinese.renderer import (
                render_conversation,
                get_conversation_timestamp,
                set_file_mtime,
                write_index_page,
            )
            from claude_export_chinese.utils import build_safe_filename, ensure_output_dir

            conversations = load_conversations(self.input_path)
            output_path = ensure_output_dir(self.output_dir)

            generated_files: list[tuple[str, str, float | None]] = []
            total = len(conversations)

            for index, conversation in enumerate(conversations):
                filename = build_safe_filename(conversation.title, index)
                file_path = output_path / filename
                file_path.write_text(render_conversation(conversation), encoding="utf-8")

                timestamp = get_conversation_timestamp(conversation)
                set_file_mtime(file_path, timestamp)
                generated_files.append((conversation.title, filename, timestamp))

                self.progress.emit(index + 1, total)

            write_index_page(generated_files, output_path)
            self.finished.emit(output_path, len(generated_files))

        except Exception as e:
            self.error.emit(str(e))
