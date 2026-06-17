import os
import google.generativeai as genai

# 读取环境变量
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def summarize(title):
    try:
        prompt = f"""
你是新闻摘要助手。

请对以下新闻标题进行总结：

要求：
1. 使用简体中文
2. 不超过30个字
3. 只输出一句话，不要解释，不要加前缀
4. 保持客观
5. 城市，地名，用英文

新闻标题：
{title}
"""

        response = model.generate_content(prompt)

        summary = response.text.strip()

        print("AI RESULT:", summary)

        return summary

    except Exception as e:
        print("AI ERROR:", e)
        return "暂无摘要"
