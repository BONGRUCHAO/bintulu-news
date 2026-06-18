import os
import json
import google.generativeai as genai
from openai import OpenAI

# ===== AI KEY =====
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ===== Prompt（强制JSON）=====
def build_prompt(title, content):
    return f"""
你是新闻分析系统，只能输出JSON，不能有任何多余文字。

JSON格式必须严格如下：
{{
  "category": "经济/天气/事故/政治/交通/发展/其他",
  "summary": "一句话中文，不超过30字"
}}

规则：
- 必须基于内容
- 不允许猜测
- 不允许解释

新闻标题：
{title}

新闻内容：
{content}
"""


# ===== Gemini =====
def gemini_ai(title, content):
    res = gemini_model.generate_content(build_prompt(title, content))
    return res.text.strip()


# ===== OpenAI =====
def openai_ai(title, content):
    res = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "只输出JSON，不要任何解释"
            },
            {
                "role": "user",
                "content": build_prompt(title, content)
            }
        ]
    )
    return res.choices[0].message.content.strip()


# ===== JSON解析（防崩核心）=====
def parse_json(text):
    try:
        # 去掉 ```json
        text = text.replace("```json", "").replace("```", "").strip()

        data = json.loads(text)

        category = data.get("category", "其他")
        summary = data.get("summary", "暂无摘要")

        return category, summary

    except Exception as e:
        print("JSON PARSE FAIL:", e)
        return "其他", "暂无摘要"


# ===== Fallback =====
def fallback(title):
    return "其他", title[:30]


# ===== 主入口（多AI防崩）=====
def analyze(title, content):
    # 1. Gemini
    try:
        print("TRY GEMINI")
        text = gemini_ai(title, content)
        return parse_json(text)

    except Exception as e:
        print("GEMINI FAIL:", e)

    # 2. OpenAI
    try:
        print("TRY OPENAI")
        text = openai_ai(title, content)
        return parse_json(text)

    except Exception as e:
        print("OPENAI FAIL:", e)

    # 3. fallback
    return fallback(title)

def safe_analyze(title, content):
    try:
        if not content:
            content = title

        category, summary = analyze(title, content)

        if not summary:
            summary = title[:30]

        return category, summary

    except Exception as e:
        print("AI FAIL:", e)
        return "其他", title[:30]
