from pathlib import Path

from .loader import load_conversations
from .renderer import write_conversation_pages, write_index_page
from .utils import ensure_output_dir


def export_conversations(input_path: str | Path, output_dir: str | Path) -> tuple[Path, int]:
    """完整导出流程：读取 JSON、生成会话页、生成索引页。"""
    conversations = load_conversations(input_path)
    output_path = ensure_output_dir(output_dir)

    generated_files = write_conversation_pages(conversations, output_path)
    write_index_page(generated_files, output_path)

    return output_path, len(generated_files)
