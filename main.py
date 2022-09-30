from flask import request
from flask import session as fsession
from sqlalchemy import distinct
from initdb import User, Results
from dbsetting import session, Engine
import hashlib
import datetime

class Auth():
    def __init__(self):
        return

    def get_userpass(self):
        """
        get username, password from webpage
        """
        username = request.form['username']
        password = request.form['password']
        password = hashlib.md5(password.encode()).hexdigest()
        return username, password

    def register(self):
        """
        Register user info
        """
        username, password = self.get_userpass()

        exist = session.query(User.name).filter(User.name == str(username)).all()
        exist = [r.name for r in exist]

        if username in exist:
            return 'This user is already exists.'
        else:
            user = User()
            user.name = str(username)
            user.password = str(password)
            user.time = datetime.datetime.now()
            session.add(user)
            session.commit()
            session.close()
            return

    def check(self):
        if 'flag' in fsession:
            return
        else:
            fsession['flag'] = False
            return

    def login(self):
        """
        login process
        """
        username, password = self.get_userpass()

        pass_info = session.query(User.password).filter(User.name == str(username)).all()
        pass_info = [r.password for r in pass_info]

        if password in pass_info == False:
            return 'Wrong user name or password'
        else:
            if password in pass_info:
                fsession['flag'] = True
                fsession['username'] = str(username)
                return None
            else:
                fsession['flag'] = False
                return 'Wrong username or password'

    def logout(self):
        """
        Logout process
        """
        fsession.clear()
        fsession['flag'] = False
        return

class Play():
    def __init__(self):
        return

    def insert_result(self):
        cor_label = request.form['cor_label']
        res_label = request.form['res_label']

        results = Results()
        results.username = str(fsession['username'])
        results.correctlabel = str(cor_label)
        results.result_label = str(res_label)
        results.point = str(1 if cor_label == res_label else 0)
        results.time = datetime.datetime.now()
        session.add(results)
        session.commit()
        session.close()
        return 'Registered.'

    def history(self):
        result = session.query(Results).all()
        result = [[i.id, i.username, i.correctlabel, i.result_label, i.point, str(i.time)] for i in result]
        return result

    def rank(self):
        result = Engine.execute('SELECT username, COUNT(point=1 or NULL) AS cor, COUNT(id) AS all, CAST(COUNT(point = 1 or NULL) AS FLOAT)/CAST(COUNT(id) AS FLOAT) * 100 AS acc FROM results GROUP BY username ORDER BY acc DESC;')
        result = [[s+1, i.username, i.cor, i.all, round(i.acc, 1)] for s, i in enumerate(result)]
        return result