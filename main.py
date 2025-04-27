import random

import requests
import json

def ask_model(prompt):
    url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": "qwen2.5-coder:3b",
        "prompt": prompt,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("response", "")
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")
        return None

def generate_task():

    prompt = f"""Generate a math problem.

It should be simple .
It shouldn`t unlude simple text, only formuls 
Analyze the task and write a short answer to it
random generation key - {random.random()}
answer is number or numbers
I just need an answer, remove the words: question and answer
output your answer by type :
problem: problem
answer: answer


"""

    answer = str(ask_model(prompt)).lower()

    return answer


if __name__ == "__main__":
    print(generate_task())
