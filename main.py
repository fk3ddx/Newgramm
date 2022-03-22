from flask import Flask, render_template
from flask_restful import Api
from data.db_session import global_init

app = Flask(__name__)
api = Api(app)
# global_init("db/Newgramm.bd")


@app.route('/')
def line():
    return render_template("line.html", title="Лента")


@app.route('/recommendations')
def recommendations():
    return render_template("recommendations.html", title="Рекомендации")


@app.route('/search')
def search():
    return render_template("search.html", title="Поиск")


@app.route('/profile')
def profile():
    return render_template("profile.html", title="Профиль")


@app.route('/profile/<int:id>')
def profile_user(id):
    return render_template("profile.html", title="Чужой профиль")


@app.route('/profile/change')
def profile_change():
    return render_template("register.html", title="Изменить профиль")


@app.route('/registration')
def registration():
    return render_template("register.html", title="Регистрация")


@app.route('/create_post')
def create_post():
    return render_template("create_post.html", title="Создать пост")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
