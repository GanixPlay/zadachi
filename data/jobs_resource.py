from flask import jsonify
from flask_restful import Resource, reqparse, abort

from . import db_session
from .jobs import Jobs
from .job_parser import parser


def abort_if_job_not_found(job_id):
    sess = db_session.create_session()
    job = sess.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f'Job {job_id} not found')


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        sess = db_session.create_session()
        job = sess.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict()})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        sess = db_session.create_session()
        job = sess.query(Jobs).get(job_id)
        sess.delete(job)
        sess.commit()
        return jsonify({'success delete': job_id})


class JobsListResource(Resource):
    def get(self):
        sess = db_session.create_session()
        jobs = sess.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict() for item in jobs]})

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        sess.add(job)
        sess.commit()
        return jsonify({'success': job.id})
