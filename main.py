from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
import random
from datetime import datetime

from rechnen.steuern import berechnen
from rechnen.steuern import abgaben #diese Werkzeuge sind vorhanden,aber ist nur Vorbereitung. Zur Verfügung stellen.

app = Flask(__name__)

@app.route("/")
def hello():

    names = ['Fabian', "Wolfgang", "Michael", "Cristina", "Meret"]
    name_choice = random.choice(names)
    about_link = url_for("about")
    return render_template("index.html", name=name_choice, link=about_link)


@app.route("/about")
def about():
    return "About test"


@app.route('/hello/<name2>')  # /hello/Fabian
def begruessung(name2):
    return "Hallo " + name2 + "!"


@app.route('/form', methods=["get", "post"])
def form():
    if request.method.lower() == "get":
        return render_template('formular.html')
    if request.method.lower() == "post":
        name = request.form['vorname']
        return name


@app.route("/list")
def auflistung():
    elemente = ["Bla", "Blubber", "Käsekuchen"]
    return render_template("liste.html", html_elemente=elemente)


@app.route("/table")
def tabelle():
    biere = [
        {
            "name": "Glatsch",
            "herkunft": "Chur",
            "vol": "4.0",
            "brauerei": "Calanda",
            "preis": 0.90
        },
        {
            "name": "Retro",
            "herkunft": "Luzern",
            "vol": "4.9",
            "brauerei": "Eichhof",
            "preis": 2.0
        },
        {
            "name": "Quöllfrisch",
            "herkunft": "Appenzell",
            "vol": "4.8",
            "brauerei": "Locher",
            "preis": 1.8
        }
    ]
    for bier in biere:
        preis = bier["preis"]
        tax = berechnen(preis)
        bier["steuern"] = tax
    # biere = False
    table_header = ["Name", "Herkunft", "Vol%", "Brauerei", "Preis", "Steuern"]
    return render_template("beer.html", beers=biere, header=table_header)


@app.route("/abgaben_chf", methods=["get", "post"])
def egal_was():
    if request.method.lower() == "get":
        return render_template("preis.html")
    if request.method.lower() == "post":
        preis = request.form["preis"]
        preis = float(preis)
        abgaben_betrag = abgaben(preis)

        now = datetime.now()
        with open("jail_free_card.txt", "a", encoding="utf8") as offene_datei:
            offene_datei.write(f"{now}, {preis}, {abgaben_betrag}\n")
        return render_template("preis.html", abgabe=abgaben_betrag)


@app.route("/abgaben_eur")
def egal_was_2():
    abgaben_betrag = abgaben(400)
    return f"{abgaben_betrag} EUR"


@app.route("/datum")
def datum_anzeigen():
    with open("jail_free_card.txt", encoding="utf8") as open_file:
        inhalt = open_file.read()
    return inhalt.replace("\n", "<br>")


@app.route("/zufall")
def zufall():
    zahl = random.randint(1, 100)
    return str(zahl)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

