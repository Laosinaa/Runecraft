"""
Game: Runecraft.

Terje Russka
"""


import tkinter as tk
from PIL import Image, ImageTk
import winsound
from Game import grid_skele
from tkinter import ttk


class Window(tk.Tk):
    """Window class."""

    def __init__(self):
        """Annab peaaknale suuruse, asukoha, frame-id."""
        tk.Tk.__init__(self)  # Et aknad saaksid avaneda, peavad funkstiooni saama TK-st
        tk.Tk.iconbitmap(self, default="favicon.ico")  # Loob aknale ikooni
        tk.Tk.wm_title(self, "RUNECRAFT")  # Loob aknale nime

        self.container = tk.Frame(self)  # Ala, kuhu pannakse kõik frame-id
        w = 1024  # Akna laius
        h = 768   # Akna pikkus
        ws = self.winfo_screenwidth()  # Leiab arvutiekraani laiuse
        hs = self.winfo_screenheight()  # Leiab arvutierkaani pikkuse
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 30
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))  # Paigutab akna ekraani keskele
        self.resizable(width=False, height=False)  # Akna suurust ei ole võimalik muuta
        self.container.pack(side="top", fill="both", expand=True)  # Frame-ide ala täidab terve ekraani

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Frame-ide dictionary

        for F in (Home, Tutorial, Winner, Loser):  # Laeb kõik frame-id juba aknasse.
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home)  # Tõstab ette kodu frame-i

    def show_frame(self, cont):
        """
        Tõstab ette valitud akna ja muudab muusika.

        :param cont: Kasutaja poolt valitud frame, controller
        :return:
        """
        if cont == Tutorial:
            winsound.PlaySound('Music\Camelot.wav', winsound.SND_ASYNC)
            frame = self.frames[cont]
            frame.tkraise()
        elif cont == Winner:
            frame = self.frames[cont]
            frame.tkraise()
        elif cont == Loser:
            frame = self.frames[cont]
            frame.tkraise()
        elif cont == Score:  # Score frame-i enne ei lae kui seda küsitakse, sest ta peab tulemusi uuendama
            winsound.PlaySound('Music\Venture.wav', winsound.SND_ASYNC)
            frame = Score(self.container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()
        else:
            winsound.PlaySound('Music\Home Sweet Home.wav', winsound.SND_ASYNC)
            frame = self.frames[cont]
            frame.tkraise()


class Home(tk.Frame):
    """Kodulehe class."""

    def __init__(self, parent, controller):
        """
        Loob Home frame-i, mis pannakse Window classi.

        :param parent: Viitab Window classile, kuhu Home frame pannakse
        :param controller: Kõik aknad mida kasutaja valida saab
        """
        tk.Frame.__init__(self, parent)  # Asjad tekivad Frame-i, mis omakorda liigub parenti.

        load = Image.open('Style\Main.png')
        render = ImageTk.PhotoImage(load)  # Laeb Home frame-i taustapildi
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        tut = ImageTk.PhotoImage(file="Style\TutorialB.png")  # Loob vajalikud nupud
        button = ttk.Button(
            self, text="Tutorial", image=tut,
            command=lambda: controller.show_frame(Tutorial))
        button.image = tut
        button.place(relx=0.5, rely=0.54, anchor=tk.CENTER)

        play = ImageTk.PhotoImage(file="Style\playnow.png")
        button2 = ttk.Button(self, image=play, command=game_start)
        button2.image = play
        button2.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        score = ImageTk.PhotoImage(file="Style\ScoreB.png")
        button3 = ttk.Button(
            self, text="Score", image=score,
            command=lambda: controller.show_frame(Score))
        button3.image = score
        button3.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        quit = ImageTk.PhotoImage(file="Style\Quit.png")
        button4 = ttk.Button(self, image=quit, text="Quit", command=exit)
        button4.image = quit
        button4.place(x=0, y=0)


def game_start():
    """
    Alustab mängu.

    :return: True või False, võit või kaotus
    """
    app.withdraw()  # Peidab Window classi akna ära
    if grid_skele.main() is True:  # Liigub teise faili ja käivitab mängu
        app.deiconify()  # Toob Window classi akna üles
        app.show_frame(Winner)  # Tõstab võitja frame-i üles
        winsound.PlaySound('Music\Winner.wav', winsound.SND_ASYNC)
    else:
        app.deiconify()
        app.show_frame(Loser)
        winsound.PlaySound('Music\Loser.wav', winsound.SND_ASYNC)


class Tutorial(tk.Frame):
    """Tutoriali class."""

    def __init__(self, parent, controller):
        """
        Loob Tutorial frame-i, mis pannakse Window classi.

        :param parent: Viide Window classile
        :param controller: Kõik aknad mida kasutaja valida saab
        """
        tk.Frame.__init__(self, parent)

        load = Image.open('Style\Tutorial.gif')
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render,)
        img.image = render
        img.place(x=0, y=0)

        load = Image.open('Style\Trps11small.gif')
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=20, y=150)

        quote = """
        ------------RUNECRAFT GAMEPLAY------------

        INSTRUCTIONS:

        Similar to rock-paper-scissors, you will
        randomly be given 20 runes. Each rune has
        5 weaknesses and 5 attack methods. What
        rune types and how many a player gets,
        is randomly generated. There are a total of
        11 different rune Types.

        The rune in the middle, called Pure Essence,
        is a wild-card and can attack any other rune,
        without having any weaknesses. These runes
        are rare and the player may obtain only one
        Pure Essence per game.

        ENVIRONMENT:

        After every 5 turns, the environment of the
        game will be randomly changed. Each environment
        gives certain runes power-ups.

        *Each power-up the environment gives will last
        until the environment changes.

        COSMIC- Runes Soul, Mind and Cosmic become immune.
        WATER- Runes Water, Air and Body become immune.
        FIRE- Runes Fire, Blood and Chaos can attack all.
        EARTH- Runes Nature and Law can attack all and
        become immune.

        Due to the power-ups, if both runes:
        * Have the ability to attack each other, then the battle
        will end in a tie.
        * Are immune to each other, then the battle will end in a tie.
        """
        txt_frame = tk.Frame(self)  # Loob frame-i kirjakasti ja kerimivõimaluse jaoks
        txt_frame.place(x=450, y=100)
        txt_frame.grid_rowconfigure(0, weight=1)
        txt_frame.grid_columnconfigure(0, weight=1)

        self.tut = tk.Text(txt_frame, width=55, height=35, font="system")
        self.tut.insert(tk.END, quote)
        self.tut.config(state=tk.DISABLED)  # Ei saa teksti kastis muuta
        self.tut.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        scroll = tk.Scrollbar(txt_frame, command=self.tut.yview)  # Tekitab kerimisvõimaluse
        scroll.grid(row=0, column=1, sticky='nsew')
        self.tut['yscrollcommand'] = scroll.set

        back = ImageTk.PhotoImage(file="Style\Back.png")
        button1 = ttk.Button(self, image=back, command=lambda: controller.show_frame(Home))
        button1.image = back
        button1.place(relx=0.1, rely=0.15, anchor=tk.W)

        quit = ImageTk.PhotoImage(file="Style\Quit.png")
        button2 = ttk.Button(self, text="Quit", image=quit, command=exit)
        button2.image = quit
        button2.place(x=0, y=0)


