from enum import Enum
import mysql.connector

# date: 13.01.2022

class Hand(Enum):
    ROCK = 0
    SCISSORS = 1
    PAPER = 2
    LIZARD = 3
    SPOCK = 4


class Result(Enum):
    DRAW = 0
    WIN = 1
    LOSE = 2


class Player:
    def __init__(self, player_name: str):
        self.id = None
        self.player_name = player_name
        self.player_creation_timestamp = None


class Session:
    def __init__(self, player_one: Player, player_two: Player):
        self.id = None
        self.player_one = player_one
        self.player_two = player_two
        self.session_timestamp = None


class GameResult:
    def __init__(self, round: int, player_one_hand: Hand, player_two_hand: Hand, result: Result, session: Session):
        self.id = None
        self.round = round
        self.player_one_hand = player_one_hand
        self.player_two_hand = player_two_hand
        self.result = result
        self.session = session


if __name__ == '__main__':
    print()


class DB:
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password

    def getConnection(self):
        return mysql.connector.connect(host= self.host, user= self.user, password= self.password)

    def prepare_database(self):
        dbcursor = self.getConnection().cursor()
        print(sql_create_database)
        print(sql_use)
        print(sql_create_table_player)
        print(sql_create_table_session)
        print(sql_create_table_game_result)
        dbcursor.execute(sql_create_database)
        print("lel")
        dbcursor.execute(sql_use)
        print("lel")
        dbcursor.execute(sql_create_table_player)
        dbcursor.execute(sql_create_table_session)
        dbcursor.execute(sql_create_table_game_result)

    def insert_player(self, player: Player):
        connection = self.getConnection()
        mycursor = connection.cursor()
        mycursor.execute(sql_insert_table_player, (player.player_name))
        connection.commit()


database_name = "swp_rubner_rpsls"
table_name_player = "t_player_rpsls"
table_name_session = "t_session_rpsls"
table_name_game_result = "t_game_result_rpsls"

sql_create_database = f"CREATE DATABASE IF NOT EXISTS {database_name};"
sql_use = "USE swp_rubner_rpsls;"
sql_create_table_player = f'''CREATE TABLE IF NOT EXISTS {table_name_player}(
	id int auto_increment,
    player_name varchar(16) not null, 
    player_creation_timestamp timestamp default current_timestamp,
    primary key(id)
);'''
sql_create_table_session = f'''CREATE TABLE IF NOT EXISTS {table_name_session}(
	id int auto_increment,
    player_one_id int not null,
    player_two_id int not null, 
    session_timestemp timestamp default current_timestamp,
    primary key(id),
    foreign key(player_one_id) references t_player_rpsls(id),
	foreign key(player_two_id) references t_player_rpsls(id)
);'''
sql_create_table_game_result = f'''CREATE TABLE IF NOT EXISTS {table_name_game_result}(
	id int auto_increment,
    round int, 
    player_one_hand int not null,
    player_two_hand int not null,
    result int  not null,
    session_id int,
    primary key(id), 
    foreign key(session_id) references t_session_rpsls(id)
);'''

sql_insert_table_player = f"INSERT INTO {table_name_player} (player_name) VALUES (%s);"
sql_insert_table_session = f"INSERT INTO {table_name_session} (player_one_id, player_two_id) VALUES (%s, %s);"
sql_insert_table_game_result = f'''INTO {table_name_game_result} 
    (round, player_one_hand, player_two_hand, result, session_id) 
    VALUES (%s, %s, %s, %s, %s)
;'''

