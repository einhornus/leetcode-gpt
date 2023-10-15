import requests
from bs4 import BeautifulSoup
import tiktoken
import os


def count_tokens(str):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(str))
    return num_tokens


def download_episode_script(episode):
    target_token_count = 2000
    max_tokens_count = 2800

    episode_url = f"https://futurama.fandom.com/wiki/{episode}/Transcript"
    response = requests.get(episode_url)
    if response.status_code == 200:
        content = response.content
        content = content.decode("utf-8")

        transcript_start_indicator1 = "<div class=\"mw-parser-output\">"
        transcript_start_index1 = content.index(transcript_start_indicator1) + len(transcript_start_indicator1)
        content = content[transcript_start_index1:]
        content = content[:content.index("<!--")]

        text = BeautifulSoup(content, "html.parser").get_text()
        lines = text.split("\n")
        lines = [line.strip() for line in lines if line.strip() != ""]
        lines = lines[6:]
        lines = [line + "\n" for line in lines]
        tokens_counts = [count_tokens(line) for line in lines]

        res = []
        current_line = ""
        current_token_count = 0
        for line in lines:
            do_stop = False
            if current_token_count + count_tokens(line) > max_tokens_count:
                do_stop = True
            if current_token_count + count_tokens(line) > target_token_count:
                if "Scene:" in line:
                    do_stop = True
            if do_stop:
                res.append(current_line)
                current_line = ""
                current_token_count = 0
            current_line += line
            current_token_count += count_tokens(line)
        if current_token_count < 500:
            res[-1] += current_line
        else:
            res.append(current_line)

        dir = "data//" + episode
        os.makedirs(dir, exist_ok=True)
        file = dir + "//script.txt"

        content = ""
        for index, section in enumerate(res):
            content += "".join(section)
            if index != len(res) - 1:
                content += "\n"

        with open(file, mode = 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print("Can't load", episode_url)

if __name__ == "__main__":
    episodes = [
        "Space_Pilot_3000",
        "Attack_of_the_Killer_App",
        "A_Bicyclops_Built_for_Two",
        "A_Big_Piece_of_Garbage",
        "A_Clockwork_Origin",
        "A_Clone_of_My_Own",
        "A_Farewell_to_Arms",
        "A_Fishful_of_Dollars",
        "A_Head_in_the_Polls",
        "A_Leela_of_Her_Own",
        "A_Pharaoh_to_Remember",
        "A_Tale_of_Two_Santas",
        "A_Taste_of_Freedom",
        "All_the_Presidents%27_Heads",
        "Amazon_Women_in_the_Mood",
        "Bend_Her",
        "Bender_Gets_Made",
        "Bender_Should_Not_Be_Allowed_on_Television",
        "Benderama",
        "Bendin%27_in_the_Wind",
        "Bendless_Love",
        "Brannigan,_Begin_Again",
        "Cold_Warriors",
        "Crimes_of_the_Hot",
        "Decision_3012",
        "Fear_of_a_Bot_Planet",
        "Free_Will_Hunting",
        "Fry_%26_the_Slurm_Factory",
        "Future_Stock",
        "Ghost_in_the_Machines",
        "Hell_Is_Other_Robots",
        "How_Hermes_Requisitioned_His_Groove_Back",
        "I_Dated_a_Robot",
        "I_Second_That_Emotion",
        "In-A-Gadda-Da-Leela",
        "Insane_in_the_Mainframe",
        "Jurassic_Bark",
        "Kif_Gets_Knocked_Up_a_Notch",
        "Law_and_Oracle",
        "Leela%27s_Homeworld",
        "Less_than_Hero",
        "Lethal_Inspection",
        "Love_and_Rocket",
        "Lrrreconcilable_Ndndifferences",
        "Mars_University",
        "Meanwhile",
        "Mother%27s_Day",
        "M%C3%B6bius_Dick",
        "Neutopia",
        "Obsoletely_Fabulous",
        "Parasites_Lost",
        "Proposition_Infinity",
        "Put_Your_Head_on_My_Shoulders",
        "Raging_Bender",
        "Rebirth",
        "Roswell_that_Ends_Well",
        "Spanish_Fry",
        "Stench_and_Stenchibility",
        "Teenage_Mutant_Leela%27s_Hurdles",
        "That_Darn_Katz!",
        "That%27s_Lobstertainment!",
        "The_30%25_Iron_Chef",
        "The_Birdbot_of_Ice-Catraz",
        "The_Bots_and_the_Bees",
        "The_Cryonic_Woman",
        "The_Cyber_House_Rules",
        "The_Deep_South",
        "The_Devil%27s_Hands_Are_Idle_Playthings",
        "The_Duh-Vinci_Code",
        "The_Honking",
        "The_Late_Philip_J._Fry",
        "The_Lesser_of_Two_Evils",
        "The_Luck_of_the_Fryrish",
        "The_Mutants_Are_Revolting",
        "The_Prisoner_of_Benda",
        "The_Prisoner_of_Benda",
        "The_Route_of_All_Evil",
        "The_Series_Has_Landed",
        "The_Silence_of_the_Clamps",
        "The_Six_Million_Dollar_Mon",
        "The_Sting",
        "The_Why_of_Fry",
        "Three_Hundred_Big_Boys",
        "Time_Keeps_on_Slippin%27",
        "War_is_the_H-Word",
        "When_Aliens_Attack",
        "Where_No_Fan_Has_Gone_Before",
        "Where_the_Buggalo_Roam",
        "Why_Must_I_Be_a_Crustacean_in_Love%3F",
        "Xmas_Story",
        "Yo_Leela_Leela",
    ]

    for episode in episodes:
        download_episode_script(episode)
