from openai import OpenAI

client = OpenAI(api_key="YOUR_KEY")

def summarize(title):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize news in 1 sentence."},
            {"role": "user", "content": title}
        ]
    )
    return response.choices[0].message.content
