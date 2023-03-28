from flask import Flask, render_template, request, redirect, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_db'
app.config['SECRET_KEY'] = 'tastycakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

@app.route('/')
def show_all_cupcakes():
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes')
def all_cupcakes():
    all_cups = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cups)

@app.route('/api/cupcakes/<int:id>')
def show_cupcake(id):
    cupcake = Cupcake.query.get(id)
    cup = cupcake.serialize()
    return jsonify(cup=cup)

@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    new_cupcake = Cupcake(flavor=request.json['flavor'],
                          size=request.json['size'],
                          rating=request.json['rating'],
                          image=request.json['image']
                          )
    db.session.add(new_cupcake)
    db.session.commit()
    cup_json = jsonify(cupcake=new_cupcake.serialize())
    return (cup_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcakes(id):
    cupcake = Cupcake.query.get(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")

