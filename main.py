from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os
import threading
import webbrowser

app = Flask(__name__)

CSV_FILE = "treneri.csv"

# 🔹 Функция загрузки данных из CSV
def load_trainers():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            return df.to_dict(orient="records")
        except Exception as e:
            print("❌ Kļūda CSV failā:", e)
    return []

# 🔹 Главные страницы
@app.route("/")
def home():
    return render_template("main.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/izglitiba")
def izglitiba():
    return render_template("izglitiba.html")

@app.route("/sertifikacija")
def sertifikacija():
    return render_template("sertifikacija.html")

@app.route("/kopiena")
def kopiena():
    return render_template("kopiena.html")

@app.route("/Pasakumi")
def Pasakumi():
    return render_template("Pasakumi.html")

@app.route("/tiklosana")
def tiklosana():
    return render_template("tiklosana.html")

@app.route("/enu_diena")
def enu_diena():
    message = request.args.get("message")
    data = load_trainers()
    return render_template("enu_diena.html", message=message, data=data)

# 🔹 API для передачи данных в график
@app.route("/chart_data")
def chart_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        data = df.groupby("Sporta veids")["Treneru skaits"].sum().to_dict()
        return jsonify(data)
    return jsonify({})

# 🔹 Обработка загрузки CSV
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    file = request.files.get("file")
    if file and file.filename.endswith(".csv"):
        try:
            file.save(CSV_FILE)
            return redirect(url_for("enu_diena", message="✅ CSV veiksmīgi augšupielādēts!"))
        except Exception as e:
            return redirect(url_for("enu_diena", message=f"❌ Neizdevās saglabāt failu: {e}"))
    return redirect(url_for("enu_diena", message="❌ Lūdzu, izvēlieties derīgu CSV failu."))

# 🔹 Обработка кнопки "Pieteikties"
@app.route("/sign_up", methods=["POST"])
def sign_up():
    iestade = request.form.get("iestade")
    sporta_veids = request.form.get("sporta_veids")
    treneru_skaits = request.form.get("treneru_skaits")
    print(f"📌 Pieteikšanās saņemta: {iestade}, {sporta_veids}, {treneru_skaits}")
    return redirect(url_for("enu_diena", message="✅ Jūs veiksmīgi pieteicāties!"))

# 🔹 Автоматически открыть браузер (только если Flask запущен напрямую)
def open_browser():
    if not os.environ.get("FLASK_RUN_FROM_CLI"):
        webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
