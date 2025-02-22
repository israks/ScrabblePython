from random import shuffle

"""
Jeu de Scrabble
Classes:
Tile - Enregistre la lettre du jeton et sa valeur
Rack - Enregistre les jetons dans la main d'un joueur
Bag - Enregistre les jetons restants dans le sac
Word - vérifie la validité d'un mot et son emplacement
Board - Enregistre l'emplacement des jetons sur le plateau
"""
#Garde une trace de la valeur du score de chaque jeton.
LETTER_VALUES = {"A": 1,
                 "B": 3,
                 "C": 3,
                 "D": 2,
                 "E": 1,
                 "F": 4,
                 "G": 2,
                 "H": 4,
                 "I": 1,
                 "J": 1,
                 "K": 5,
                 "L": 1,
                 "M": 3,
                 "N": 1,
                 "O": 1,
                 "P": 3,
                 "Q": 10,
                 "R": 1,
                 "S": 1,
                 "T": 1,
                 "U": 1,
                 "V": 4,
                 "W": 4,
                 "X": 8,
                 "Y": 4,
                 "Z": 10,
                 "#": 0}

class Board:
    """
    Creer le plateau de scrabble.
    """
    def __init__(self):
        #Crée une liste 2-dimensionnelle qui agit comme plateau de scrabble, ainsi que des ajouts dans les cases bonus. 
        self.board = [["   " for i in range(15)] for j in range(15)]
        self.add_premium_squares()
        self.board[7][7] = " * "

    def get_board(self):
        #Retourne le plateau en forme textuelle
        board_str = "   |  " + "  |  ".join(str(item) for item in range(10)) + "  | " + "  | ".join(str(item) for item in range(10, 15)) + " |"
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        board = list(self.board)
        for i in range(len(board)):
            if i < 10:
                board[i] = str(i) + "  | " + " | ".join(str(item) for item in board[i]) + " |"
            if i >= 10:
                board[i] = str(i) + " | " + " | ".join(str(item) for item in board[i]) + " |"
        board_str += "\n   |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|\n".join(board)
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"
        return board_str

    def add_premium_squares(self):
        #Ajoute toutes les cases bonus qui influencent le score du mot.
        cases_MT = ((0,0), (7, 0), (14,0), (0, 7), (14, 7), (0, 14), (7, 14), (14,14))
        cases_MD = ((1,1), (2,2), (3,3), (4,4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4), (13,13), (12, 12), (11,11), (10,10))
        cases_LT = ((1,5), (1, 9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13, 5), (13,9))
        cases_LD = ((0, 3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8, 12), (11,0), (11,7), (11,14), (12,6), (12,8), (14, 3), (14, 11))

        for coordinate in cases_MT:
            self.board[coordinate[0]][coordinate[1]] = "MT"
        for coordinate in cases_MD:
            self.board[coordinate[0]][coordinate[1]] = "LT"
        for coordinate in cases_LT:
            self.board[coordinate[0]][coordinate[1]] = "WD"
        for coordinate in cases_LD:
            self.board[coordinate[0]][coordinate[1]] = "LD"

    def place_word(self, word, location, direction, player):
        #Vous permet de jouer des mots, en supposant qu'ils ont déjà été confirmés comme valides.

        global premium_spots
        premium_spots = []
        direction = direction.lower()
        word = word.upper()

        #Place le mot vers la droite
        if direction.lower() == "right":
            for i in range(len(word)):
                if self.board[location[0]][location[1]+i] != "   ":
                    premium_spots.append((word[i], self.board[location[0]][location[1]+i]))
                self.board[location[0]][location[1]+i] = " " + word[i] + " "

        #Place le mot vers le bas
        elif direction.lower() == "down":
            for i in range(len(word)):
                if self.board[location[0]][location[1]+i] != "   ":
                    premium_spots.append((word[i], self.board[location[0]][location[1]+i]))
                self.board[location[0]+i][location[1]] = " " + word[i] + " "

        #Supprime les jetons de la main du joueur et les remplace par des jetons du sac.
        for letter in word:
            for tile in player.get_rack_arr():
                if tile.get_letter() == letter:
                    player.rack.remove_from_rack(tile)
        player.rack.replenish_rack()

    def board_array(self):
        #Retourne le plateau comme une liste 2-dimensionnelle.
        return self.board


