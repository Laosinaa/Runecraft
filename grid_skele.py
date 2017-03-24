"""
Game: Runecraft.

Terje Russka
"""


import tkinter as tk
from PIL import Image, ImageTk
import random
import threading
import sys
from tkinter import ttk
import winsound


class Runes:
    """Elementide class."""

    all_types = [
        "Fire", "Nature", "Law", "Blood",
        "Water", "Air", "Mind", "Chaos",
        "Soul", "Body", "Cosmic", "Essence"
    ]

    def __init__(self, name):
        """
        Annab elenedile classi, rünnakud ja nõrkused.

        :param name: Elemendi ID, mis saadakse mängu alustamisel
        """
        self.attacks = []
        self.weaknesses = []
        self.type = ''
        self.id = name

    def give_type(self):
        """
        Genereerib elemendile suvalise classi ja sellele vastavad atribuudid.

        :return:
        """
        self.type = Runes.all_types[random.randrange(len(Runes.all_types))]
        if "Essence" in Player.current_runes or "Essence" in Computer.current_runes:
            while self.type == "Essence":  # Essence elementi võib nii arvutil kui ka mängijal olla vaid üks
                self.type = Runes.all_types[random.randrange(len(Runes.all_types))]
        self.type_attack()
        self.type_weakness()

    def check_type(self):
        """
        Tagastab valitud elemendi classi.

        :return: Elemendi class
        """
        return self.type

    def rune_ID(self):
        """
        Tagastab elemendi ID.

        :return: Elemendi ID
        """
        return self.id

    def give_attacks(self, attack_index):
        """
        Annab elemendile rünnakud.

        :param attack_index: Milliste elementide indeksid saab rünnata.
        :return:
        """
        for i in attack_index:
            self.attacks.append(Runes.all_types[i])

    def give_weaknesses(self, weakness_index):
        """
        Annnab elemnedile nõrkusi.

        :param weakness_index: Millised elemendid on nõrkuseks
        :return:
        """
        for i in weakness_index:
            self.attacks.append(Runes.all_types[i])

    def reset_attacks(self):
        """
        Taastab antud elemendi rünnakud algseisu.

        :return:
        """
        self.attacks = []
        self.type_attack()

    def reset_weaknesses(self):
        """
        Taastab antud elemendi nõrkused algseisu.

        :return:
        """
        self.weaknesses = []
        self.type_weakness()

    def type_weakness(self):
        """
        Leiab vastavalt genereeitud elemendi classile tema atribuudid.

        :return:
        """
        weakness_dict = {
            "Fire": [1, 2, 3, 4, 5],
            "Nature": [2, 3, 4, 5, 6],
            "Law": [2, 3, 4, 5, 6],
            "Blood": [4, 5, 6, 7, 8],
            "Water": [5, 6, 7, 8, 9],
            "Air": [6, 7, 8, 9, 10],
            "Mind": [7, 8, 9, 10, 0],
            "Chaos": [8, 9, 10, 0, 1],
            "Soul": [9, 10, 0, 1, 2],
            "Body": [10, 0, 1, 2, 3],
            "Cosmic": [0, 1, 2, 3, 4],
            "Essence": []
        }
        weakness_index = weakness_dict[self.type]
        for i in weakness_index:
            self.weaknesses.append(Runes.all_types[i])

    def type_attack(self):
        """
        Leiab vastavalt genereeitud elemendi classile tema atribuudid.

        :return:
        """
        attack_dict = {
            "Fire": [6, 7, 8, 9, 10],
            "Nature": [7, 8, 9, 10, 0],
            "Law": [8, 9, 10, 0, 1],
            "Blood": [9, 10, 0, 1, 2],
            "Water": [10, 0, 1, 2, 3],
            "Air": [0, 1, 2, 3, 4],
            "Mind": [1, 2, 3, 4, 5],
            "Chaos": [2, 3, 4, 5, 6],
            "Soul": [3, 4, 5, 6, 7],
            "Body": [4, 5, 6, 7, 8],
            "Cosmic": [5, 6, 7, 8, 9],
            "Essence": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }
        attack_index = attack_dict[self.type]
        for i in attack_index:
            self.attacks.append(Runes.all_types[i])


