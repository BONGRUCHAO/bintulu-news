import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze(title):
    try:
        prompt = f"""
你是新闻分析系统。

请完成两件事：

1. 分类（只能选一个）：
经济 / 天气 / 事故 / 政治 / 交通 / 发展 / 其他

2. 一句话中文摘要（不超过30字）

3. 城市，地名，用英文

严格输出格式：
Category: xxx
Summary: xxx

新闻标题：
{title}
"""

        response = model.generate_content(prompt)
        text = response.text.strip()

        category = "其他"
        summary = ""

        for line in text.split("\n"):
            if "Category:" in line:
                category = line.replace("Category:", "").strip()
            if "Summary:" in line:
                summary = line.replace("Summary:", "").strip()

        print("AI RESULT:", text)

        return category, summary

    except Exception as e:
        print("AI ERROR:", e)
        return "其他", "暂无摘要"
