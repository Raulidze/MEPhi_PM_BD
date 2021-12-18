import random, math, datetime, string
from dataclasses import dataclass

import numpy as np
import psycopg2
from transliterate import translit

from people_data import maleNames, maleSurNames, femaleNames, femaleSurNames

# DATACLASSES
@dataclass
class Player:
    """Class for keeping player data."""
    # data
    player_id: int
    surname: str
    name: str
    date_of_birth: datetime.date
    email: str
    match_count: int
    hours_count: float #!!!
    victory_count: int
    rating: int
    name: str
    # for generation
    # success_rate: float

    def win(self, hours_count) -> None:
        self.match_count += 1
        self.hours_count += hours_count
        self.victory_count += 1
    
    def lose(self, hours_count) -> None:
        self.match_count += 1
        self.hours_count += hours_count
    
    def tie(self, hours_count) -> None:
        self.match_count += 1
        self.hours_count += hours_count

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Player):
            return self.player_id == other.player_id
        return False

    def __hash__(self) -> int:
        return hash(self.player_id)

    # def total_cost(self) -> float:
    #     return self.unit_price * self.quantity_on_hand

@dataclass
class Tournament:
    """Class for keeping tournament data."""
    tournament_id: int
    name: str
    number_of_players: int
    required_rating: int
    player_queue: str

@dataclass
class PlayersTournament:
    """Class for keeping players & tournaments data."""
    players_tournaments_id: int
    player_id: int
    tournament_id: int

@dataclass
class PlayersGames:
    """Class for keeping players & games data."""
    players_games_id: int
    player_id: int
    game_id: int

@dataclass
class PlayerCourses:
    """Class for keeping players & courses data."""
    players_courses_id: int
    player_id: int
    course_id: int

@dataclass
class Task:
    """Class for keeping task data."""
    task_id: int
    name: str
    start_position: str
    move_sequence: str
    course_id: int

@dataclass
class GameMode:
    """Class for keeping gamemode data."""
    gamemode_id: int
    name: str
    game_time: int
    extra_time_per_move: int

@dataclass
class Game:
    """Class for keeping game data."""
    game_id: int
    datetime: datetime.datetime
    result: str
    moves: str
    white_player_id: int
    gamemode_id: int
    tournament_id: int

# UTILITY
def randomBool():
    return bool(random.getrandbits(1))


# DB OPERATIONS
def rollback(conn) -> None:
    curs = conn.cursor()
    curs.execute("ROLLBACK")
    conn.commit()

def getGameModes(conn) -> list[GameMode]:
    cur = conn.cursor()
    cur.execute('SELECT * FROM gamemodes;')
    res = cur.fetchall()
    gamemodes = list()
    for t in res:
        gamemodes.append(GameMode(
            gamemode_id=t[0],
            name=t[1],
            game_time=t[2],
            extra_time_per_move=t[3]
        ))
    return gamemodes

def getCourses(conn) -> dict:
    cur = conn.cursor()
    cur.execute('SELECT * FROM Courses;')
    res = cur.fetchall()
    сourses = list()
    for t in res:
        сourses.append({
            'course_id': t[0],
            'name': t[1],
            'number_of_tasks': t[2]
        })
    return сourses


# INSERTS
def insertPlayer(conn, player: Player):
    cursor = conn.cursor()
    t_player = (
        player.player_id,
        player.surname,
        player.name,
        player.date_of_birth,
        player.email,
        player.match_count,
        player.hours_count,
        player.victory_count,
        player.rating
    )
    cursor.execute("INSERT INTO players (player_id, surname, name, date_of_birth, email, match_count, hours_count, victory_count, rating) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", t_player)
    conn.commit()

def insertTournament(conn, tournament: Tournament):
    cursor = conn.cursor()
    t_tournament = (
        tournament.tournament_id,
        tournament.name,
        tournament.number_of_players,
        tournament.required_rating,
        tournament.player_queue
    )
    cursor.execute("INSERT INTO tournaments (tournament_id, name, number_of_players, required_rating, player_queue) VALUES(%s, %s, %s, %s, %s)", t_tournament)
    conn.commit()

