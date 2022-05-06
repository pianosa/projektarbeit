from flask import Flask, render_template, url_for, request
import daten


app = Flask("Mountrainer")


@app.route("/", methods=['GET', 'POST'])  # Verlinkung Hauptseite
def eingabe():
    if request.method == 'POST':

        return

    return render_template("index.html")


@app.route("/formular")  # Verlinkung Formular
def test():
    return "success"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
