import os

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

# Keep game names and their templates in one place so search links always work.
GAMES = {
    "adventure": "adventure.html",
    "factors": "factors.html",
    "fox and hounds": "fox and hounds.html",
    "mars lander": "mars lander.html",
    "maze": "maze.html",
    "maze room": "maze room.html",
    "missionaries and cannibals": "missionaries and cannibals.html",
    "snake": "snake.html",
    "soccer penalties": "soccer penalties.html",
    "solitare": "solitare.html",
    "tetris": "tetris.html",
    "trivia": "trivia.html",
    "virus": "virus.html",
    "zion": "zion.html",
}

# Accept common spellings used by the old homepage/search box.
ALIASES = {
    "choose your own adventure": "adventure",
    "chose your own adventure": "adventure",
    "solitaire": "solitare",
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    name = request.values.get("name", "").strip().casefold()
    game = ALIASES.get(name, name)
    if game in GAMES:
        return redirect(url_for("game", name=game))
    return render_template("index.html", name=name)


@app.route("/games/<path:name>")
def game(name):
    game_name = name.casefold()
    template = GAMES.get(game_name)
    if template is None:
        return render_template("404.html"), 404
    return render_template(template)


# Keep the original game URLs working, including names with spaces.
for game_name in GAMES:
    app.add_url_rule(
        f"/{game_name}",
        endpoint=f"legacy_game_{len(app.url_map._rules)}",
        view_func=lambda game_name=game_name: redirect(
            url_for("game", name=game_name)
        ),
    )


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )
