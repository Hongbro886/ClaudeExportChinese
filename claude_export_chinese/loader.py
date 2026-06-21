import json
from pathlib import Path
from typing import Any

from .models import ChatMessage, Conversation


def load_conversations(input_path: str | Path) -> list[Conversation]:
    """读取 Claude 导出的 conversations.json，并转换为内部模型。"""
    path = Path(input_path)

    try:
        with path.open("r", encoding="utf-8") as file:
            raw_conversations = json.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"未找到输入文件: {path}") from exc

    return [parse_conversation(raw, index) for index, raw in enumerate(raw_conversations)]


def parse_conversation(raw: dict[str, Any], index: int) -> Conversation:
    """从单个 Claude 原始会话对象中提取标题和消息列表。"""
    raw_title = str(raw.get("name", "")).strip()
    title = raw_title if raw_title else f"未命名对话_{index + 1}"

    messages = [parse_message(message) for message in raw.get("chat_messages", [])]
    messages.sort(key=lambda message: message.created_at)

    return Conversation(
        title=title,
        created_at=str(raw.get("created_at", "")),
        updated_at=str(raw.get("updated_at", "")),
        messages=messages,
    )


def parse_message(raw: dict[str, Any]) -> ChatMessage:
    """只保留生成 Markdown 时真正需要的消息字段。"""
    return ChatMessage(
        sender=str(raw.get("sender", "human")),
        text=str(raw.get("text", "")),
        created_at=str(raw.get("created_at", "")),
    )
