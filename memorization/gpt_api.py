import os
from time import sleep
import openai

openai.api_key = os.environ.get("GPT_API_KEY")

def query_api(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

def sentence_generator(question):
    mensagens = [{"role": "user", "content": "you are an english teacher"}]
    mensagens.append({"role": "user", "content": question})
    try:
        answer = query_api(mensagens)
        return answer
    except Exception as exc:
        print(f"openai exception: {exc}")

        sleep(3)

        sentence_generator(question)