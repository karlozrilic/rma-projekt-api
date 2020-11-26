import os
import json
from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)

with open('data-mini.json', 'r', encoding='utf-8-sig') as json_file:
    data = json.load(json_file)

cr = {
    "type": "service_account",
    "project_id": "rwa-projekt-api",
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-nedvi%40rwa-projekt-api.iam.gserviceaccount.com"
}

cred = credentials.Certificate(cr)
firebase_admin.initialize_app(cred)

db = firestore.client()
top_songs = db.collection("top_songs")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/v1/list-songs", methods=["GET"])
def list_songs():
    songs = [doc.to_dict() for doc in top_songs.order_by("id", direction=firestore.Query.ASCENDING).stream()]
    if len(songs) == 0:
        return {"error", "No data"}, 409
    else:
        data = []
        for i in songs:
            data.append(i)
        temp = {"data": data}
        return temp

@app.route("/api/v1/init-add", methods=["GET"])
def init_add():
    songs = [doc.to_dict() for doc in top_songs.stream()]
    print(data[0]["strAlbum"])
    if len(songs) == 0:
        for song in data:
            top_songs.document().set({
                "id": data.index(song)+1,
                "strAlbum": song["strAlbum"],
                "strArtist": song["strArtist"],
                "strTrack": song["strTrack"],
                "strDescription": song["strDescription"],
                "strGenre": song["strGenre"],
                "strMusicVid": song["strMusicVid"],
                "strTrackThumb": song["strTrackThumb"]
            })
        return {"message": "Data added"}
    else:
        return {"error": "Data already exists"}

if __name__ == "__main__":
    app.run(debug=True)