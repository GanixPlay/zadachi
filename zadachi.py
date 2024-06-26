from flask import Flask, url_for, request, render_template, redirect, abort
import json
import base64
from data import db_session, user_resource, jobs_resource, jobs_api, one_job, users_api
from data.db_session import global_init, create_session
from data.jobs import Jobs
from data.users import User
from data.departaments import Department
from data.category import Category
from forms.user import RegisterForm
from forms.job_form import JobForm
from forms.login import LoginForm
from forms.depart_form import DepartForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


@app.route('/index')
@app.route('/')
def index():
    title = 'Главная'
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('jobs.html', jobs=jobs)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message='Такой пользователь уже есть')

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return render_template('register.html', form=form, message='Пользователь успешно зарегестрирован')
    return render_template('register.html', form=form)


@app.route('/new_job', methods=['GET', 'POST'])
def new_job():
    form = JobForm()
    if form.validate_on_submit():
        sess = db_session.create_session()

        if sess.query(Jobs).filter(Jobs.job == form.job.data).first():
            return render_template('add_job.html', form=form, message='Такая работа уже есть')

        job = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        category = Category(
            name=form.categories.data
        )
        job.categories.append(category)
        sess.add(job)
        sess.commit()
        return redirect('/')
    return render_template('add_job.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        user = sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        else:
            return render_template('login.html', message='Неверно', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/new_job/<int:id>', methods=['GET', 'POST'])
@login_required
def job_edit(id):
    form = JobForm()
    if request.method == 'GET':
        sess = db_session.create_session()
        job = sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
        if job or current_user.id == 1:
            form.job.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
        else:
            abort(404)
    if form.validate_on_submit():
        sess = db_session.create_session()
        job = sess.query(Jobs).filter(Jobs.id == id, Jobs.team_leader == current_user.id).first()
        if job or current_user.id == 1:
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            sess.commit()
            return redirect('/')
        else:
            abort(404)

    return render_template('add_job.html', form=form)


@app.route('/job_delete/<int:id>')
@login_required
def delete_job(id):
    sess = db_session.create_session()
    job = sess.query(Jobs).filter(Jobs.id == id).first()
    if job:
        sess.delete(job)
        sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/departments')
def departments():
    sess = db_session.create_session()
    departs = sess.query(Department).all()
    return render_template('departments.html', departs=departs)


@app.route('/new_department', methods=['GET', 'POST'])
def new_department():
    form = DepartForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        depart = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )
        sess.add(depart)
        sess.commit()
        return redirect('/departments')
    return render_template('add_depart.html', form=form)


@app.route('/new_department/<int:id>', methods=['GET', 'POST'])
def edit_depart(id):
    form = DepartForm()
    if request.method == 'GET':
        sess = db_session.create_session()
        job = sess.query(Department).filter(Department.id == id, Department.chief == current_user.id).first()
        if job:
            form.title.data = job.title
            form.chief.data = job.chief
            form.members.data = job.members
            form.email.data = job.email
        else:
            abort(404)
    if form.validate_on_submit():
        sess = db_session.create_session()
        job = sess.query(Department).filter(Department.id == id, Department.chief == current_user.id).first()
        if job:
            job.title = form.title.data
            job.chief = form.chief.data
            job.members = form.members.data
            job.email = form.email.data
            sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('add_depart.html', form=form)


@app.route('/delete_depart/<int:id>')
def delete_depart(id):
    sess = db_session.create_session()
    job = sess.query(Department).filter(Department.id == id, Department.chief == current_user.id).first()
    if job:
        sess.delete(job)
        sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    user_data = requests.get(f'http://127.0.0.1:8080/api/users/{user_id}').json()
    name = user_data['users'][0]['name']
    surname = user_data['users'][0]['surname']
    city = user_data['users'][0]['city_from']
    zapros = f'http://geocode-maps.yandex.ru/1.x/?apikey={KEY}&geocode={city}&format=json'

    response = requests.get(zapros)
    if response:
        response = response.json()
        toponim = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        coords = toponim['Point']['pos']
        coords = coords.split()

    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}&spn=0.1,0.1&l=map"
    response = requests.get(map_request)
    return render_template('users_show.html', name=name, surname=surname,
                           image=base64.b64encode(response.content).decode("ascii"))


def main():
    db_session.global_init('db/jobs1.db')
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(one_job.blueprint)
    app.register_blueprint(users_api.blueprint)
    api.add_resource(user_resource.UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(user_resource.UserListResource, '/api/v2/users/')
    api.add_resource(jobs_resource.JobsResource, '/api/v2/jobs/<int:job_id>')
    api.add_resource(jobs_resource.JobsListResource, '/api/v2/jobs/')
    app.run('127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
