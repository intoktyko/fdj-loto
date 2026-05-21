from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

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
    if s == "frecventa":
        numere = pick_weighted(FREQ_LOTO, 6)
    elif s == "retardataire":
        numere = pick_weighted(RETARD_LOTO, 6)
    elif s == "mixta":
        f = pick_weighted(FREQ_LOTO, 4)
        r = [n for n in pick_weighted(RETARD_LOTO, 6) if n not in f][:2]
        numere = sorted(f + r)
    else:
        numere = sorted(random.sample(range(1, 50), 6))
    return numere, random.randint(1, 10)

def gen_euro(s):
    if s == "frecventa":
        numere = pick_weighted(FREQ_EURO, 5)
    elif s == "retardataire":
        numere = pick_weighted(RETARD_EURO, 5)
    elif s == "mixta":
        f = pick_weighted(FREQ_EURO, 3)
        r = [n for n in pick_weighted(RETARD_EURO, 5) if n not in f][:2]
        numere = sorted(f + r)
    else:
        numere = sorted(random.sample(range(1, 51), 5))
    return numere, sorted(random.sample(range(1, 13), 2))

def gen_keno():
    return sorted(random.sample(range(1, 71), 20))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/genereaza", methods=["POST"])
def genereaza():
    data = request.json
    joc = data.get("joc", "loto")
    strat = data.get("strat", "mixta")
    if joc == "loto":
        numere, chance = gen_loto(strat)
        return jsonify({"joc": "Loto 6/49", "numere": numere, "bonus": [chance], "tip_bonus": "chance"})
    elif joc == "euro":
        numere, stele = gen_euro(strat)
        return jsonify({"joc": "EuroMillions", "numere": numere, "bonus": stele, "tip_bonus": "stele"})
    else:
        numere = gen_keno()
        return jsonify({"joc": "Keno 20/70", "numere": numere, "bonus": [], "tip_bonus": ""})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")