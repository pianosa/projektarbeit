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
        zurueckgelegte_Km = data["zurueckgelegte Km"]
        zurueckgelegte_Hm = data["zurueckgelegte Hm"]
        dauer = data["dauer"]
        try:
            with open("aktivitaeten.json", "r") as open_file: #r für read = lesen
                datei_inhalt = json.load(open_file)
        except FileNotFoundError:
            datei_inhalt = []

        my_dict = {"Name": name, "Datum": datum, "Zurueckgelegte Km": zurueckgelegte_Km, "Zurueckgelegte Hm": zurueckgelegte_Hm, "Dauer": dauer}
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


@app.route("/deinjahr/", methods=['GET', 'POST'])
def deinjahr():
    return render_template("deinjahr.html")


@app.route("/aboutme/", methods=['GET', 'POST'])
def aboutme():
    return render_template("aboutme.html")


@app.route("/bestaetigung/", methods=['GET', 'POST'])
def bestaetigung():
    return render_template("bestaetigung.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
