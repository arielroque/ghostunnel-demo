from flask import Flask

app = Flask(__name__)

@app.route("/")
def health():
    return "I am the server running with TLS and I am fine"

if __name__ == "__main__":
    app.run(port=8000)