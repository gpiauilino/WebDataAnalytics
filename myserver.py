from flask import Flask, Response, render_template
import sqlite3
import os
import datetime
from flask import send_from_directory
from werkzeug.exceptions import abort

app = Flask(__name__)

#A função get_db_connection() abre uma conexão ao arquivo de banco de dados database.db e, em seguida,
# define o atributo row_factory ao sqlite3.Row para que você tenha acesso baseado em nome às colunas. 
# Ou seja, a conexão do banco de dados retornará linhas que se comportam como um dicionário comum do Python. 
# Por último, a função retorna o objeto de conexão conn que você utilizará para acessar o banco de dados.

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#Chamada de função para realizar select filtrada pelo id.
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(app.root_path, filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

if __name__ == '__main__':  # pragma: no cover
    app.run(port=5001)