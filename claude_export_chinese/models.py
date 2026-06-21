from dataclasses import dataclass


@dataclass(frozen=True)
class ChatMessage:
    """渲染层需要的单条聊天消息。"""

    sender: str
    text: str
    created_at: str


@dataclass(frozen=True)
class Conversation:
    """渲染层使用的对话结构，隔离 Claude 原始导出字段。"""

    title: str
    messages: list[ChatMessage]
