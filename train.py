import json

import openai
import time


def download_file_from_openai(file_id: str, output_file_path: str):
    res = openai.File.download(id=file_id)
    with open(output_file_path, "wb") as f:
        f.write(res)
    return res


def upload_file_to_openai(file_path: str, waiting_interval: int = 10):
    print("Initiating file upload...", file_path)
    elapsed_time = 0
    response = openai.File.create(file=open(file_path, "rb"), purpose="fine-tune")
    uploaded_file_id = response["id"]
    while True:
        file_records = openai.File.list()
        current_file = None
        for file_entry in file_records["data"]:
            if file_entry["id"] == uploaded_file_id:
                current_file = file_entry
        print(f"After {elapsed_time} seconds:")
        print(current_file)
        print("------")
        print()
        if current_file["status"] == "processed":
            break
        else:
            elapsed_time += waiting_interval
            time.sleep(waiting_interval)
    return uploaded_file_id


def run_fine_tuning(base_model="gpt-3.5-turbo", waiting_interval=10):
    print("Initiating file uploads...")

    train_file_id = upload_file_to_openai("data//train.jsonl")
    print("Training file uploaded.")

    valid_file_id = upload_file_to_openai("data//validation.jsonl")
    print("Validation file uploaded.")

    print("Launching fine-tuning process...")
    tuning_job = openai.FineTuningJob.create(training_file=train_file_id, validation_file=valid_file_id,
                                             model=base_model,
                                             hyperparameters={"n_epochs": 3})
    elapsed_time = 0
    current_state = None
    while True:
        current_state = openai.FineTuningJob.retrieve(tuning_job["id"])
        print(f"Elapsed time: {elapsed_time} seconds:")
        print(current_state)
        print("------")
        print()

        if current_state["status"] == "succeeded":
            break
        else:
            time.sleep(waiting_interval)
            elapsed_time += waiting_interval

    for file_id in current_state["result_files"]:
        download_file_from_openai(file_id, f"data//loss.csv")
    return current_state


def main():
    openai.api_key = json.load(open("config.json", "r", encoding="utf-8"))["OPENAI_API_KEY"]
    run_fine_tuning()


if __name__ == "__main__":
    #main()
    download_file_from_openai("file-DtxuNjPL3FLd8sGT3YDbjpvM", "data//loss.csv")
