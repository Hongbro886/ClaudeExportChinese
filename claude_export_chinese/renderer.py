from pathlib import Path

from .models import ChatMessage, Conversation
from .utils import build_safe_filename


def render_conversation(conversation: Conversation) -> str:
    """渲染单个对话为 Markdown 文档。"""
    body_markdown = "\n\n".join(
        render_message(message) for message in conversation.messages
    )
    title = escape_markdown_heading(conversation.title)

    return f"# {title}\n\n{body_markdown}\n"


def render_message(message: ChatMessage) -> str:
    """渲染单条消息为 Markdown 段落。"""
    sender_is_human = message.sender == "human"
    sender_label = "You" if sender_is_human else "Claude"
    text = message.text.strip()

    return f"## {sender_label}\n\n{text}"


def escape_markdown_heading(text: str) -> str:
    """避免标题开头的 Markdown 标记改变标题层级。"""
    return text.lstrip("# ") or "未命名对话"


def write_conversation_pages(
    conversations: list[Conversation], output_dir: Path
) -> list[tuple[str, str]]:
    """写入所有会话 Markdown，并返回索引需要的标题和文件名。"""
    generated_files: list[tuple[str, str]] = []

    for index, conversation in enumerate(conversations):
        filename = build_safe_filename(conversation.title, index)
        output_path = output_dir / filename
        output_path.write_text(render_conversation(conversation), encoding="utf-8")
        generated_files.append((conversation.title, filename))

    return generated_files


def write_index_page(generated_files: list[tuple[str, str]], output_dir: Path) -> None:
    """生成所有会话 Markdown 的入口目录。"""
    items_markdown = "".join(
        f"- [{escape_markdown_link_text(title)}](<{filename}>)\n"
        for title, filename in generated_files
    )
    index_markdown = f"# Claude 中文对话导出\n\n共导出了 {len(generated_files)} 个历史会话。\n\n{items_markdown}"

    (output_dir / "index.md").write_text(index_markdown, encoding="utf-8")


def escape_markdown_link_text(text: str) -> str:
    """转义 Markdown 链接文本中的方括号。"""
    return text.replace("[", "\\[").replace("]", "\\]")
