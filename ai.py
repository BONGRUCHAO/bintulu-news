from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

def summarize(title):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize news in one short sentence."},
                {"role": "user", "content": title}
            ],
            temperature=0.3
        )

        return res.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", e)
        return title  # fallback