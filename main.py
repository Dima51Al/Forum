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
    prompt = f"""Generate a math task.

    It should be very simple.
    Include only formulas, no descriptive text.
    Analyze the task and provide a brief numeric response.
    Random generation key: {random.random()}
    Output format:
    task: [mathematical task]
    response: [numeric response]
    """

    answer = str(ask_model(prompt)).lower()

    return answer

def split_gen():
    task = generate_task()
    task = task.replace(" ", "")

    task1 = task.replace("task:", "")
    answer = task1.split("response:")

    return answer

if __name__ == "__main__":
    print(split_gen())