class Environment:
    """Keskkondade class."""

    all_environments = ["Fire_env", "Earth_env", "Water_env", "Cosmic_env"]

    def __init__(self, name):
        """
        Loob keskonnale suvalise tüübi ja ID.

        :param name: Keskkonna ID, mis saadakse mängu alustamisel
        """
        self.environment = Environment.all_environments[random.randrange(len(Environment.all_environments))]
        self.id = name

    def power_ups(self, dict_run):
        """
        Vastavalt keskkonna tüübile saavad vastavad elemendid tugevamaks kui tavaliselt.

        :param dict_run: Mängu alguses genereeritud elemendid
        :return:
        """
        runeID = dict_run.keys()  # Võtab mängu elemnedid
        runeID = list(runeID)
        for rune in runeID:  # Taastab elementide võimed algseisu
            dict_run[rune].reset_attacks()
            dict_run[rune].reset_weaknesses()
        if self.environment == "Fire_env":
            self.env_attack(runeID, dict_run, "Fire", "Blood", "Chaos")
        elif self.environment == "Earth_env":
            self.env_attack(runeID, dict_run, "Nature", "Law", "")
            self.env_immune(runeID, dict_run, "Nature", "Law", "")
        elif self.environment == "Water_env":
            self.env_immune(runeID, dict_run, "Water", "Air", "Body")
        elif self.environment == "Cosmic_env":
            self.env_immune(runeID, dict_run, "Soul", "Mind", "Cosmic")

    @staticmethod
    def env_attack(runeID, dict_run, rune1, rune2, rune3):
        """
        Olenevalt keskonnale annab teatud elementidele lisa rünnakuid.

        :param runeID: Võtab mängu elemnedid, nende ID-d
        :param dict_run: Mängu alguses genereeritud elemendid
        :param rune1: Mõjutatav element
        :param rune2: Mõjutatav element
        :param rune3: Mõjutatav element
        :return:
        """
        for rune in runeID:
            if dict_run[rune].check_type() in (rune1, rune2, rune3):
                attack_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                dict_run[rune].attacks = []
                for i in attack_index:
                    dict_run[rune].attacks.append(Runes.all_types[i])

    @staticmethod
    def env_immune(runeID, dict_run, rune1, rune2, rune3):
        """
        Olenevalt keskonnale annab teatud elementidele immuunsuse.

        :param runeID: Võtab mängu elemnedid, nende ID-d
        :param dict_run: Mängu alguses genereeritud elemendid
        :param rune1: Mõjutatav element
        :param rune2: Mõjutatav element
        :param rune3: Mõjutatav element
        :return:
        """
        for rune in runeID:
            if dict_run[rune].check_type() in (rune1, rune2, rune3):
                dict_run[rune].weaknesses = []

    def environment_check(self):
        """
        Kontrollib keskkonna tüüpi.

        :return: Keskkonna tüüp
        """
        return self.environment

    def environment_id(self):
        """
        Kontrollib keskonna ID-d.

        :return: Keskkonna ID
        """
        return self.id


class Player:
    """Kasutaja class."""

    current_runes = []
    rune_IDs = []

    def __init__(self):
        """Kasutajale antakse score."""
        self.score = 0

    def add_score(self):
        """
        Lisatakse punkt juurde.

        :return:
        """
        self.score += 1

    @staticmethod
    def chose_rune():
        """
        Kasutaja valib mängus elemendi.

        :return: Valitud element
        """
        chosen_rune = Window.chosen_rune
        while chosen_rune == "None":
            chosen_rune = Window.chosen_rune  # Ootab Kuna kasutaja klõpsab elemendile
        Player.rune_IDs.remove(chosen_rune)  # Eemaldab valitud elemendi kasutaja elementidest
        Window.chosen_rune = "None"
        return chosen_rune

    def final_score(self):
        """
        Tagastab kasutaja lõpptulemuse.

        :return: Lõpptulemus
        """
        return self.score


class Computer:
    """Arvut class."""

    current_runes = []
    rune_IDs = []

    def __init__(self):
        """Loob aruvtile score-i."""
        self.score = 0

    def add_score(self):
        """
        Arvutile lisatakse punkt.

        :return:
        """
        self.score += 1

    @staticmethod
    def chose_rune():
        """
        Arvuti valib suvalise elemendi.

        :return: Valitud element
        """
        chosen_rune = Computer.rune_IDs[random.randrange(len(Computer.rune_IDs))]
        Computer.rune_IDs.remove(chosen_rune)  # Valitud element eemaldataske arvuti elementidest
        return chosen_rune

    def final_score(self):
        """
        Tagastab arvuti lõpputulemuse.

        :return: Lõpptulemus
        """
        return self.score