class Tile:
    """
    Classe qui permet la création d'un jeton. Initialise à l'aide d'une chaîne majuscule d'une lettre,
    et un entier représentant le score de cette lettre.
    """
    def __init__(self, letter, letter_values):
        #Initialise la classe de jetons. Prend la lettre sous forme de chaîne et le dictionnaire des valeurs de lettre comme arguments.
        self.letter = letter.upper()
        if self.letter in letter_values:
            self.score = letter_values[self.letter]
        else:
            self.score = 0

    def get_letter(self):
        #Retourne la lettre du jeton (string).
        return self.letter

    def get_score(self):
        #Retourne le score du jeton.
        return self.score

class Bag:
    """
    Crée le sac de tous les jetons qui seront disponibles pendant le jeu. Contient 98 lettres and deux jetons joker.
    Ne prend aucun argument pour initialiser.
    """
    def __init__(self):
        #Crée le sac plein de jetons de jeu et appelle la méthode initialize_bag (), qui ajoute les 100 jetons par défaut au sac.
        #Ne prend aucun argument

        self.bag = []
        self.initialize_bag()

    def add_to_bag(self, tile, quantity):
        #Ajoute une certaine quantité d'un jeton spécifique. Prend comme argument un jeton et une quantité entière. 
        for i in range(quantity):
            self.bag.append(tile)

    def initialize_bag(self):
        #Ajoute les 100 valeurs initiales à la pioche.
        global LETTER_VALUES
        self.add_to_bag(Tile("A", LETTER_VALUES), 9)
        self.add_to_bag(Tile("B", LETTER_VALUES), 2)
        self.add_to_bag(Tile("C", LETTER_VALUES), 2)
        self.add_to_bag(Tile("D", LETTER_VALUES), 4)
        self.add_to_bag(Tile("E", LETTER_VALUES), 12)
        self.add_to_bag(Tile("F", LETTER_VALUES), 2)
        self.add_to_bag(Tile("G", LETTER_VALUES), 3)
        self.add_to_bag(Tile("H", LETTER_VALUES), 2)
        self.add_to_bag(Tile("I", LETTER_VALUES), 9)
        self.add_to_bag(Tile("J", LETTER_VALUES), 9)
        self.add_to_bag(Tile("K", LETTER_VALUES), 1)
        self.add_to_bag(Tile("L", LETTER_VALUES), 4)
        self.add_to_bag(Tile("M", LETTER_VALUES), 2)
        self.add_to_bag(Tile("N", LETTER_VALUES), 6)
        self.add_to_bag(Tile("O", LETTER_VALUES), 8)
        self.add_to_bag(Tile("P", LETTER_VALUES), 2)
        self.add_to_bag(Tile("Q", LETTER_VALUES), 1)
        self.add_to_bag(Tile("R", LETTER_VALUES), 6)
        self.add_to_bag(Tile("S", LETTER_VALUES), 4)
        self.add_to_bag(Tile("T", LETTER_VALUES), 6)
        self.add_to_bag(Tile("U", LETTER_VALUES), 4)
        self.add_to_bag(Tile("V", LETTER_VALUES), 2)
        self.add_to_bag(Tile("W", LETTER_VALUES), 2)
        self.add_to_bag(Tile("X", LETTER_VALUES), 1)
        self.add_to_bag(Tile("Y", LETTER_VALUES), 2)
        self.add_to_bag(Tile("Z", LETTER_VALUES), 1)
        self.add_to_bag(Tile("?", LETTER_VALUES), 2)
        shuffle(self.bag)

    def take_from_bag(self):
        #Supprime un jeton du sac et la renvoie à l'utilisateur. Ceci est utilisé pour réapprovisionner la main.
        return self.bag.pop()

    def get_remaining_tiles(self):
        #Retourne le nombre de jetons restant dans le sac
        return len(self.bag)
    

