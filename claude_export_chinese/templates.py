CONVERSATION_TEMPLATE_START = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{
            background-color: #ffffff;
            color: #111111;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .container {{
            width: 100%;
            max-width: 700px;
        }}
        h1 {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 40px;
            color: #000000;
            letter-spacing: -0.5px;
        }}
        .message-box {{
            margin-bottom: 32px;
            padding: 12px 0;
        }}
        .sender {{
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            color: #666666;
        }}
        .content {{
            font-size: 15px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
        }}
        .human .sender {{ color: #2563eb; }}
        .assistant .sender {{ color: #0f172a; }}
        hr {{
            border: 0;
            border-top: 1px solid #f1f5f9;
            margin: 40px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
"""

CONVERSATION_TEMPLATE_END = """
    </div>
</body>
</html>
"""

INDEX_TEMPLATE_START = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Claude 历史对话存档</title>
    <style>
        body {{
            background-color: #ffffff;
            color: #111111;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: 60px 20px;
            display: flex;
            justify-content: center;
        }}
        .container {{ width: 100%; max-width: 600px; }}
        h1 {{ font-size: 28px; font-weight: 600; margin-bottom: 8px; letter-spacing: -0.5px; }}
        .subtitle {{ color: #666666; font-size: 14px; margin-bottom: 48px; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ margin-bottom: 16px; }}
        a {{
            color: #111111;
            text-decoration: none;
            font-size: 16px;
            display: block;
            padding: 10px 0;
            border-bottom: 1px solid #f1f5f9;
            transition: all 0.2s ease;
        }}
        a:hover {{ color: #2563eb; border-bottom-color: #2563eb; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>对话存档画廊</h1>
        <div class="subtitle">共导出了 {count} 个历史会话</div>
        <ul>
"""

INDEX_TEMPLATE_END = """        </ul>
    </div>
</body>
</html>
"""
