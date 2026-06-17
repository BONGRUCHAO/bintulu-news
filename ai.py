import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def summarize(title):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize this news headline in one sentence."
                },
                {
                    "role": "user",
                    "content": title
                }
            ]
        )

        summary = response.choices[0].message.content

        print("AI RESULT:", summary)

        return summary

    except Exception as e:
        print("AI ERROR:", e)

        return "AI Summary Failed"
