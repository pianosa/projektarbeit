from flask import Flask  # DOM-Tree Architektur (DOM = Document Object Model)
from flask import render_template  # Ausgabe von HTML-Dokumenten
from flask import request  # Datenübergabe (persistente Daten) für GET- / POST-Verfahren
import json  # JavaScript Objekt Notation: JavaScript Nutzung
from json import loads  # JSON String einlesen in Python
import plotly.express as px  # Datenvisualisierung mit Diagramm
from plotly.offline import plot  # Datenvisualisierung auch im Offline-Modus möglich


app = Flask("Mountrainer")


@app.route("/")  # Verlinkung Hauptseite
def index():  # Home-Seite: keine weitere Definition ausser Ausgabe index.html
    return render_template("index.html")


@app.route("/formular/", methods=["GET", "POST"])  # Verlinkung Formular
def formular():  # Definition hinter dem Formular
    if request.method == "POST":  # POST = Dateneingabe und danach Speicherung in JSON
        data = request.form  # request = Daten werden von Formular übergeben
        name = data["name"]  # Variable wird für einzelne Eingaben definiert
        datum = data["datum"]
        zurueckgelegte_km = data["zurueckgelegte_km"]
        zurueckgelegte_hm = data["zurueckgelegte_hm"]
        dauer = data["dauer"]
        try:
            with open("aktivitaeten.json", "r") as open_file:  # r für read = lesen, falls JSON-Datei schon vorhanden
                datei_inhalt = json.load(open_file)
        except FileNotFoundError:
            datei_inhalt = []  # Wenn JSON noch nicht erstellt, wird neue Liste angelegt mit Namen datei_inhalt

        my_dict = {"Name": name, "Datum": datum, "zurueckgelegte_km": zurueckgelegte_km,
                   "zurueckgelegte_hm": zurueckgelegte_hm, "Dauer": dauer}  # Variablen werden in ein Dictionary gezogen
        datei_inhalt.append(my_dict)  # einzelne Formular-Füllungen werden als Dictionary der JSON-Datei hinzugefügt

        with open("aktivitaeten.json", "w") as open_file:  # w für write = schreiben, falls JSON-Datei noch nicht vorhanden
            json.dump(datei_inhalt, open_file, indent=4)  # indent=4 sieht schöner aussieht
        return render_template("bestaetigung.html")
    else:
        return render_template("formular.html")


@app.route("/analyse/")   # Verlinkung Wanderungen
def analyse():
    with open("aktivitaeten.json") as open_file:
        json_as_string = open_file.read()  # Lese-Zugriff auf JSON Datei
        daten_inhalt = loads(json_as_string)  # loads = JSON String einlesen in Python, Daten in Dictionary im JSON
        # Quelle: https://hellocoding.de/blog/coding-language/python/json-verwenden
    return render_template("analyse.html", daten_inhalt=daten_inhalt)


@app.route("/deinjahr/")  # Verlinkung Auswertung Wanderungen
def berechnung():  # Berechnung Summe der Attribute einer Wanderung
    with open("aktivitaeten.json", "r") as open_file:
        json_as_string = open_file.read()
        daten_inhalt = loads(json_as_string)

    #  Startsumme für Variablen in Berechnungen
    summe_km_janina = 0
    summe_hm_janina = 0
    summe_h_janina = 0
    summe_km_anne = 0
    summe_hm_anne = 0
    summe_h_anne = 0
    summe_km_laura = 0
    summe_hm_laura = 0
    summe_h_laura = 0

    for eintrag in daten_inhalt:  # for-Schleife um Summe zu ziehen für Kilometer
        if eintrag["Name"] == "Janina":
            try:
                summe_km_janina += float(eintrag["zurueckgelegte_km"])
            except:
                continue
        elif eintrag["Name"] == "Anne":
            try:
                summe_km_anne += float(eintrag["zurueckgelegte_km"])
            except:
                continue
        elif eintrag["Name"] == "Laura":
            try:
                summe_km_laura += float(eintrag["zurueckgelegte_km"])
            except:
                continue

    for eintrag in daten_inhalt:  # for-Schleife um Summe zu ziehen für Höhenmeter
        if eintrag["Name"] == "Janina":
            try:
                summe_hm_janina += float(eintrag["zurueckgelegte_hm"])
            except:
                continue
        elif eintrag["Name"] == "Anne":
            try:
                summe_hm_anne += float(eintrag["zurueckgelegte_hm"])
            except:
                continue
        elif eintrag["Name"] == "Laura":
            try:
                summe_hm_laura += float(eintrag["zurueckgelegte_hm"])
            except:
                continue

    for eintrag in daten_inhalt:  # for-Schleife um Summe zu ziehen für Stunden
        if eintrag["Name"] == "Janina":
            try:
                summe_h_janina += float(eintrag["Dauer"])
            except:
                continue
        elif eintrag["Name"] == "Anne":
            try:
                summe_h_anne += float(eintrag["Dauer"])
            except:
                continue
        elif eintrag["Name"] == "Laura":
            try:
                summe_h_laura += float(eintrag["Dauer"])
            except:
                continue

    balkendiagramm_hm = px.bar(  # Balkendiagramm mit plotly
            x=["Janina", "Anne", "Laura"],  # Daten für x-Achse des Diagramms
            y=[summe_hm_janina, summe_hm_anne, summe_hm_laura],  # Daten für y-Achse des Diagramms
            labels={"x": "Name", "y": "Anzahl hm"}  # Achsenbeschriftung
    )
    div_balkendiagramm_hm = plot(balkendiagramm_hm, output_type="div")  # Balkendiagramm für Vergleich Höhenmeter

    balkendiagramm_km = px.bar(
            x=["Janina", "Anne", "Laura"],
            y=[summe_km_janina, summe_km_anne, summe_km_laura],
            labels={"x": "Name", "y": "Anzahl km"}
    )
    div_balkendiagramm_km = plot(balkendiagramm_km, output_type="div")  # Balkendiagramm für Vergleich Kilometer

    balkendiagramm_h = px.bar(
            x=["Janina", "Anne", "Laura"],
            y=[summe_h_janina, summe_h_anne, summe_h_laura],
            labels={"x": "Name", "y": "Anzahl h"}
    )
    div_balkendiagramm_h = plot(balkendiagramm_h, output_type="div")  # Balkendiagramm für Vergleich Stunden

    return render_template("deinjahr.html",
                           summe_km_janina=summe_km_janina,
                           summe_km_anne=summe_km_anne,
                           summe_km_laura=summe_km_laura,
                           summe_hm_janina=summe_hm_janina,
                           summe_hm_anne=summe_hm_anne,
                           summe_hm_laura=summe_hm_laura,
                           summe_h_janina=summe_h_janina,
                           summe_h_anne=summe_h_anne,
                           summe_h_laura=summe_h_laura,
                           balkendiagramm_hm=div_balkendiagramm_hm,
                           balkendiagramm_km=div_balkendiagramm_km,
                           balkendiagramm_h=div_balkendiagramm_h)


@app.route("/bestaetigung/")  # kein verlinkter Menu-Punkt aber eine Seite für Bestätigung
def bestaetigung():
    return render_template("bestaetigung.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
