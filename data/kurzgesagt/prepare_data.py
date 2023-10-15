import csv

if __name__ == "__main__":
    videos = []
    current_video = {"title": None, "url": None, "sentences": []}

    with open("source.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader):
            if index > 0:
                title = row[0]
                url = row[1]
                sentence = row[2]
                print(row)

        