class Rack:
    """
    Creer la main du joueur. Permet aux joueurs d'ajouter, de supprimer et de reconstituer le nombre de jetons dans leur main.
    """
    def __init__(self, bag):
        #Initialise la main du joueur. Prend comme argument le sac d'où vient les jetons.
        self.rack = []
        self.bag = bag
        self.initialize()

    def add_to_rack(self):
        #Prend un jeton du sac et l'ajoute a la main du joueur.
        self.rack.append(self.bag.take_from_bag())

    def initialize(self):
        #Ajoute les 7 premiers jetons dans la main du joueur.
        for i in range(7):
            self.add_to_rack()

    def get_rack_str(self):
        #Affiche la main du joueur
        return ", ".join(str(item.get_letter()) for item in self.rack)

    def get_rack_arr(self):
        #Retourne la main comme une liste d'instances de jetons
        return self.rack

    def remove_from_rack(self, tile):
        #Supprime un jeton de la main (par exemple, lorsqu'un jeton est en cours de lecture).

        self.rack.remove(tile)

    def get_rack_length(self):
        #Renvoie le nombre de jetons restants dans la main.
        return len(self.rack)

    def replenish_rack(self):
        #Ajoute des jetons a la main du joueur pour maintenir les 7 jetons dans la main du joueur (en supposant un nombre approprié de jetons dans le sac).
        while self.get_rack_length() < 7 and self.bag.get_remaining_tiles() > 0:
            self.add_to_rack()

f = open("dictionnaire.txt").read().splitlines()
dictionary = "list1"

