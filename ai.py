import os
import google.generativeai as genai
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze(title):
    try:
        prompt = f"""
你是新闻分析系统。

请严格输出以下格式（必须严格两行）：

Category: 经济/天气/事故/政治/交通/发展/其他
Summary: 一句话中文，不超过30字

不要任何解释，不要换格式。

新闻标题：
{title}
"""

        response = model.generate_content(prompt)

        text = response.text.strip()

        print("AI RAW:", text)

        # ⭐ 核心修复：支持中英文冒号 + 空格变化
        category_match = re.search(r"Category\s*[:：]\s*(.+)", text)
        summary_match = re.search(r"Summary\s*[:：]\s*(.+)", text)

        category = category_match.group(1).strip() if category_match else None
        summary = summary_match.group(1).strip() if summary_match else None

        # ⭐ 再做一次兜底（关键）
        if not category or len(category) > 10:
            category = "其他"

        if not summary:
            summary = "暂无摘要"

        return category, summary

    except Exception as e:
        print("AI ERROR:", e)
        return "其他", "暂无摘要"
