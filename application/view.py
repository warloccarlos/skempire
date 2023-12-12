import base64
from flask import Blueprint, redirect, url_for, render_template, request, flash, send_file
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from . import db
from .models import Contacts

view = Blueprint('view', __name__)


@view.route('/')
def index():
    return render_template('index.html')


@view.route('/dash')
@login_required
def dash():
    user = current_user.id
    contacts = Contacts.query.filter_by(user_id=user).all()
    images = []
    names = []
    data = {}
    for c in contacts:
        names.append(c.name)
        image_data = c.pic
        image = base64.b64encode(image_data).decode('ASCII')
        images.append(image)
    data = dict(zip(names, images))
    return render_template('contacts.html', user=current_user, data=data)


@view.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    user = current_user.id
    contacts = Contacts.query.filter_by(user_id=user).all()
    return render_template('manage.html', user=current_user, data=contacts)


@view.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        name = request.form.get('name')
        typ = request.form.get('type')
        phone = request.form.get('phone')
        email = request.form.get('email')
        com = request.form.get('com')
        data = Contacts.query.filter_by(id=id).first()
        data.name = name
        data.type = typ
        data.phone = phone
        data.email = email
        data.com = com
        db.session.commit()
        flash('Contact updated', category='success')
    return redirect(url_for('view.manage'))


@view.route('/delcon/<id>', methods=['POST'])
def delcon(id):
    if request.method == 'POST':
        Contacts.query.filter_by(id=id).delete()
        db.session.commit()
        flash('Contact deleted', category='success')
    return redirect(url_for('view.manage'))


@view.route('/addnew', methods=['GET', 'POST'])
@login_required
def addnew():
    if request.method == 'POST':
        user_id = current_user.id
        fName = request.form.get('fName')
        lName = request.form.get('lName')
        name = fName + ' ' + lName
        type = request.form.get('type')
        phone = request.form.get('conNumber')
        email = request.form.get('conEmail')
        com = request.form.get('conCom')
        pic = request.files['conPic']
        if pic:
            pic_name = secure_filename(pic.filename)
        new_contact = Contacts(name=name, type=type, phone=phone, email=email, com=com, pic_name=pic_name, pic=pic.read(), user_id=user_id)
        db.session.add(new_contact)
        db.session.commit()
        flash('Contact saved', category='success')
        return redirect(url_for('view.dash'))
    return render_template('addnew.html', user=current_user)


@view.route('/about')
def about():
    return render_template('about.html')

@view.route('/impexp', methods=['GET', 'POST'])
def impexp():
    return render_template('impexp.html', user=current_user)