class Word:
    def __init__(self, word, location, player, direction, board):
        self.word = word.upper()
        self.location = location
        self.player = player
        self.direction = direction.lower()
        self.board = board

    def check_word(self):
        #Vérifie le mot pour s'assurer qu'il est dans le dictionnaire et que l'emplacement est compris dans les limites.
        #Contrôle également la superposition des mots.
        global round_number, players
        word_score = 0
        global dictionary 
        if dictionary not in globals():
            f = open("dictionnaire.txt").read().splitlines()
            dictionnary = "list1"

        current_board_ltr = ""
        needed_tiles = ""
        blank_tile_val = ""

        #En supposant que le joueur ne saute pas le tour:
        if self.word != "":

            #Permet aux joueurs de déclarer la valeur d'un jeton vierge.
            if "?" in self.word:
                while len(blank_tile_val) != 1:
                    blank_tile_val = input("Veuillez saisir la lettre que représente le joker: ")
                self.word = self.word[:word.index("?")] + blank_tile_val.upper() + self.word[(word.index("?")+1):]

            #Lit les valeurs actuelles du tableau sous l'endroit où le mot en cours de lecture ira. Déclenche une erreur si la direction n'est pas valide.
            if self.direction == "right":
                for i in range(len(self.word)):
                    if ((self.board[self.location[0]][self.location[1]+i][1] == " ") or (self.board[self.location[0]][self.location[1]+i] == "LT") or (self.board[self.location[0]][self.location[1]+i] == "MT") or (self.board[self.location[0]][self.location[1]+i] == "LD") or (self.board[self.location[0]][self.location[1]+i] == "MD") or (self.board[self.location[0]][self.location[1]+i][1] == "*")):
                        current_board_ltr += " "
                    else:
                        current_board_ltr += self.board[self.location[0]][self.location[1]+i][1]
            elif self.direction == "down":
                for i in range(len(self.word)):
                    if ((self.board[self.location[0]+i][self.location[1]] == " ") or (self.board[self.location[0]+i][self.location[1]] == "LT") or (self.board[self.location[0]+i][self.location[1]] == "MT") or (self.board[self.location[0]+i][self.location[1]] == "LD") or (self.board[self.location[0]+i][self.location[1]] == "MD") or (self.board[self.location[0]+i][self.location[1]] == " * ")):
                        current_board_ltr += " "
                    else:
                        current_board_ltr += self.board[self.location[0]+i][self.location[1]][1]
            else:
                return "Erreur: veuillez entrer une direction valide."

            #Déclenche une erreur si le mot en cours de lecture n'est pas dans le dictionnaire officiel du scrabble (dictionnaire.txt).
            if self.word in dictionary:
                return "Veuillez saisir un mot de dictionnaire valide.\n"

            #S'assure que les mots se superposent correctement. S'il y a des lettres en conflit entre le plateau actuel et le mot en cours de lecture, génère une erreur.
            for i in range(len(self.word)):
                if current_board_ltr[i] == " ":
                    needed_tiles += self.word[i]
                elif current_board_ltr[i] != self.word[i]:
                    print("Current_board_ltr: " + str(current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                    return "Les lettres ne se superposent pas correctement, choisissez un autre mot."

            #S'il y a un jeton vierge, supprime sa valeur donnée des jetons nécessaires pour jouer le mot.
            if blank_tile_val != "":
                needed_tiles = needed_tiles[needed_tiles.index(blank_tile_val):] + needed_tiles[:needed_tiles.index(blank_tile_val)]

            #S'assure que le mot est bien lié aux autres mots présents sur le plateau.
            if (round_number != 1 or (round_number == 1 and players[0] != self.player)) and current_board_ltr == " " * len(self.word):
                print("Current_board_ltr: " + str(current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                return "Veuillez lier le mot à une lettre précédemment jouée."

            #Déclenche une erreur si le joueur n'a pas les bons jetons pour jouer le mot.
            for letter in needed_tiles:
                if letter not in self.player.get_rack_str() or self.player.get_rack_str().count(letter) < needed_tiles.count(letter):
                    return "Vous n'avez pas de jetons pour ce mot\n"

            #Déclenche une erreur si l'emplacement du mot est hors limites.

            if self.location[0] > 14 or self.location[1] > 14 or self.location[0] < 0 or self.location[1] < 0 or (self.direction == "down" and (self.location[0]+len(self.word)-1) > 14) or (self.direction == "right" and (self.location[1]+len(self.word)-1) > 14):
                return "Emplacement hors limites.\n"

            #S'assure que le premier tour de jeu aura le mot placé à (7,7).
            if round_number == 1 and players[0] == self.player and self.location != [7,7]:
                return "Le premier tour doit commencer à l'emplacement (7, 7).\n"
            return True

        #Si l'utilisateur saute le virage, confirmez. Si l'utilisateur répond par "Y", sautez le tour du joueur. Sinon, autorisez l'utilisateur à entrer un autre mot.
        else:
            if input("Êtes-vous sûr(e) de vouloir sauter votre tour? (y/n) ").upper() == "Y":
                if round_number == 1 and players[0] == self.player:
                    return "Ne sautez pas votre premier tour. Entrez un mot."
                return True
            else:
                return "Entrer un mot."

    def calculate_word_score(self):
        #Calcule le score en mot, en tenant compte des cases bonus.
        global LETTER_VALUES, premium_spots
        word_score = 0
        for letter in self.word:
            for spot in premium_spots:
                if letter == spot[0]:
                    if spot[1] == "LT":
                        word_score += LETTER_VALUES[letter] * 2
                    elif spot[1] == "LD":
                        word_score += LETTER_VALUES[letter]
            word_score += LETTER_VALUES[letter]
        for spot in premium_spots:
            if spot[1] == "MT":
                word_score *= 3
            elif spot[1] == "MD":
                word_score *= 2
        self.player.increase_score(word_score)

    def set_word(self, word):
        self.word = word.upper()

    def set_location(self, location):
        self.location = location

    def set_direction(self, direction):
        self.direction = direction

    def get_word(self):
        return self.word

class Player:
    """
    Crée une instance d'un joueur. Initialise la main du lecteur et vous permet de définir / obtenir un nom de joueur.
    """
    def __init__(self, bag):
        #Initialise une instance de joueur. Crée la main du joueur en créant une instance de cette classe.

        #Prend le sac comme argument, afin de créer la main.
        self.name = ""
        self.rack = Rack(bag)
        self.score = 0

    def set_name(self, name):
        #Etablit le nom du joueur.
        self.name = name

    def get_name(self):
        #Obtient le nom du joueur.
        return self.name

    def get_rack_str(self):
        #Renvoie la pioche du joueur.
        return self.rack.get_rack_str()

    def get_rack_arr(self):
        #Retourne le rack du joueur sous la forme de la liste.
        return self.rack.get_rack_arr()

    def increase_score(self, increase):
        #Augmente le score du joueur d'un certain montant. Prend l'augmentation (int) comme argument et l'ajoute au score.
        self.score += increase

    def get_score(self):
        #Renvoie le score du joueur
        return self.score



def turn(player, board, bag):
    #Commence un tour, en affichant le plateau actuel, en obtenant les informations pour jouer un tour et en créant une boucle récursive pour permettre à la personne suivante de jouer.
    global round_number, players, skipped_turns

    #Si le nombre de tours sautés est inférieur à 6, et qu'il y a des jetons dans le sac, ou qu'un des joueurs a encore des jetons, jouez le tour.

    #Sinon, terminez le jeu.
    if (skipped_turns < 6) or (player.rack.get_rack_length() == 0 and bag.get_remaining_tiles() == 0):

        #Affiche à qui appartient le tour, le plateau actuel et la pioche du joueur.

        print("\nRound " + str(round_number) + ": " + player.get_name() + "'s turn \n")
        print(board.get_board())
        print("\n" + player.get_name() + "'s Letter Rack: " + player.get_rack_str())

        #Obtient des informations pour jouer un mot.

        word_to_play = input("Mot a jouer: ")
        location = []
        col = input("Numero de colonne: ")
        row = input("Numéro de ligne: ")
        if (col == "" or row == "") or (col not in [str(x) for x in range(15)] or row not in [str(x) for x in range(15)]):
            location = [-1, -1]
        else:
            location = [int(row), int(col)]
        direction = input("Direction du mot (right or down): ")

        word = Word(word_to_play, location, player, direction, board.board_array())

        #Si le premier mot renvoie une erreur, crée une boucle récursive jusqu'à ce que les informations soient fournies correctement.
        checked = word.check_word()
        while checked != True:
            print(checked)
            word_to_play = input("Mot a jouer: ")
            word.set_word(word_to_play)
            location = []
            col = input("Numero de colonne: ")
            row = input("Numéro de ligne: ")
            if (col == "" or row == "") or (col not in [str(x) for x in range(15)] or row not in [str(x) for x in range(15)]):
                location = [-1, -1]
            else:
                word.set_location([int(row), int(col)])
                location = [int(row), int(col)]
            direction = input("Direction du mot (right or down): ")
            word.set_direction(direction)
            checked = word.check_word()

        #Si l'utilisateur a confirmé qu'il aimerait sauter son tour, ignorez-le.
        #Sinon, lit le mot correct et imprime le plateau.

        if word.get_word() == "":
            print("Votre tour a été sauté.")
            skipped_turns += 1
        else:
            board.place_word(word_to_play, location, direction, player)
            word.calculate_word_score()
            skipped_turns = 0

        #Imprime le score du joueur actuel
        print("\n" + player.get_name() + "'s score is: " + str(player.get_score()))

        #Obtient le joueur suivant.
        if players.index(player) != (len(players)-1):
            player = players[players.index(player)+1]
        else:
            player = players[0]
            round_number += 1

        #Appelle la fonction de manière récursive pour jouer le tour suivant.
        turn(player, board, bag)

    #Si le nombre de tours sautés est supérieur à 6, ou qu'il n'y a plus de jetons dans le sac et qu'un des deux joueurs n'a plus de jetons, finit le jeu.

    else:
        end_game()

def start_game():
    #Démarre le jeu et appelle la fonction turn.
    global round_number, players, skipped_turns
    board = Board()
    bag = Bag()

    #Demande au joueur le nombre de joueurs.
    num_of_players = int(input("\nEntrez le nombre de joueurs (2-4): "))
    while num_of_players < 2 or num_of_players > 4:
        num_of_players = int(input("Ce nombre est invalide. Veuillez entrer le nombre de joueurs (2-4): "))

    #Accueille les joueurs dans le jeu et permet aux joueurs de choisir leur nom.
    print("\nBienvenue à Scrabble! Entrez ci-dessous les noms des joueurs.")
    players = []
    for i in range(num_of_players):
        players.append(Player(bag))
        players[i].set_name(input("Joueur " + str(i+1) + "nom: "))

    #Définit la valeur par défaut des variables globales.
    round_number = 1
    skipped_turns = 0
    current_player = players[0]
    turn(current_player, board, bag)

def end_game():
    #Force le jeu à se terminer lorsque le sac est à court de jetons.
    global players
    highest_score = 0
    winning_player = ""
    for player in players:
        if player.get_score > highest_score:
            highest_score = player.get_score()
            winning_player = player.get_name()
    print("La partie est terminée! " + winning_player + ", vous avez gagné!")

    if input("\nVoulez vous rejouer? (y/n)").upper() == "Y":
        start_game()

start_game()

