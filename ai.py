import os
import google.generativeai as genai
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze(title):
    try:
        prompt = f"""
你是新闻分析系统。

请严格按下面格式输出（必须严格一致）：

Category: 经济/天气/事故/政治/交通/发展/其他
Summary: 一句话中文摘要，不超过30字

必须严格输出两行：
Category: xxx
Summary: xxx
不要合并在一行
不要加任何解释

不要添加任何多余内容。

新闻标题：
{title}
"""

        response = model.generate_content(prompt)
        text = response.text.strip()

        print("AI RAW:", text)

        # 用正则强解析（关键修复点）
        category_match = re.search(r"Category\s*[:：]\s*(.*)", text)
        summary_match = re.search(r"Summary\s*[:：]\s*(.*)", text)

        category = category_match.group(1).strip() if category_match else "其他"
        summary = summary_match.group(1).strip() if summary_match else "暂无摘要"

        return category, summary

    except Exception as e:
        print("AI ERROR:", e)
        return "其他", "暂无摘要"
