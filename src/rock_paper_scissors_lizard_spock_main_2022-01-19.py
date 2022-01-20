from datetime import *
import random
import copy

from src.models import *


# rock paper scissors lizard spock 01
# 1. make terminal-game
# 2. make one player against random-hand-generator
# logbook
# 3. TODO: no win-counter
# 4. TODO: no picked-hand-counter
# 5. TODO: no database
# 6. TODO: no menu: play, statistik, data upload
# 7. TODO: no api name+Symbol+symbolzahl

# query has to be more efficient
# the orientation of the query is clockwise, according to
# https://static.wikia.nocookie.net/bigbangtheory/images/7/7d/RPSLS.png/revision/latest?cb=20120822205915


def print_hand_option(hand: Hand):
    print("\t" + str(hand.value) + ": " + hand.name)


def print_option(last_number: int, name: str):
    last_number = last_number + 1
    print("\t" + str(last_number) + ": " + name)
    return last_number


def print_option_description(name: str, description: str):
    print("\t" + name + ":\n\t\t" + description)


def play_one_round(player: Hand, opponent: Hand):
    # a draw
    if player == opponent:
        return Result.DRAW
    # rock
    if player == Hand.ROCK:
        if opponent == Hand.LIZARD or opponent == Hand.SCISSORS:
            return Result.WIN
        if opponent == Hand.SPOCK or opponent == Hand.PAPER:
            return Result.LOSE
    # scissors
    if player == Hand.SCISSORS:
        if opponent == Hand.PAPER or opponent == Hand.LIZARD:
            return Result.WIN
        if opponent == Hand.ROCK or opponent == Hand.SPOCK:
            return Result.LOSE
    # paper
    if player == Hand.PAPER:
        if opponent == Hand.ROCK or opponent == Hand.SPOCK:
            return Result.WIN
        if opponent == Hand.LIZARD or opponent == Hand.SCISSORS:
            return Result.LOSE
    # lizard
    if player == Hand.LIZARD:
        if opponent == Hand.SPOCK or opponent == Hand.PAPER:
            return Result.WIN
        if opponent == Hand.SCISSORS or opponent == Hand.ROCK:
            return Result.LOSE
    # spock
    if player == Hand.SPOCK:
        if opponent == Hand.SCISSORS or opponent == Hand.ROCK:
            return Result.WIN
        if opponent == Hand.PAPER or opponent == Hand.LIZARD:
            return Result.LOSE
    return "failure"


def readme():
    print("\nhelp")
    print("-rock-paper-scissors-lizard-spock")
    print("\tPlay the mini-game rock-paper-scissors-game with extension.")
    print("-options")
    print_option_description("help", "You are right know in \"help\"")
    print_option_description("change name", "Change your player-name")
    print_option_description("play", "At \"play\" you can play some rounds")
    print_option_description("statistic", "Show the local player-statistics")
    print_option_description("upload", "Upload the data in the logbook to the api")
    print_option_description("show logbook", "Shows the data in the logbook")
    print_option_description("reset logbook", "Empties the logbook")
    print("done\n")