class Winner(tk.Frame):
    """Võitja class."""

    def __init__(self, parent, controller):
        """
        Loob Winner frame-i, mis pannakse Window classi.

        :param parent: Viide Window classile
        :param controller: Kõik aknad mida kasutaja valida saab
        """
        tk.Frame.__init__(self, parent)

        load = Image.open('Style\Winner.gif')
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render,)
        img.image = render
        img.place(x=0, y=0)

        quit = ImageTk.PhotoImage(file="Style\Quit.png")
        button2 = ttk.Button(self, text="Quit", image=quit, command=exit)
        button2.image = quit
        button2.place(x=0, y=0)

        score = ImageTk.PhotoImage(file="Style\ScoreB.png")
        button3 = ttk.Button(self, text="Score", image=score,
                             command=lambda: controller.show_frame(Score))
        button3.image = score
        button3.place(relx=0.5, rely=0.65, anchor=tk.CENTER)


class Loser(tk.Frame):
    """Kaotaja class."""

    def __init__(self, parent, controller):
        """
        Loob Loser frame-i, mis pannakse Window classi.

        :param parent: Viide Window classile
        :param controller: Kõik aknad mida kasutaja valida saab
        """
        tk.Frame.__init__(self, parent)

        load = Image.open('Style\Loser.gif')
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render,)
        img.image = render
        img.place(x=0, y=0)

        quit = ImageTk.PhotoImage(file="Style\Quit.png")
        button2 = ttk.Button(self, text="Quit", image=quit, command=exit)
        button2.image = quit
        button2.place(x=0, y=0)

        score = ImageTk.PhotoImage(file="Style\ScoreB.png")
        button3 = ttk.Button(self, text="Score", image=score,
                             command=lambda: controller.show_frame(Score))
        button3.image = score
        button3.place(relx=0.5, rely=0.65, anchor=tk.CENTER)


