import os
import google.generativeai as genai
from openai import OpenAI

# ====== Gemini ======
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# ====== OpenAI ======
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def gemini_ai(title):
    response = gemini_model.generate_content(
        f"用中文一句话总结新闻，不超过30字：{title}"
    )
    return response.text.strip()


def openai_ai(title):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是新闻摘要助手，用中文一句话总结，不超过30字"},
            {"role": "user", "content": title}
        ]
    )
    return response.choices[0].message.content.strip()


def fallback_ai(title):
    return f"新闻：{title}"


# ====== 主入口（自动切换） ======
def analyze(title):
    try:
        print("TRY GEMINI")
        return "其他", gemini_ai(title)

    except Exception as e:
        print("GEMINI FAIL:", e)

        try:
            print("TRY OPENAI")
            return "其他", openai_ai(title)

        except Exception as e2:
            print("OPENAI FAIL:", e2)

            return "其他", fallback_ai(title)