class RockPaperScissorsLizardSpock:
    mysql_host = "Localhost"
    mysql_user = "swp-rubner"
    mysql_password = "swp-rubner"
    mysql_database = "swp_rubner"
    name = "Anonymous"
    logbook_initiator = {
        "init": {
            "session_timestamp": str(datetime.now()),
            "round": 0,
            "player_one_name": "player_one",
            "player_one_hand": 0,
            "player_one_result": 0,
            "player_two_name": "player_two",
            "player_two_hand": 0,
            "player_two_result": 0
        }
    }
    logbook = {}

    def __init__(self):
        self.reset_logbook()

    def menu(self):
        interrupt = False
        options = [readme, self.change_name, self.play, self.statistic, self.upload, self.show_logbook,
                   self.reset_logbook]
        print(f"\nWelcome {self.name} to rock-paper-scissors-lizard-spock")
        while (not interrupt):
            last_number = -1
            print(f"\nYour choices {self.name}")
            last_number = print_option(last_number, "help")
            last_number = print_option(last_number, "change name")
            last_number = print_option(last_number, "play")
            last_number = print_option(last_number, "statistic")
            last_number = print_option(last_number, "upload")
            last_number = print_option(last_number, "show logbook")
            last_number = print_option(last_number, "reset logbook")
            last_number = print_option(last_number, "exit")
            try:
                choice = int(input("Your choice? "))
                if choice == last_number:
                    interrupt = True
                else:
                    options[choice]()
            except ValueError:
                print("\nPick a number!")
            except IndexError:
                print("\nPick a number in the given range!")
            print("")
        print("\nBye")

    def change_name(self):
        print("\nchange name")
        while True:
            user_input = input("Type your name: ")
            if user_input != "COM":
                self.name = user_input
                break
            else:
                print("\nName is not allowed to be \"COM\"")

    def play(self):
        print("\nplay")
        interrupt = False

        while not interrupt:
            last_number = -1
            print(f"\nYour choices {self.name}")
            last_number = print_option(last_number, "play one round against computer")
            last_number = print_option(last_number, "exit")
            session_timestamp: datetime = datetime.now()
            round_temp: int = 1
            try:
                choice = int(input("Your choice? "))
                print()
                if choice == last_number:
                    interrupt = True
                else:
                    com_choice = random.randint(0, len(Hand) - 1)
                    round_temp = (
                            self.logbook[(str(len(self.logbook) - 1) if (len(self.logbook) - 1) != 0 else "init")][
                                "round"] + 1)
                    logbook_temp = self.play_sure(session_timestamp, round_temp, self.name, choice, "COM", com_choice)
                    self.insert_logbook_into_db(copy.deepcopy(logbook_temp))
                    self.logbook[str(len(self.logbook))] = copy.deepcopy(logbook_temp)
            except ValueError:
                print("\nPick a number!")
            except IndexError:
                print("\nPick a number in the given range!")
        print("done\n")

    def play_sure(self, session_timestamp: datetime, round: int, player_one_name: str, player_one_hand: int,
                  player_two_name: str, player_two_hand: int):
        while True:
            print(f"Your choices {self.name}")
            for hand in Hand:
                print_hand_option(hand)
            print_option(len(Hand), "exit")
            logbook_temp = {}
            try:
                choice = int(input("Your choice? "))
                if choice == len(Hand):
                    interrupt = True
                else:
                    result = play_one_round(Hand(player_one_hand), Hand(player_two_hand)).value
                    print("%-8s" % Hand(player_one_hand).name, end="")
                    print(" vs %-8s" % Hand(player_two_hand).name, end="")
                    print("\tresult: " + str(Result(result).name))
                    logbook_temp["session_timestamp"] = str(session_timestamp)
                    logbook_temp["round"] = round
                    logbook_temp["player_one_name"] = player_one_name
                    logbook_temp["player_one_hand"] = player_one_hand
                    logbook_temp["player_one_result"] = result
                    logbook_temp["player_two_name"] = player_two_name
                    logbook_temp["player_two_hand"] = player_two_hand
                    logbook_temp["player_two_result"] = len(Result) - result
                    print(logbook_temp)
                    return logbook_temp
            except ValueError:
                print("\nPick a number!")
            except IndexError:
                print("\nPick a number in the given range!")

    def statistic(self):
        print("\nstatisic")
        print("done\n")

    def upload(self):
        print("\nupload")
        print("done\n")

    def show_logbook(self):
        for key_self in self.logbook:
            for key_2_self in self.logbook[key_self]:
                print("%-28s" % (key_2_self if key_self == "init" else self.logbook[key_self][key_2_self]),
                      end="")
            print()

    def reset_logbook(self):
        self.logbook = copy.deepcopy(self.logbook_initiator)

    # database-things

    def insert_logbook_into_db(self, logbook_temp: dict):
        lt = logbook_temp
        connection = mysql.connector.connect(host=self.mysql_host, user=self.mysql_user, password=self.mysql_password, database=self.mysql_database)
        mycursor = connection.cursor()
        sql = f'''INSERT INTO rpsls_game_history(
        	session_timestamp,
            round,
            player_one_name, 
            player_one_hand, 
            player_one_result, 
            player_two_name, 
            player_two_hand, 
            player_two_result
        )VALUES(%s,%s,%s,%s,%s,%s,%s,%s);'''
        val = (lt["session_timestamp"],
            lt["round"],
            lt["player_one_name"],
            lt["player_one_hand"],
            lt["player_one_result"],
            lt["player_two_name"],
            lt["player_two_hand"],
            lt["player_two_result"])
        mycursor.execute(sql, val)
        connection.commit()
        # print(mycursor.rowcount, "record inserted.")




if __name__ == '__main__':
    rpsls = RockPaperScissorsLizardSpock()
    rpsls.menu()
