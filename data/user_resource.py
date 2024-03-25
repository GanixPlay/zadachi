from flask import jsonify
from flask_restful import Resource, reqparse, abort

from . import db_session
from .users import User
from .user_parser import parser

def abort_if_user_not_found(user_id):
    sess = db_session.create_session()
    user = sess.query(User).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        return jsonify({'user': user.to_dict(only=('name', 'surname', 'age'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        sess.delete(user)
        sess.commit()
        return jsonify({'delete success': user_id})


class UserListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        news = sess.query(User).all()
        return jsonify({'user': [item.to_dict(only=('name', 'surname', 'position')) for item in news]})

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email']
        )
        user.set_password(args['hashed_password'])
        sess.add(user)
        sess.commit()
        sess.close()
        return jsonify({'user': 'OK'})