def insertGame(conn, game: Game):
    cursor = conn.cursor()
    t_game = (
        game.game_id,
        game.datetime,
        game.result,
        game.moves,
        game.white_player_id,
        game.gamemode_id,
        game.tournament_id
    )
    cursor.execute("INSERT INTO games (game_id, datetime, result, moves, white_player_id, gamemode_id, tournament_id) VALUES(%s, %s, %s, %s, %s, %s, %s)", t_game)
    conn.commit()

def insertPlayerTournament(conn, playertournament: PlayersTournament):
    cursor = conn.cursor()
    t_playertournament = (
        playertournament.players_tournaments_id,
        playertournament.player_id,
        playertournament.tournament_id
    )
    cursor.execute("INSERT INTO playerstournaments (players_tournaments_id, player_id, tournament_id) VALUES(%s, %s, %s)", t_playertournament)
    conn.commit()

def insertPlayerGame(conn, playergame: PlayersGames):
    cursor = conn.cursor()
    t_playergame = (
        playergame.players_games_id,
        playergame.player_id,
        playergame.game_id
    )
    cursor.execute("INSERT INTO playersgames (players_games_id, player_id, game_id) VALUES(%s, %s, %s)", t_playergame)
    conn.commit()

def insertPlayersCourses(conn, playerscourses: PlayerCourses):
    cursor = conn.cursor()
    t_playerscourses = (
        playerscourses.players_courses_id,
        playerscourses.player_id,
        playerscourses.course_id
    )
    cursor.execute("INSERT INTO playerscourses (players_courses_id, player_id, course_id) VALUES(%s, %s, %s)", t_playerscourses)
    conn.commit()

def insertTask(conn, task: Task):
    cursor = conn.cursor()
    t_task = (
        task.task_id,
        task.name,
        task.start_position,
        task.move_sequence,
        task.course_id
    )
    cursor.execute("INSERT INTO tasks (task_id, name, start_position, move_sequence, course_id) VALUES(%s, %s, %s, %s, %s)", t_task)
    conn.commit()


# GENERATION
def generateTasks(conn):
    # сourses = getCourses(conn)
    # for course in сourses:
    pass

def generateNormalDistribution(N: int) -> np.ndarray:
    mu, sigma = 0.01, 0.1 # mean and standard deviation
    s = np.random.normal(mu, sigma, N)
    s = s - s.min()
    s = s / s.max()
    return s

def generateRatings(N: int) -> np.ndarray:
    return (generateNormalDistribution(N) * 2000) + 500

def generatePlayer(player_id: int, rating):
    global maleNames, maleSurNames, femaleNames, femaleSurNames

    if randomBool():
        name = random.choice(maleNames)
        surname = random.choice(maleSurNames)
    else:
        name = random.choice(femaleNames)
        surname = random.choice(femaleSurNames)
    
    age = random.randint(15, 70)
    date_of_birth = datetime.date.today() - datetime.timedelta(days=365*age)

    email = (translit(name[0] + surname, 'ru', reversed=True) + "@yandex.ru").replace("'", "")
    # match_count = random.randint(0, 10000)
    # hours_count = match_count * int((random.randint(0, 90)) / 60)

    # success_rate = random.uniform(0.3, 0.9)
    # victory_count = match_count * success_rate
    
    player = Player(
        player_id=player_id,
        surname=surname,
        name=name,
        date_of_birth=date_of_birth,
        email=email,
        match_count=0,
        hours_count=0,
        victory_count=0,
        rating=rating,
        # success_rate=success_rate
    ) 

    return player

def generatePlayers(N):

    players: list[Player] = list()
    ratings = generateRatings(N)

    for i in range(N):
        player = generatePlayer(i + 1, ratings[i])
        players.append(player)
    
    return players

def playGame(player1: Player, player2: Player) -> int:
    """Returns who won, 1 or 2 player"""
    diff = (player1.rating  - player2.rating) / player1.rating 
    p = math.atan(math.pi*diff/4) + 0.5
    if 0.4 < p < 0.6 and random.choice([True, False]):
        return 0
    elif p > 0.5: return 1
    else: return 2