class Battle:
    """Battle class."""

    def __init__(self, dict_run):
        """
        Loob raundi numbrid ja kasutatavad elemendid.

        :param dict_run: Mängu elemendid
        """
        self.round = 0
        self.runeID = dict_run.keys()
        self.runeID = list(self.runeID)
        self.dict_run = dict_run

    def round_check(self, user, comp):
        """
        Kontrollib kes võitis roundi.

        :param user: viide kasutaja classile
        :param comp: viide arvuti classile
        :return:
        """
        score_comp = 0  # Punktide arvestus mis määrab roundi võidu
        score_player = 0
        player = user.chose_rune()  # Kasutaja valib elemendi, saab elemendi ID
        computer = comp.chose_rune()  # Arvuti valib elemendi, saab elemendi ID
        comp_run = self.dict_run[computer].check_type()  # Elemendi nimi
        player_run = self.dict_run[player].check_type()
        comp_atk = self.dict_run[computer].attacks  # Elemendi tugevused
        player_atk = self.dict_run[player].attacks
        comp_weak = self.dict_run[computer].weaknesses  # Elemendi nõrkused
        player_weak = self.dict_run[player].weaknesses
        if comp_run in player_weak:
            score_comp += 1
        if player_run in comp_atk:
            if player_weak != []:
                score_comp += 1
        if player_run in comp_weak:
            score_player += 1
        if comp_run in player_atk:
            if comp_weak != []:
                score_player += 1
        if score_comp > score_player:
            comp.add_score()
        elif score_player == score_comp:
            comp.add_score()
            user.add_score()
        else:
            user.add_score()

        self.round += 1


def game_runes(player, computer, nr):
    """
    Genereerib mängu jaoks nii kasutajale kui ka arvutile 20 elementi.

    :param player: Viide Player classile
    :param computer: Viide arvuti classile
    :param nr: Mitu elementi genereeritakse
    :return: Mängu elementide dictionary
    """
    rune_list = []
    for i in range(nr):  # Loob listid , kus on teadud arv elmemtide ID
        name = "rune" + str(i)
        rune_list.append(name)
    dict_run = {}
    counter = 1
    for name in rune_list:
        dict_run[name] = Runes(name)  # Lisab ID koos classiga dictionarisse
        dict_run[name].give_type()  # Annab ID elemendile tüübi
        if counter % 2 == 0:  # Elemendid jagatakse arvuti ja kasutaja vahel ära
            computer.rune_IDs.append(dict_run[name].rune_ID())  # Arvuti elementide listi lisatakse elemendi ID
            computer.current_runes.append(dict_run[name].check_type())
            counter += 1
        else:
            player.rune_IDs.append(dict_run[name].rune_ID())
            player.current_runes.append(dict_run[name].check_type())
            counter += 1
    return dict_run


def game_environments(nr):
    """
    Genereerib mängu jaoks random keskkonnad.

    :param nr: Mitu keskkonda genereeritakse
    :return: Keskkondade dictionary
    """
    env_list = []
    for i in range(nr):  # Loob listi keskkondade ID
        name = "env" + str(i)
        env_list.append(name)
    dict_env = {}
    for name in env_list:  # Annab dictionaris ID-le classi
        dict_env[name] = Environment(name)

    return dict_env