class Score(tk.Frame):
    """Tulemuste class."""

    def __init__(self, parent, controller):
        """
        Loob Tulemuste frame-i, mis pannakse Window classi.

        :param parent: Viide Window classile
        :param controller: Kõik aknad mida kasutaja valida saab
        """
        tk.Frame.__init__(self, parent)

        load = Image.open('Style\Score.gif')
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        txt_frame = tk.Frame(self)  # Tekitab ekraanile kasti
        txt_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        txt_frame.grid_rowconfigure(0, weight=1)
        txt_frame.grid_columnconfigure(0, weight=1)

        self.tut = tk.Text(txt_frame, width=22, height=13, font=("system", 26))  # Teeb kasti tekstiboxi
        data = Data("data.txt")
        if data.Get_Comp_Stats() != [] and data.Get_User_Stats() != []:
            self.tut.insert(tk.END, "Games played: " + data.Get_Games() + "\n")
            comp = data.Get_Comp_Stats()
            user = data.Get_User_Stats()
            self.tut.insert(tk.END, "{0:<26}{1}".format("Computer", "User") + "\n")  # Lisatakse kasutaja ja arvuti punktid
            for i in range(int(data.Get_Games())):
                self.tut.insert(tk.END, "{0:<33}{1:>5}".format(str(comp[i]), str(user[i])) + "\n")
        else:
            self.tut.insert(tk.END, "Games played: 0" + "\n")
        self.tut.insert(tk.END, """
        1 Battle won
        0 Battle lost
        1-1 Battle tied""")
        self.tut.config(state=tk.DISABLED)  # Ei lase andmeid muuta
        self.tut.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        scroll = tk.Scrollbar(txt_frame, command=self.tut.yview)
        scroll.grid(row=0, column=1, sticky='nsew')
        self.tut['yscrollcommand'] = scroll.set

        back = ImageTk.PhotoImage(file="Style\Back.png")
        button1 = ttk.Button(
            self, text="Back to Home", image=back,
            command=lambda: controller.show_frame(Home))
        button1.image = back
        button1.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        quit = ImageTk.PhotoImage(file="Style\Quit.png")
        button2 = ttk.Button(self, text="Quit", image=quit, command=exit)
        button2.image = quit
        button2.place(x=0, y=0)


class Data:
    """Andmete class."""

    def __init__(self, file):
        """Loeb andmed ja sorteerib."""
        self.text = open(file, "r")
        self.rows = self.text.read().split("\n")
        self.comp = []
        self.user = []
        for i in range(len(self.rows) - 1):
            row = self.rows[i]
            if row != "":
                row = row.split()
                self.comp.append(row[0])
                self.user.append(row[1])

    def Get_Games(self):
        """
        Leiab mitu mängu on mängitud.

        :return: Mängude arv
        """
        return str(len(self.rows) - 1)

    def Get_Comp_Stats(self):
        """
        Leiab arvuti punktid.

        :return: Arvuti punktid
        """
        return self.comp

    def Get_User_Stats(self):
        """
        Leiab kasutaja punktid.

        :return: Kasutaja punktid
        """
        return self.user


app = Window()
app.mainloop()
