from flask import Flask, render_template, request
import requests


app = Flask(__name__)

API_KEY = ("9971c8a07ae61825931bc9ad2c1d54d8")
BASE_URL = "https://api.themoviedb.org/3"
IMG_URL = "https://image.tmdb.org/t/p/w500"

def obtener_generos():
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY, "language": "es-ES"}
    return requests.get(url, params=params).json().get("genres", [])

@app.route("/")
def index():
    url = f"{BASE_URL}/trending/all/week"
    params = {"api_key": API_KEY, "language": "es-ES"}
    datos = requests.get(url, params=params).json()
    resultados = datos.get("results", [])[:10]
    return render_template("index.html", items=resultados, img_url=IMG_URL)

@app.route("/search")
def search():
    query = request.args.get("q")
    genre = request.args.get("genre")
    page = request.args.get("page", 1)

    url = f"{BASE_URL}/search/multi"
    params = {
        "api_key": API_KEY,
        "language": "es-ES",
        "query": query,
        "page": page
    }

    respuesta = requests.get(url, params=params).json()

    return render_template(
        "search.html",
        resultados=respuesta.get("results", []),
        total_pages=respuesta.get("total_pages", 1),
        page=int(page),
        query=query,
        generos=obtener_generos(),
        img_url=IMG_URL
    )

@app.route("/detail/<tipo>/<int:item_id>")
def detail(tipo, item_id):
    url = f"{BASE_URL}/{tipo}/{item_id}"
    params = {"api_key": API_KEY, "language": "es-ES"}
    data = requests.get(url, params=params).json()

    credits = requests.get(
        f"{url}/credits", params=params
    ).json()

    videos = requests.get(
        f"{url}/videos", params=params
    ).json()

    trailer = None
    for v in videos.get("results", []):
        if v["type"] == "Trailer":
            trailer = v["key"]
            break

    return render_template(
        "detalle.html",
        item=data,
        cast=credits.get("cast", [])[:6],
        trailer=trailer,
        img_url=IMG_URL,
        tipo=tipo
    )

if __name__ == "__main__":
    app.run(debug=True)
