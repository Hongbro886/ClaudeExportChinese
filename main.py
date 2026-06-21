from claude_export_chinese.exporter import export_conversations


def main() -> None:
    """命令行入口：从默认 JSON 文件导出 Markdown 对话存档。"""
    output_dir, count = export_conversations(
        input_path="conversations.json",
        output_dir="Claude_Visual_History",
    )

    print(f"解析完成！共导出 {count} 个会话，Markdown 已存入文件夹: {output_dir}")
    print(f"请打开 {output_dir}/index.md 浏览全部中文对话。")


if __name__ == "__main__":
    main()
