import flask
from . import db_session
from .users import User
from flask import request, make_response, jsonify

blueprint = flask.Blueprint(
    'get_user',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    d = {}
    sess = db_session.create_session()
    req = sess.query(User).all()
    return flask.jsonify({'users': [item.to_dict(only=('id', 'name', 'surname')) for item in req]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    sess = db_session.create_session()
    req = sess.query(User).get(user_id)
    if not req:
        return flask.jsonify({'error': 'no such id'})
    else:
        return flask.jsonify({
            'users': [
                req.to_dict()
            ]
        })


@blueprint.route('/api/users', methods=['POST'])
def post_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    sess = db_session.create_session()
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        city_from=request.json['city_from']
    )
    user.set_password(request.json['password'])
    sess.add(user)
    sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    sess = db_session.create_session()
    user = sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'not found'}), 404)
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.email = request.json['email']
    user.city_from = request.json['city_from']
    sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    sess = db_session.create_session()
    user = sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'not found'}), 404)
    sess.delete(user)
    sess.commit()
    return jsonify({'success': 'OK'})
