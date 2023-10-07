import json
import random


def to_data(problem):
    res = []
    for key in problem["solutions"]:
        statement = problem["problem"]
        solution = problem["solutions"][key]

        messages = [{
            "role": "system",
            "content": "You are LeetCodeGPT, the competitive programming champion. "
                       "Please solve the given LeetCode problem using " + key + "."
        }, {
            "role": "user",
            "content": statement
        }, {
            "role": "assistant",
            "content": solution
        }]
        obj = {
            "messages": messages
        }
        res.append(json.dumps(obj, ensure_ascii=False))
    return res


def main():
    languages = ["JavaScript", "C++", " C ", "Java", "Python 3", "Python 2", "Rust"]
    res = {}

    with open("data//submissions.jsonl", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            obj = json.loads(line)
            instruction = obj["instruction"]
            statement = obj["input"]
            statement = statement.replace(" ", " ")
            output = obj["output"]

            current_language = None
            for language in languages:
                if language in instruction:
                    current_language = language
                    break
            if current_language == " C ":
                current_language = "C"

            if statement not in res:
                res[statement] = {}

            res[statement][current_language] = output

    res_problems = []
    for problem in res:
        res_problems.append({
            "problem": problem,
            "solutions": res[problem]
        })

    train_problems = res_problems[:int(len(res_problems) * 0.9)]
    validation_problems = res_problems[int(len(res_problems) * 0.9):]

    random.shuffle(train_problems)
    random.shuffle(validation_problems)

    res_train = []
    res_validation = []

    for problem in train_problems:
        res_train += to_data(problem)
    for problem in validation_problems:
        res_validation += to_data(problem)

    with open("data//train.jsonl", "w", encoding="utf-8") as file:
        for line in res_train:
            file.write(line + "\n")
    with open("data//validation.jsonl", "w", encoding="utf-8") as file:
        for line in res_validation:
            file.write(line + "\n")


if __name__ == '__main__':
    main()
