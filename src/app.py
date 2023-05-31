"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorite
# from models import user

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def handle_hello():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    """
    Single user
    """

    user1 = User.query.get(user_id)
    return jsonify(user1.serialize()), 200

    return "Invalid Method", 404


@app.route('/people', methods=['GET'])
def handle_people():

    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))

    return jsonify(all_people), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_people(people_id):
    """
    Single people
    """
    people1 = People.query.get(people_id)
    if people1 is None:
        raise APIException("User not found", status_code=404)
    return jsonify(people1.serialize()), 200


@app.route('/planets', methods=['GET'])
def handle_planets():

    planets = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_planets), 200


@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_single_planets(planets_id):
    """
    Single planets
    """
    planets1 = Planets.query.get(planets_id)
    if planets1 is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planets1.serialize()), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return 'User noy found', 404
    favorites = [favorite.serialize() for favorite in user.favorites]
    return jsonify(favorites), 200


@app.route('/favorite/user/planet', methods=['POST'])
def add_favorite_planet():
    data = request.get_json()
    planets_id = data['planets_id']
    user_id = data['user_id']

    user = User.query.get(user_id)
    planets = Planets.query.get(planets_id)
    new_favorite = Favorite(user=user, planets=planets)

    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        'msg': 'Planet has been added.'}
    return jsonify(response_body), 200


@app.route('/favorite/user/people', methods=['POST'])
def add_favorite_people():
    data = request.get_json()
    people_id = data['people_id']
    user_id = data['user_id']

    user = User.query.get(user_id)
    people = People.query.get(people_id)
    new_favorite = Favorite(user=user, people=people)

    db.session.add(new_favorite)
    db.session.commit()

    response_body = {
        'msg': 'Character has been added.'}

    return jsonify(response_body), 200


@app.route('/favorite/user/people', methods=['DELETE'])
def delete_favorite_people():

    data = request.get_json()
    people_id = data['people_id']
    user_id = data['user_id']

    user = User.query.get(user_id)
    people = People.query.get(people_id)

    delete_favorite = Favorite.query.filter_by(
        user=user, people=people).first()

    if delete_favorite is None:
        return jsonify({'msg': 'No favorite found'}), 404

    db.session.delete(delete_favorite)
    db.session.commit()

    response_body = {'msg': 'Your character has been deleted'}, 200
    return jsonify(response_body)


@app.route('/favorite/user/planets', methods=['DELETE'])
def delete_favorite_planets():

    data = request.get_json()
    planets_id = data['planets_id']
    user_id = data['user_id']

    user = User.query.get(user_id)
    planets = Planets.query.get(planets_id)

    delete_favorite = Favorite.query.filter_by(
        user=user, planets=planets).first()

    if delete_favorite is None:
        return jsonify({'msg': 'No favorite found'}), 404

    db.session.delete(delete_favorite)
    db.session.commit()

    response_body = {'msg': 'Your planet has been deleted'}, 200
    return jsonify(response_body)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
