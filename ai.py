import os
import re
import google.generativeai as genai
from openai import OpenAI

# ===== Gemini =====
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# ===== OpenAI =====
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gemini_ai(title, content):
    prompt = f"""
你是新闻分析系统。

基于全文输出：

Category: 经济/天气/事故/政治/交通/发展/其他
Summary: 一句话中文（30字以内）

标题：
{title}

内容：
{content}
"""

    res = gemini_model.generate_content(prompt)
    return res.text.strip()


def openai_ai(title, content):
    res = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "你是新闻分析系统，输出：Category + Summary，两行中文"
            },
            {
                "role": "user",
                "content": f"{title}\n\n{content}"
            }
        ]
    )

    return res.choices[0].message.content.strip()


def parse(text):
    category = "其他"
    summary = "暂无摘要"

    cat = re.search(r"(经济|天气|事故|政治|交通|发展|其他)", text)
    if cat:
        category = cat.group(1)

    lines = text.split("\n")
    for line in lines:
        if len(line.strip()) > 5:
            summary = line.strip()

    return category, summary


# ===== 最终入口（多AI自动切换） =====
def analyze(title, content):
    try:
        print("TRY GEMINI")
        text = gemini_ai(title, content)
        return parse(text)

    except Exception as e:
        print("GEMINI FAIL:", e)

        try:
            print("TRY OPENAI")
            text = openai_ai(title, content)
            return parse(text)

        except Exception as e2:
            print("OPENAI FAIL:", e2)

            return "其他", f"新闻：{title}"
