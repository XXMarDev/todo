import datetime

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from utilies import array_toJson

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/todo"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
sql = SQLAlchemy(app)
CORS(app)


class Task(sql.Model):
    id_task = sql.Column(sql.Integer, primary_key=True)
    completato = sql.Column(sql.Boolean)
    titolo = sql.Column(sql.String(20))
    data_creazione = sql.Column(sql.Date)
    descrizione = sql.Column(sql.String(150))

    def __init__(self, titolo, descrizione):
        self.completato = False
        self.titolo = titolo
        self.data_creazione = datetime.date.today()
        self.descrizione = descrizione

    def to_json(self):
        return {
            "id_task": self.id_task,
            "completato": self.completato,
            "titolo": self.titolo,
            "data_creazione": str(self.data_creazione),
            "descrizione": self.descrizione
        }

@app.get('/get_taskT/<titolo>')
def get_taskT(titolo):
    lista_task = sql.session.query(Task).filter(Task.titolo.like('%' + titolo + '%')).all()
    sql.session.commit()
    return array_toJson(lista_task)

@app.get('/get_taskD/<descrizione>')
def get_taskD(descrizione):
    lista_task = sql.session.query(Task).filter(Task.descrizione.like('%' + descrizione + '%')).all()
    sql.session.commit()
    return array_toJson(lista_task)

@app.post('/create_task')
def create_task():
    task = Task(request.json['titolo'], request.json['descrizione'])
    sql.session.add(task)
    sql.session.commit()
    return task.to_json()

@app.put('/complete_task/<id_task>')
def complete_task(id_task):
    task = sql.session.query(Task).filter(Task.id_task == id_task).first()
    task.completato = True
    sql.session.commit()
    return task.to_json()
@app.delete('/delete_task/<id_task>')
def delete_task(id_task):
    task = sql.session.query(Task).filter(Task.id_task == id_task).delete()
    sql.session.commit()
    return {
        "messagge": "Task eliminata con successo"
    }

with app.app_context():
    sql.create_all()
    app.run()
