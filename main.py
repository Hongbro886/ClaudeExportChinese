import sys


def main() -> None:
    """入口：默认启动 GUI，传入 --cli 则使用命令行模式。"""
    if "--cli" in sys.argv:
        from claude_export_chinese.exporter import export_conversations

        output_dir, count = export_conversations(
            input_path="conversations.json",
            output_dir="Claude_Visual_History",
        )
        print(f"解析完成！共导出 {count} 个会话，Markdown 已存入文件夹: {output_dir}")
        print(f"请打开 {output_dir}/index.md 浏览全部中文对话。")
    else:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtGui import QFont, QFontDatabase
        from qfluentwidgets import setTheme, Theme
        from gui import MainWindow

        app = QApplication(sys.argv)

        font = QFont()
        available_families = QFontDatabase.families()
        if sys.platform == "darwin":
            for family in ["PingFang SC", "Heiti SC", "STHeiti"]:
                if family in available_families:
                    font.setFamily(family)
                    break
        elif sys.platform == "win32":
            for family in ["Microsoft YaHei", "SimHei", "SimSun"]:
                if family in available_families:
                    font.setFamily(family)
                    break
        else:
            for family in ["Noto Sans CJK SC", "WenQuanYi Micro Hei", "Droid Sans Fallback"]:
                if family in available_families:
                    font.setFamily(family)
                    break
        app.setFont(font)

        setTheme(Theme.LIGHT)

        window = MainWindow()
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
