import os
import openai

# Initialize the API key
openai.api_key = os.environ.get("GPT_API_KEY")

def query_api(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", ##
        #model="gpt-3.5-turbo-0301", ## ateh 1 junho 2023
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return response.choices[0].message.content

def generates_response(question, profile):
    mensagens = [{"role": "system", "content": f"{profile}"}]
    mensagens.append({"role": "user", "content": str(question)})
    answer = query_api(mensagens)
    return answer