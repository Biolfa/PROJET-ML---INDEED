'''from flask import Flask, render_template

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

@app.route('/')
def index():
        return "Hello world !"

#render_template est une fonction qui permet faire le lien avec le fichier html pour éviter de lélanger les codes lisibles par le serveur vs ceux exécutés côté cliengt
@app.route('/dashboard/')
def dashboard():
        return render_template('dashboard.html')

if __name__ == "__main__":
        app.run()

#Flask vous permet d'importer toutes les variables en une fois dans votre projet en utilisant la méthode config.from_object(file_name)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

'''


# -*- coding: utf-8 -*-

from flask import Flask, render_template
app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)

'''

@app.route('/error')
def error():
    return render_template('404.html')

@app.route('/blank')
def blank():
    return render_template('blank.html')

@app.route('/charts)
def charts():
    return render_template('charts.html')

@app.route('/password')
def password():
    return render_template('forgot-password.html')

@app.route('/login')
def index():
    return render_template('index.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/readme')
def readme():
    return render_template('readme.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

'''




