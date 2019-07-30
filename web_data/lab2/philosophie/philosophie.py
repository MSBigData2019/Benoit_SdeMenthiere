#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash, url_for
from getpage import getPage

app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', message="Bonjour, monde !")

# Si vous définissez de nouvelles routes, faites-le ici
@app.route('/new-game', methods=['POST'])
def newgame():
    title = request.form['start']
    session['article'] = title
    session['score'] = 0
    if getPage(title)[0] == 'Philosophie':
        flash("You can't start with Philosophie")
        return redirect('/')
    if 'Philosophie' in getPage(title)[1]:
        flash("You can't start with this world because it redirects to Philosophie")
        return redirect('/')
    if getPage(title)[1] == []:
        flash('You loose: no link in this page')
        return redirect('/')
    else:
        return redirect('/game')

@app.route('/game', methods=['GET'])
def game():
    session['score'] += 1
    title, links = getPage(session['article'])
    return render_template('game.html', title=title, links=links)

@app.route('/move', methods=['POST'])
def move():
    session['article'] = request.form['destination']
    if session['article'] == 'Philosophie':
        flash('You win')
        return redirect('/')
    if getPage(session['article'])[1] == []:
        flash('You loose: no link in this page')
        return redirect('/')
    else:
        return redirect('/game')

if __name__ == '__main__':
    app.run(debug=True)
