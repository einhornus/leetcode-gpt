import gpt
import os
import urllib.parse
import time


def summarize_script(script, project, title, word_count=100, model="gpt-3.5-turbo"):
    sections = script.split("\n\n")
    res_summary = ""
    for index, section in enumerate(sections):
        messages = [{
            "role": "system",
            "content": f"You are SummarizeGPT. Please summarize the given section "
                       f"of the {project} script in about {word_count} words. "
                       f"Please be very concise and straight to the point."
        }, {
            "role": "user",
            "content": section
        }]
        res = gpt.call_chatgpt_on_messages(messages, model=model, temperature=0.0, max_tokens=500)
        res = res.replace("\n", "")
        res_summary += res
        if index != len(sections) - 1:
            res_summary += "\n"
    res_summary = urllib.parse.unquote(title).replace("_", " ") + "\n" + res_summary
    return res_summary


def summarize_project(project):
    dirs = os.listdir("data//" + project + "//data")
    for dir in dirs:
        script_path = "data//" + project + "//data//" + dir + "//script.txt"
        script_content = open(script_path, "r", encoding="utf-8").read()
        summarized_script = summarize_script(script_content, project, dir, model='gpt-3.5-turbo')
        summary_path = "data//" + project + "//data//" + dir + "//summary.txt"
        with open(summary_path, mode='w', encoding='utf-8') as f:
            f.write(summarized_script)
        exit(0)


if __name__ == "__main__":
    summarize_project("Futurama")
