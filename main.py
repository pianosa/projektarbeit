from flask import Flask
from flask import render_template
from flask import request
import json
from json import loads
import plotly.express as px
from plotly.offline import plot


app = Flask("Mountrainer")


@app.route("/")  # Verlinkung Hauptseite
def index():
    return render_template("index.html")


@app.route("/formular/", methods=["GET", "POST"])  # Verlinkung Formular
def formular():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        datum = data["datum"]
        zurueckgelegte_Km = data["zurueckgelegte_Km"]
        zurueckgelegte_Hm = data["zurueckgelegte_Hm"]
        dauer = data["dauer"]
        try:
            with open("aktivitaeten.json", "r") as open_file: #r für read = lesen
                datei_inhalt = json.load(open_file)
        except FileNotFoundError:
            datei_inhalt = []

        my_dict = {"Name": name, "Datum": datum, "zurueckgelegte_Km": zurueckgelegte_Km,
                   "zurueckgelegte_Hm": zurueckgelegte_Hm, "Dauer": dauer}
        datei_inhalt.append(my_dict)

        with open("aktivitaeten.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4)  # indent=4 sieht schöner aussieht
        return render_template("bestaetigung.html")
    else:
        return render_template("formular.html")


@app.route("/analyse/")
def analyse():
    with open("aktivitaeten.json") as open_file:
        json_as_string = open_file.read()
        daten_inhalt = loads(json_as_string)
    return render_template("analyse.html", daten_inhalt=daten_inhalt)


@app.route("/deinjahr/")
def berechnung():
    with open("aktivitaeten.json", "r") as open_file:
        json_as_string = open_file.read()
        daten_inhalt = loads(json_as_string)

    summe_km_janina = 0
    summe_hm_janina = 0
    summe_h_janina = 0
    summe_km_anne = 0
    summe_hm_anne = 0
    summe_h_anne = 0
    summe_km_laura = 0
    summe_hm_laura = 0
    summe_h_laura = 0

    for eintrag in daten_inhalt:
        if eintrag["Name"] == "Janina":
            try:
                summe_km_janina += float(eintrag["zurueckgelegte_Km"])
            except:
                continue
        elif eintrag["Name"] == "Anne":
            try:
                summe_km_anne += float(eintrag["zurueckgelegte_Km"])
            except:
                continue
        elif eintrag["Name"] == "Laura":
            try:
                summe_km_laura += float(eintrag["zurueckgelegte_Km"])
            except:
                continue

    for eintrag in daten_inhalt:
        if eintrag["Name"] == "Janina":
            try:
                summe_hm_janina += float(eintrag["zurueckgelegte_Hm"])
            except:
                continue
        elif eintrag["Name"] == "Anne":
            try:
                summe_hm_anne += float(eintrag["zurueckgelegte_Hm"])
            except:
                continue
        elif eintrag["Name"] == "Laura":
            try:
                summe_hm_laura += float(eintrag["zurueckgelegte_Hm"])
            except:
                continue

    for eintrag in daten_inhalt:
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

    balkendiagramm_hm = px.bar(
            x=["Janina", "Anne", "Laura"],
            y=[summe_hm_janina, summe_hm_anne, summe_hm_laura],
            labels={"x": "Name", "y": "Anzahl hm"}
    )
    div_balkendiagramm_hm = plot(balkendiagramm_hm, output_type="div")

    balkendiagramm_km = px.bar(
            x=["Janina", "Anne", "Laura"],
            y=[summe_km_janina, summe_km_anne, summe_km_laura],
            labels={"x": "Name", "y": "Anzahl km"}
    )
    div_balkendiagramm_km = plot(balkendiagramm_km, output_type="div")

    balkendiagramm_h = px.bar(
            x=["Janina", "Anne", "Laura"],
            y=[summe_h_janina, summe_h_anne, summe_h_laura],
            labels={"x": "Name", "y": "Anzahl h"}
    )
    div_balkendiagramm_h = plot(balkendiagramm_h, output_type="div")

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


@app.route("/bestaetigung/", methods=["GET", "POST"])
def bestaetigung():
    return render_template("bestaetigung.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
