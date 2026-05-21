import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.widget import Widget

Window.clearcolor = (0.1, 0.1, 0.18, 1)

FREQ_LOTO = [7,13,23,41,38,17,3,29,45,22,11,36,19,48,5,31,44,26,8,15,42,33,20,9,46,2,37,14,28,49,6,18,39,25,12,43,30,4,47,21,35,10,27,40,16,34,24,32,1]
RETARD_LOTO = [32,1,24,34,16,40,27,10,35,21,47,4,30,43,12,25,39,18,6,49,28,14,37,2,46,9,20,33,42,15,8,26,44,31,5,48,19,36,11,22,45,29,3,17,38,41,23,13,7]
FREQ_EURO = [23,44,19,50,4,39,17,11,34,27,5,42,8,31,48,16,22,36,3,45,12,29,41,7,18,38,26,2,47,13,33,21,9,6,37,24,15,30,43,20,10,46,28,1,35,25,40,14,32,49]
RETARD_EURO = [14,40,25,35,1,28,46,10,20,43,30,15,50,24,37,6,9,21,33,7,26,38,18,12,45,29,41,3,16,48,36,22,13,2,47,31,8,42,5,27,11,17,39,4,19,34,44,23,24,32]

def pick_weighted(freq_list, count):
    pool = []
    for i, n in enumerate(freq_list):
        pool.extend([n] * (max(1, len(freq_list) - i) // 5 + 1))
    result = []
    pool_copy = pool.copy()
    while len(result) < count:
        n = random.choice(pool_copy)
        if n not in result:
            result.append(n)
    return sorted(result)

def gen_loto(s):
    if s == "Frecventa":
        numere = pick_weighted(FREQ_LOTO, 6)
    elif s == "Retardataire":
        numere = pick_weighted(RETARD_LOTO, 6)
    elif s == "Mixta (IA)":
        f = pick_weighted(FREQ_LOTO, 4)
        r = [n for n in pick_weighted(RETARD_LOTO, 6) if n not in f][:2]
        numere = sorted(f + r)
    else:
        numere = sorted(random.sample(range(1, 50), 6))
    return numere, random.randint(1, 10)

def gen_euro(s):
    if s == "Frecventa":
        numere = pick_weighted(FREQ_EURO, 5)
    elif s == "Retardataire":
        numere = pick_weighted(RETARD_EURO, 5)
    elif s == "Mixta (IA)":
        f = pick_weighted(FREQ_EURO, 3)
        r = [n for n in pick_weighted(RETARD_EURO, 5) if n not in f][:2]
        numere = sorted(f + r)
    else:
        numere = sorted(random.sample(range(1, 51), 5))
    return numere, sorted(random.sample(range(1, 13), 2))

def gen_keno():
    return sorted(random.sample(range(1, 71), 20))

class FDJApp(App):
    def build(self):
        self.title = "Generator FDJ"
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        title = Label(text="GENERATOR FDJ", font_size=28, bold=True,
                     color=(0.91, 0.27, 0.37, 1), size_hint_y=None, height=50)
        layout.add_widget(title)

        self.joc_spinner = Spinner(
            text="Loto 6/49",
            values=["Loto 6/49", "EuroMillions", "Keno 20/70"],
            size_hint_y=None, height=44,
            background_color=(0.06, 0.2, 0.38, 1),
            color=(1, 1, 1, 1), font_size=16)
        layout.add_widget(self.joc_spinner)

        self.strat_spinner = Spinner(
            text="Mixta (IA)",
            values=["Mixta (IA)", "Frecventa", "Retardataire", "Aleatorie"],
            size_hint_y=None, height=44,
            background_color=(0.06, 0.2, 0.38, 1),
            color=(1, 1, 1, 1), font_size=16)
        layout.add_widget(self.strat_spinner)

        btn = Button(text="GENEREAZA NUMERE", font_size=18, bold=True,
                    background_color=(0.91, 0.27, 0.37, 1),
                    size_hint_y=None, height=55)
        btn.bind(on_press=self.genereaza)
        layout.add_widget(btn)

        self.rezultat_label = Label(
            text="Apasa butonul pentru a genera numere",
            font_size=14, color=(0.68, 0.78, 0.86, 1),
            size_hint_y=None, height=120,
            text_size=(Window.width - 40, None),
            halign="center", valign="middle")
        layout.add_widget(self.rezultat_label)

        istoric_title = Label(text="Istoric:", font_size=14,
                             color=(1,1,1,1), size_hint_y=None, height=25,
                             halign="left")
        layout.add_widget(istoric_title)

        scroll = ScrollView(size_hint=(1, 1))
        self.istoric_label = Label(
            text="", font_size=12,
            color=(0.66, 0.85, 0.86, 1),
            size_hint_y=None,
            text_size=(Window.width - 40, None),
            halign="left", valign="top")
        self.istoric_label.bind(texture_size=self.istoric_label.setter("size"))
        scroll.add_widget(self.istoric_label)
        layout.add_widget(scroll)

        btn_sterge = Button(text="Sterge istoric", font_size=13,
                           background_color=(0.06, 0.2, 0.38, 1),
                           size_hint_y=None, height=36)
        btn_sterge.bind(on_press=self.sterge_istoric)
        layout.add_widget(btn_sterge)

        self.nr = 0
        return layout

    def genereaza(self, instance):
        joc = self.joc_spinner.text
        strat = self.strat_spinner.text

        if joc == "Loto 6/49":
            numere, chance = gen_loto(strat)
            rezultat = "LOTO 6/49\n"
            rezultat += "  ".join(str(n) for n in numere)
            rezultat += "  +  " + str(chance) + " (Chance)\n"
            rezultat += "Strategie: " + strat
            line = "Loto | " + str(numere) + " C:" + str(chance) + " | " + strat
        elif joc == "EuroMillions":
            numere, stele = gen_euro(strat)
            rezultat = "EUROMILLIONS\n"
            rezultat += "  ".join(str(n) for n in numere)
            rezultat += "  +  " + "  ".join(str(s) for s in stele) + " (Stele)\n"
            rezultat += "Strategie: " + strat
            line = "Euro | " + str(numere) + " St:" + str(stele) + " | " + strat
        else:
            numere = gen_keno()
            rezultat = "KENO 20/70\n"
            rezultat += "  ".join(str(n) for n in numere[:10]) + "\n"
            rezultat += "  ".join(str(n) for n in numere[10:])
            line = "Keno | " + str(numere)

        self.rezultat_label.text = rezultat
        self.nr += 1
        self.istoric_label.text = "#" + str(self.nr) + " | " + line + "\n" + self.istoric_label.text

    def sterge_istoric(self, instance):
        self.istoric_label.text = ""
        self.nr = 0

if __name__ == "__main__":
    FDJApp().run()