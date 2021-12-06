from flask import Flask
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:JlLa3166095@localhost:5432/postgres'
db = SQLAlchemy(app)



@app.route('/')
def hello():
    user_agent = request.headers.get('User-Agent')
    return 'Hello! I see you are using %s' % user_agent

class Ventas (db.Model):
    id = db.Column(db.Integer)
    nombre = db.Column(db.String(30))
    fecha = db.Column(db.Date, primary_key=True)
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
    def __repr__(self):
        return f'{self.fecha}'
db.create_all()

class VentaSchema(Schema):
    class Meta(Schema.Meta):
        model = Ventas
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    nombre = fields.String(required=True)
    fecha = fields.Date(required=True)


@app.route('/ventas/<fecha>', methods = ['GET'])
def get_ventas_fecha(fecha):
    get_ventas = Ventas.query.get(fecha)
    ventas_schema = VentaSchema()
    ventas = ventas_schema.dump(get_ventas)
    return make_response(jsonify({"Ventas": ventas}))    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) 