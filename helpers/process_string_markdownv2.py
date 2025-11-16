def escape_markdown_v2(text: str) -> str:
    """
    Экранирует ВСЕ специальные символы для MarkdownV2
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])