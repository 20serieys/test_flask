from flask import Flask, render_template 
from flask_socketio import SocketIO
from game_backend import Game
import json

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()


@app.route("/")
def index():
    map = game.getMap()
    stats = game.getStat() #permet d'accéder aux stats du joueur
    return render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]), PV_1=stats[0], money_1=stats[1], protection_1=stats[2], PV_2=stats[3], money_2=stats[4], protection_2=stats[5])

@socketio.on("move_1")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    dx = json['dx']
    dy = json["dy"]

    data, ret = game.move_1(dx,dy)
    
    #déplacements des monstres:
    data_monsters = game.move_monsters()
    for elt in data_monsters:
        data.append(elt[0])
        data.append(elt[1])
    

    #Prise en compte des stats du joueur:
    stats = game.getStat()
    data.append(stats[0])
    data.append(stats[1])
    data.append(stats[2])
    data.append(stats[3])
    data.append(stats[4])
    data.append(stats[5])

    if ret:
        print(data)
        socketio.emit("response", data)
    
@socketio.on("move_2")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    dx = json['dx']
    dy = json["dy"]

    data, ret = game.move_2(dx,dy)
    
    #déplacements des monstres:
    data_monsters = game.move_monsters()
    for elt in data_monsters:
        data.append(elt[0])
        data.append(elt[1])
    

    #Prise en compte des stats du joueur:
    stats = game.getStat()
    data.append(stats[0])
    data.append(stats[1])
    data.append(stats[2])
    data.append(stats[3])
    data.append(stats[4])
    data.append(stats[5])

    if ret:
        print(data)
        socketio.emit("response", data)

@socketio.on("save")
def on_save_msg():
    print("received save message")
    data_save = game.set_save()
    socketio.emit("save_response", json.dumps(data_save))

@socketio.on("charge")
def on_charge_msg(charge):
    print("received charge message")
    data_charge = json.loads(charge)
    game.charge(data_charge)


if __name__=="__main__":
    socketio.run(app, port=5001)




