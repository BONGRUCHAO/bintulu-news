import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def summarize(title):
    try:
        response = model.generate_content(
            f"请用一句话总结这条新闻：{title}"
        )

        summary = response.text.strip()

        print("AI RESULT:", summary)

        return summary

    except Exception as e:
        print("AI ERROR:", e)
        return "AI Summary Failed"
