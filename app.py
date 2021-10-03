"""Flask app for Cupcakes"""

from flask import Flask, request, render_template,  redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, Cupcake, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def index_page():
    """show an empty form with javascript"""
    return render_template('index.html')


@app.route('/api/cupcakes')
def all_cupcakes():
    """get a list of all cupcakes and return in json"""

    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def a_cupcake(id):
    """get data on one cupcake and return json"""

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """create a new cupcake from json"""

    new_cupcake = Cupcake(flavor=request.json['flavor'], size=request.json['size'], rating=request.json['rating'], image=request.json['image'])
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    
    return response_json,201

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """update a cupcake"""

    cupcake = Cupcake.query.get_or_404(id)
    request.json
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """delete a cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='deleted')


