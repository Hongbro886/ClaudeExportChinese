import html
from pathlib import Path

from .models import ChatMessage, Conversation
from .templates import (
    CONVERSATION_TEMPLATE_END,
    CONVERSATION_TEMPLATE_START,
    INDEX_TEMPLATE_END,
    INDEX_TEMPLATE_START,
)
from .utils import build_safe_filename


def render_conversation(conversation: Conversation) -> str:
    """渲染单个对话页面。"""
    body_html = "".join(render_message(message) for message in conversation.messages)
    title = html.escape(conversation.title)

    return (
        CONVERSATION_TEMPLATE_START.format(title=title)
        + body_html
        + CONVERSATION_TEMPLATE_END
    )


def render_message(message: ChatMessage) -> str:
    """渲染单条消息，并转义正文避免 HTML 注入和排版破坏。"""
    sender_is_human = message.sender == "human"
    sender_label = "YOU" if sender_is_human else "CLAUDE"
    css_class = "human" if sender_is_human else "assistant"
    escaped_text = html.escape(message.text)

    return f"""
        <div class="message-box {css_class}">
            <div class="sender">{sender_label}</div>
            <div class="content">{escaped_text}</div>
        </div>
"""


def write_conversation_pages(
    conversations: list[Conversation], output_dir: Path
) -> list[tuple[str, str]]:
    """写入所有会话页面，并返回索引页需要的标题和文件名。"""
    generated_files: list[tuple[str, str]] = []

    for index, conversation in enumerate(conversations):
        filename = build_safe_filename(conversation.title, index)
        output_path = output_dir / filename
        output_path.write_text(render_conversation(conversation), encoding="utf-8")
        generated_files.append((conversation.title, filename))

    return generated_files


def write_index_page(generated_files: list[tuple[str, str]], output_dir: Path) -> None:
    """生成所有会话页面的入口目录。"""
    items_html = "".join(
        f'            <li><a href="{html.escape(filename)}" target="_blank">{html.escape(title)}</a></li>\n'
        for title, filename in generated_files
    )
    index_html = (
        INDEX_TEMPLATE_START.format(count=len(generated_files))
        + items_html
        + INDEX_TEMPLATE_END
    )

    (output_dir / "index.html").write_text(index_html, encoding="utf-8")
