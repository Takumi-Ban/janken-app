from flask import Flask, redirect, render_template, request, url_for
from flask import session as fsession
from main import Auth, Play
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def root():
    auth = Auth()
    auth.check()
    return redirect(url_for('index'))

@app.route('/index')
def index():
    auth = Auth()
    auth.check()
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    auth = Auth()
    auth.check()
    if request.method == 'GET':
        return render_template('register.html')
    else:
        msg = auth.register()
        if msg:
            return render_template('register.html', msg = msg)
        else:
            return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    auth = Auth()
    auth.check()
    if request.method == 'GET':
        return render_template('login.html')
    else:
        msg = auth.login()
        if msg:
            return render_template('login.html', msg = msg)
        else:
            return redirect(url_for('index'))  

@app.route('/logout')
def logout():
    auth = Auth()
    auth.check()
    auth.logout()
    return redirect(url_for('index'))

@app.route('/history')
def history():
    auth = Auth()
    auth.check()
    if fsession['flag'] == False:
        return redirect(url_for('login'))
    else:
        p = Play()
        data = p.history()
        rank_data = p.rank()
        return render_template('history.html', results=data, user_rank=rank_data)


@app.route('/play', methods=['GET', 'POST'])
def play():
    auth = Auth()
    auth.check()
    if fsession['flag'] == False:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            return render_template('play.html')
        else:
            p = Play()
            p.insert_result()
            return redirect(url_for('play'))

if __name__ == '__main__':
    app.run(debug=True)