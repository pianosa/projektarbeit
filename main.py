from flask import Flask
from flask import render_template
from flask import request
import daten
import json
from json import loads


app = Flask("Mountrainer")


@app.route("/")  # Verlinkung Hauptseite
def index():
    return render_template("index.html")


@app.route("/formular/", methods=['GET', 'POST'])  # Verlinkung Formular
def formular():
    if request.method == 'POST':
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

        my_dict = {"Name": name, "Datum": datum, "zurueckgelegte_Km": zurueckgelegte_Km, "zurueckgelegte_Hm": zurueckgelegte_Hm, "Dauer": dauer}
        datei_inhalt.append(my_dict)

        with open("aktivitaeten.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4) #indent=4 sieht schöner aussieht
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
    summe_km_anne = 0
    summe_km_laura = 0


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


    return render_template("deinjahr.html",
                           summe_km_janina=summe_km_janina,
                           summe_km_anne=summe_km_anne,
                           summe_km_laura=summe_km_laura)


@app.route("/bestaetigung/", methods=['GET', 'POST'])
def bestaetigung():
    return render_template("bestaetigung.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