class Window(tk.Toplevel):
    """Window class."""

    chosen_rune = "None"

    def __init__(self, player, dict_run, env, computer):
        """
        Loob mänguakna, kus kasutaja saab valida elemente.

        :param player: Viide Player classile
        :param dict_run: Mängule genereeritud elemendid
        :param env: Keskkond
        :param computer: Viide Computer classile
        """
        tk.Toplevel.__init__(self)
        self.container = tk.Frame(self)
        w = 1024
        h = 768
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 30
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(width=False, height=False)

        load = Image.open('Style\{}.gif'.format(env.environment_check()))
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        load2 = Image.open('Style\Trps11tiny.gif')
        render2 = ImageTk.PhotoImage(load2)
        img2 = tk.Label(self, image=render2)
        img2.image = render2
        img2.place(x=780, y=10)

        comp_score = tk.Text(self, width=11, height=1, font=("system", 20))
        comp_score.insert(tk.END, "Computer: " + str(computer.score))
        comp_score.config(state=tk.DISABLED)
        comp_score.place(relx=0.6, rely=0.2, anchor=tk.CENTER)
        user_score = tk.Text(self, width=11, height=1, font=("system", 20))
        user_score.insert(tk.END, "Player: " + str(player.score))
        user_score.config(state=tk.DISABLED)
        user_score.place(relx=0.3, rely=0.2, anchor=tk.CENTER)

        user_runes = player.rune_IDs  # Kasutajale antud elementide ID-d
        ind = 0
        grid = []
        for r in range(4):
            for c in range(5):
                grid.append([r, c])  # Loob listi koordinaatidega, mida kastuada elementide nuppude paigutamiseks

        container = ttk.Frame(self)
        container.pack(side="top", expand=True)

        quit = ImageTk.PhotoImage(file="Style\Quit.png")
        button4 = ttk.Button(self, text="Quit", image=quit, command=lambda: self.chosen("Quit"))
        button4.image = quit
        button4.place(x=0, y=0)

        for rune_nr in user_runes:
            if dict_run[rune_nr].check_type() == "Nature":
                img = ImageTk.PhotoImage(file="Runes\Ature.png")
            else:
                img = ImageTk.PhotoImage(file="Runes\{}.png".format(dict_run[rune_nr].check_type()))
            rune_nr = tk.Button(
                container, image=img, text=dict_run[rune_nr].check_type(), width=130,
                command=lambda rune=rune_nr: self.chosen(rune))
            rune_nr.image = img
            grid_rune = grid[ind]
            rune_nr.place(x=100, y=100)
            rune_nr.grid(row=grid_rune[0], column=grid_rune[1])
            ind += 1

        self.operation()
        self.withdraw()  # Peidab akna

    def operation(self):
        """
        Ootab kasutaja valikut.

        :return:
        """
        while self.chosen_rune == "None" or self.chosen_rune == "Quit":
            if self.chosen_rune == "Quit":
                sys.exit()
            self.after(1, self.update())

    @staticmethod
    def chosen(chosen_rune):
        """
        Muudab valitud elemendi nupu None- is vastavaks nimeks.

        :param chosen_rune: Valitud element, nupp
        :return:
        """
        Window.chosen_rune = chosen_rune


def main():
    """
    Mängu põhifunktsioon, mis käivitab aknad ja genereerib mängu olukorrad.

    :return: Kas mäng võidetud või kaotatud.
    """
    player = Player()  # Käivitab kasutaja classi
    computer = Computer()  # Käivitab arvuti classi
    dict_run = game_runes(player, computer, 40)  # Loob mängu jaoks elemendid
    dict_env = game_environments(5)  # Loon mängu jaoks keskkonnad
    env_list = dict_env.keys()  # Keskkondade ID list
    env_list = list(env_list)
    env = env_list[random.randrange(len(env_list))]  # Random keskkond, selle nimi
    winsound.PlaySound('Music\{}.wav'.format(dict_env[env].environment_check()), winsound.SND_ASYNC)
    dict_env[env].power_ups(dict_run)  # Keskonnale vastav power-ups, pilt ja heli
    battle = Battle(dict_run)  # Alustab esimese roundi
    for i in range(20):
        app = Window(player, dict_run, dict_env[env], computer)
        th = threading.Thread(target=app, args=(player, computer, dict_run, dict_env[env], battle))
        th.start()  # Käivitab akna nii, et kood jooksesk veel edasi
        battle.round_check(player, computer)  # Kontrillib kes võitis roundi
        if battle.round % 5 == 0 and battle.round != 20:  # Keskkond muutub viie roundi pärast
            env2 = env_list[random.randrange(len(env_list))]  # Uus random keskkond
            if dict_env[env].environment_check() != dict_env[env2].environment_check():  # Kui ei ole sama
                winsound.PlaySound('Music\{}.wav'.format(dict_env[env2].environment_check()), winsound.SND_ASYNC)
                dict_env[env2].power_ups(dict_run)
                env = env2
            else:
                dict_env[env2].power_ups(dict_run)
                env = env2

    text = open("data.txt", "a")
    text.writelines("{0} {1}\n".format(str(computer.score), str(player.score)))
    if computer.score > player.score:
        return False
    else:
        return True
