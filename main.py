from flask import Flask, render_template, url_for , request
from flask_socketio import SocketIO
import sqlite3


def get_message():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM message ")
    msg = cur.fetchall()
    cur.close()
    con.close()
    return msg


def add_msg(info):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("INSERT INTO message(login,txt) VALUES(?,?)",(info["user_name"],info["message"]))
    con.commit()
    cur.close()
    con.close()



app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    msg = []
    list = get_message()
    for l in list:
        msg.append({"user":l[0],"msg":l[1]})
    return render_template('session.html',messages = msg)

def messageReceived(methods=['GET', 'POST']):
    print('ОК')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    add_msg(json)
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
