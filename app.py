from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session

boggle_game = Boggle()
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-secret-secret"

@app.route("/")
def show_board():
    session["board"] = boggle_game.make_board()
    board = session["board"]
    highscore = session.get("highscore", 0)
    times_played = session.get("times_played", 0)
    return render_template("board.html", board=board, highscore=highscore, played=times_played)

@app.route("/check-word")
def check_guess():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board,word)
    return jsonify({"result": response}) 

@app.route("/final-score", methods=["POST"])
def end_game():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    times_played = session.get("times_played", 0)
    session["times_played"] = times_played + 1
    session["highscore"] = max(score, highscore)

    return jsonify(newRecord = score > highscore)
