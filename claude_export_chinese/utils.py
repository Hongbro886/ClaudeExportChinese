from pathlib import Path


def build_safe_filename(title: str, index: int) -> str:
    """把会话标题转换为可跨平台保存的 Markdown 文件名。"""
    safe_title = "".join(
        char for char in title if char.isalpha() or char.isdigit() or char in " _-"
    ).strip()

    if not safe_title:
        safe_title = f"Conversation_{index + 1}"

    return f"{safe_title}.md"


def ensure_output_dir(output_dir: str | Path) -> Path:
    """确保输出目录存在，并返回 Path 对象方便后续拼接文件路径。"""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path