def generateMoves() -> str:
    N = random.randint(10, 100)
    res = ''
    for _ in range(N):
        s1 = random.choice(['K', 'Q', 'R', 'B', 'N']) if random.choice([True, False]) else ''
        s2 = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
        s3 = random.choice(['1', '2', '3', '4', '5', '6', '7', '8'])
        res += s1 + s2 + s3 + '/'
    return res

def generateTasks(courses: list[dict]) -> list[Task]:
    tasks: list[Task] = list()
    task_id = 1
    for course in courses:
        number_of_tasks = course['number_of_tasks']
        for _ in range(number_of_tasks):
            tasks.append(Task(
                task_id=task_id,
                name=f"{course['name']} #{task_id}",
                start_position=generateMoves(),
                move_sequence=generateMoves(),
                course_id=course['course_id']
            ))
            task_id += 1
    return tasks

def generateANDInsertPlayersCourses(conn, players: list[Player], courses: list[dict]):
    players_courses_id = 1
    for player in players:
        for _ in range(random.randint(1, 3)):
            course = random.choice(courses)
            insertPlayersCourses(conn, PlayerCourses(
                players_courses_id=players_courses_id,
                player_id=player.player_id,
                course_id=course['course_id']
            ))
            players_courses_id += 1

def makeTournaments(conn, N: int, players: list[Player]):

    tournaments: list[Tournament] = list()
    games: list[Game] = list()
    playerstournaments: list[PlayersTournament] = list()
    playersgames: list[PlayersGames] = list()

    game_id = 1
    players_games_id = 1
    players_tournaments_id = 1

    gameModes = getGameModes(conn)

    for i in range(N):
        
        tournament_id = i + 1

        tournament_date = datetime.date.today() - datetime.timedelta(days=random.randint(1, 300))

        number_of_players = random.randint(5, 20)
        required_rating = random.randint(10, 15) * 100

        # choose players for tournament
        player_queue = str()
        players_in_tournament: set[Player] = set()
        while len(players_in_tournament) < number_of_players:
            player = random.choice(players)
            if player.rating >= required_rating:
                players_in_tournament.add(player)
                playerstournaments.append(PlayersTournament(
                    players_tournaments_id=players_tournaments_id,
                    player_id=player.player_id,
                    tournament_id=tournament_id
                ))
                players_tournaments_id += 1
                player_queue += '>' + str(player.player_id)
        
        gamemode = random.choice(gameModes)

        # play tournament
        # every player with every player
        for player1 in players_in_tournament:
            for player2 in players_in_tournament:
                if player1 != player2:
                    # play game
                    game = Game(
                        game_id=game_id,
                        datetime=tournament_date,
                        result='',
                        moves=generateMoves(),
                        white_player_id=player1.player_id,
                        gamemode_id=gamemode.gamemode_id,
                        tournament_id=tournament_id
                    )

                    game_time = gamemode.game_time/60

                    if playGame(player1, player2) == 0:
                        player1.tie(game_time)
                        player2.tie(game_time)
                        game.result = 'tie'
                    elif playGame(player1, player2) == 1:
                        player1.win(game_time)
                        player2.lose(game_time)
                        game.result = 'white won'
                    else:
                        player1.lose(game_time)
                        player2.win(game_time)
                        game.result = 'black won'
                    
                    playersgames.append(PlayersGames(
                        players_games_id=players_games_id,
                        player_id=player1.player_id,
                        game_id=game_id
                    ))
                    players_games_id += 1
                    playersgames.append(PlayersGames(
                        players_games_id=players_games_id,
                        player_id=player2.player_id,
                        game_id=game_id
                    ))
                    players_games_id += 1
                    games.append(game)
                    
                    game_id += 1
        
        tournaments.append(Tournament(
            tournament_id=tournament_id,
            name='tournament #' + str(tournament_id),
            number_of_players=number_of_players,
            required_rating=required_rating,
            player_queue=player_queue
        ))

    return tournaments, games, playerstournaments, playersgames