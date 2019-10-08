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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/indeed')
def dashboard():
    return render_template('etude_indeed.html')

if __name__ == "__main__":
    app.run(debug=True)

