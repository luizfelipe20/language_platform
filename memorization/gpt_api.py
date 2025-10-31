import os
from time import sleep
from openai import OpenAI


client = OpenAI(api_key=os.environ.get("GPT_API_KEY"))


def query_api(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

def sentence_generator(question):
    mensagens = [{"role": "user", "content": "you are an english teacher"}]
    mensagens.append({"role": "user", "content": question})
    try:
        answer = query_api(mensagens)
        print(answer)
        
        validator_answer = [elem in answer for elem in ("Sorry", "sorry", "Desculpe", "ajudar")]
        if any(validator_answer):
            print(f"reexecução..........: {question}")
            sleep(2)
            return sentence_generator(question)

        return answer
    except Exception as exc:
        print(f"openai exception: {exc}")

        sleep(3)

        sentence_generator(question)