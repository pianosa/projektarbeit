from flask import Flask
from flask import render_template
from flask import request
import daten
import json


app = Flask("Mountrainer")


@app.route("/")  # Verlinkung Hauptseite
def index():
    return render_template("index.html")


@app.route("/formular/", methods=['GET', 'POST'])  # Verlinkung Formular
def formular():
    if request.method == 'POST':
        data = request.form
        vorname = data["vorname"]
        nachname = data["nachname"]
        datum = data["datum"]
        zurueckgelegte_Km = data["zurueckgelegte Km"]
        zurueckgelegte_Hm = data["zurueckgelegte Hm"]
        dauer = data["dauer"]
        temperatur = data["temperatur"]
        try:
            with open("aktivitaeten.json", "r") as open_file: #r für read = lesen
                datei_inhalt = json.load(open_file)
        except FileNotFoundError:
            datei_inhalt = []

        my_dict = {"Vorname": vorname, "Nachname": nachname, "Datum": datum, "Zurueckgelegte Km": zurueckgelegte_Km, "Zurueckgelegte Hm": zurueckgelegte_Hm, "Temperatur": temperatur, "Dauer": dauer}
        datei_inhalt.append(my_dict)

        with open("aktivitaeten.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4) #indent=4 sieht schöner aussieht
        return str("Danke für deine Eingabe, die Daten wurden gespeichert.")
    else:
        return render_template("formular.html")


@app.route("/analyse/", methods=['GET', 'POST'])
def analyse():
    return render_template("analyse.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
