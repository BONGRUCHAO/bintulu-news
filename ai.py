response = model.generate_content(
    f"""
请用简体中文总结以下新闻标题。

要求：
1. 不超过30字
2. 保持客观
3. 只输出摘要内容

标题：
{title}
"""
)
