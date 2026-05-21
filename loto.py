import tkinter as tk
from tkinter import ttk
import random

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

def bila(parent, numar, bg, fg):
    c = tk.Canvas(parent, width=48, height=48, bg="#16213e", highlightthickness=0)
    c.pack(side=tk.LEFT, padx=4)
    c.create_oval(2, 2, 46, 46, fill=bg, outline="")
    c.create_text(24, 24, text=str(numar), font=("Arial", 13, "bold"), fill=fg)

class App:
    def __init__(self, root):
        self.root = root
        root.title("Generator FDJ - Franta")
        root.geometry("700x620")
        root.configure(bg="#1a1a2e")
        root.resizable(False, False)

        tk.Label(root, text="GENERATOR FDJ", font=("Arial", 22, "bold"), bg="#1a1a2e", fg="#e94560").pack(pady=15)

        fj = tk.Frame(root, bg="#1a1a2e")
        fj.pack(pady=5)
        tk.Label(fj, text="Joc:", font=("Arial", 12), bg="#1a1a2e", fg="white").pack(side=tk.LEFT, padx=5)
        self.joc = tk.StringVar(value="Loto 6/49")
        ttk.Combobox(fj, textvariable=self.joc, values=["Loto 6/49", "EuroMillions", "Keno"], width=15, state="readonly").pack(side=tk.LEFT)

        fs = tk.Frame(root, bg="#1a1a2e")
        fs.pack(pady=5)
        tk.Label(fs, text="Strategie:", font=("Arial", 12), bg="#1a1a2e", fg="white").pack(side=tk.LEFT, padx=5)
        self.strat = tk.StringVar(value="Mixta (IA)")
        ttk.Combobox(fs, textvariable=self.strat, values=["Frecventa", "Retardataire", "Mixta (IA)", "Aleatorie"], width=15, state="readonly").pack(side=tk.LEFT)

        tk.Button(root, text="GENEREAZA NUMERE", font=("Arial", 14, "bold"), bg="#e94560", fg="white", relief="flat", padx=20, pady=10, cursor="hand2", command=self.gen).pack(pady=20)

        self.fr = tk.Frame(root, bg="#16213e")
        self.fr.pack(pady=5, padx=30, fill="x")
        self.lj = tk.Label(self.fr, text="", font=("Arial", 13, "bold"), bg="#16213e", fg="#e94560")
        self.lj.pack(pady=8)
        self.fb = tk.Frame(self.fr, bg="#16213e")
        self.fb.pack(pady=5)
        self.lb = tk.Label(self.fr, text="", font=("Arial", 11), bg="#16213e", fg="#f5a623")
        self.lb.pack(pady=5)
        self.ls = tk.Label(self.fr, text="", font=("Arial", 10), bg="#16213e", fg="#7ec8e3")
        self.ls.pack(pady=5)

        tk.Label(root, text="Istoric:", font=("Arial", 11, "bold"), bg="#1a1a2e", fg="white").pack(anchor="w", padx=30, pady=(10,2))
        self.ist = tk.Text(root, height=6, width=75, bg="#0f3460", fg="#a8dadc", font=("Courier", 9), relief="flat")
        self.ist.pack(padx=30)
        self.ist.config(state="disabled")
        tk.Button(root, text="Sterge istoric", font=("Arial", 9), bg="#0f3460", fg="white", relief="flat", cursor="hand2", command=self.sterge).pack(pady=8)
        self.nr = 0

    def gen(self):
        joc = self.joc.get()
        s = self.strat.get()
        for w in self.fb.winfo_children():
            w.destroy()
        if joc == "Loto 6/49":
            numere, chance = gen_loto(s)
            self.lj.config(text="LOTO 6/49")
            for n in numere:
                bila(self.fb, n, "#e94560", "white")
            tk.Label(self.fb, text=" + ", bg="#16213e", fg="white", font=("Arial", 14)).pack(side=tk.LEFT)
            bila(self.fb, chance, "#f5a623", "#1a1a2e")
            self.lb.config(text="Numero Chance: " + str(chance))
            line = "Loto | " + str(numere) + " C:" + str(chance) + " | " + s + "\n"
        elif joc == "EuroMillions":
            numere, stele = gen_euro(s)
            self.lj.config(text="EUROMILLIONS")
            for n in numere:
                bila(self.fb, n, "#1a78c2", "white")
            tk.Label(self.fb, text=" + ", bg="#16213e", fg="#f5a623", font=("Arial", 14)).pack(side=tk.LEFT)
            for st in stele:
                bila(self.fb, st, "#f5a623", "#1a1a2e")
            self.lb.config(text="Stele: " + str(stele))
            line = "Euro | " + str(numere) + " St:" + str(stele) + " | " + s + "\n"
        else:
            numere = gen_keno()
            self.lj.config(text="KENO 20/70")
            r1 = tk.Frame(self.fb, bg="#16213e")
            r1.pack()
            r2 = tk.Frame(self.fb, bg="#16213e")
            r2.pack()
            for i, n in enumerate(numere):
                bila(r1 if i < 10 else r2, n, "#6c3483", "white")
            self.lb.config(text="")
            line = "Keno | " + str(numere) + "\n"
        self.ls.config(text="Strategie: " + s)
        self.nr += 1
        self.ist.config(state="normal")
        self.ist.insert("1.0", "#" + str(self.nr) + " | " + line)
        self.ist.config(state="disabled")

    def sterge(self):
        self.ist.config(state="normal")
        self.ist.delete("1.0", tk.END)
        self.ist.config(state="disabled")
        self.nr = 0

root = tk.Tk()
App(root)
root.mainloop()