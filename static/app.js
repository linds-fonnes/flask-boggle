class BoggleGame {
  constructor() {
    this.words = new Set();
    this.score = 0;
    this.seconds = 60;
    this.timer = setInterval(this.countdown.bind(this), 1000);
    this.displayTimer();
    $(".submit").on("submit", this.checkGuess.bind(this));
  }

  displayMessage(msg) {
    $(".message").text(msg);
  }

  displayScore() {
    $(".score").text("Score: " + this.score);
  }

  displayTimer() {
    $(".timer").text("Time Remaining: " + this.seconds);
  }

  async countdown() {
    this.seconds -= 1;
    this.displayTimer();

    if (this.seconds === 0) {
      clearInterval(this.timer);
      await this.endGame();
    }
  }

  async checkGuess(evt) {
    evt.preventDefault();

    const $word = $(".word");
    let word = $word.val();

    if (!word) return;
    if (this.words.has(word)) {
      this.displayMessage(`Already found the word: ${word}`);
      return;
    }

    const response = await axios.get("/check-word", { params: { word: word } });

    if (response.data.result === "not-on-board") {
      this.displayMessage(`The word ${word} is not on the board!`);
    } else if (response.data.result === "not-word") {
      this.displayMessage(`${word} is not a valid word!`);
    } else if (response.data.result === "ok") {
      this.displayMessage(`Nice, ${word} is valid!`);
      this.words.add(word);
      if (word.length < 4) {
        this.score += 1;
      } else if (word.length === 4) {
        this.score += 2;
      } else if (word.length === 5) {
        this.score += 3;
      } else if (word.length >= 6) {
        this.score += 4;
      }
      this.displayScore();
    }

    $word.val("");
  }

  async endGame() {
    $(".submit").hide();
    const response = await axios.post("/final-score", { score: this.score });
    if (response.data.newRecord) {
      this.displayMessage(`New High Score: ${this.score}`);
    } else {
      this.displayMessage(`Final Score: ${this.score}`);
    }
  }
}

let game = new BoggleGame();
