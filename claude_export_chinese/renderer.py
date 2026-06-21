import os
from datetime import datetime
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
    text = preserve_soft_line_breaks(message.text.strip())

    return f"## {sender_label}\n\n{text}"


def preserve_soft_line_breaks(text: str) -> str:
    """把普通换行转成 Markdown 硬换行，避免数字列表挤成一行。"""
    return "\n".join(line + "  " if line else line for line in text.splitlines())


def escape_markdown_heading(text: str) -> str:
    """避免标题开头的 Markdown 标记改变标题层级。"""
    return text.lstrip("# ") or "未命名对话"


def write_conversation_pages(
    conversations: list[Conversation], output_dir: Path
) -> list[tuple[str, str, float | None]]:
    """写入所有会话 Markdown，并返回索引需要的标题和文件名。"""
    generated_files: list[tuple[str, str, float | None]] = []

    for index, conversation in enumerate(conversations):
        filename = build_safe_filename(conversation.title, index)
        output_path = output_dir / filename
        output_path.write_text(render_conversation(conversation), encoding="utf-8")
        timestamp = get_conversation_timestamp(conversation)
        set_file_mtime(output_path, timestamp)
        generated_files.append((conversation.title, filename, timestamp))

    return generated_files


def write_index_page(
    generated_files: list[tuple[str, str, float | None]], output_dir: Path
) -> None:
    """生成所有会话 Markdown 的入口目录。"""
    items_markdown = "".join(
        f"- [{escape_markdown_link_text(title)}](<{filename}>)\n"
        for title, filename, _timestamp in generated_files
    )
    index_markdown = f"# Claude 中文对话导出\n\n共导出了 {len(generated_files)} 个历史会话。\n\n{items_markdown}"
    index_path = output_dir / "index.md"

    index_path.write_text(index_markdown, encoding="utf-8")
    timestamps = [timestamp for *_unused, timestamp in generated_files if timestamp]
    if timestamps:
        set_file_mtime(index_path, max(timestamps))


def escape_markdown_link_text(text: str) -> str:
    """转义 Markdown 链接文本中的方括号。"""
    return text.replace("[", "\\[").replace("]", "\\]")


def get_conversation_timestamp(conversation: Conversation) -> float | None:
    """返回会话更新时间；没有时回退到最后一条消息时间。"""
    timestamp = parse_iso_timestamp(conversation.updated_at)
    if timestamp is not None:
        return timestamp

    if conversation.messages:
        return parse_iso_timestamp(conversation.messages[-1].created_at)

    return parse_iso_timestamp(conversation.created_at)


def parse_iso_timestamp(value: str) -> float | None:
    """解析 Claude 导出的 ISO 时间字符串为 Unix timestamp。"""
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def set_file_mtime(path: Path, timestamp: float | None) -> None:
    """用聊天时间设置导出文件的访问和修改时间。"""
    if timestamp is not None:
        os.utime(path, (timestamp, timestamp))
