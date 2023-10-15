import openai
import time


def call_chatgpt_on_messages(messages, model="gpt-3.5-turbo", temperature=0.0, max_tokens=500):
    print("Calling chatgpt with model " + model + " and temperature " + str(temperature) + "...")
    for message in messages:
        print(message["role"] + ": " + message["content"])
    print("--------")

    for i in range(10):
        try:
            completion = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                request_timeout=10
            )

            res = ""
            for stuff in completion:
                if "content" in stuff["choices"][0]["delta"]:
                    res += stuff["choices"][0]["delta"]["content"]
                    print("Streamed", stuff["choices"][0]["delta"]["content"])
            return res
        except Exception as e:
            print(e)
            print(f"Retrying in {2 ** i} seconds...")
            time.sleep(2 ** i)
