import base64
import os
import csv
from flask import Blueprint, redirect, url_for, render_template, request, flash, send_file
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from . import db
from .models import Contacts

view = Blueprint('view', __name__)

IMAGE_DIR = 'C:\\Users\\DieTer HellStorm\\Documents\\skempire\\application\\static\\images'


@view.route('/')
def index():
    return render_template('index.html')


@view.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@view.route('/dash')
@login_required
def dash():
    user = current_user.id
    contacts = Contacts.query.filter_by(user_id=user).all()
    return render_template('contacts.html', user=current_user, data=contacts)


@view.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    user = current_user.id
    contacts = Contacts.query.filter_by(user_id=user).all()
    return render_template('manage.html', user=current_user, data=contacts)


@view.route('/update/<uid>', methods=['POST'])
def update(uid):
    if request.method == 'POST':
        name = request.form.get('name')
        typ = request.form.get('type')
        phone = request.form.get('phone')
        email = request.form.get('email')
        com = request.form.get('com')
        pic = request.files['pic']
        if pic:
            pic_name = secure_filename(pic.filename)
            pic_savename = "images/" + pic_name
            pic_path = os.path.join(IMAGE_DIR, pic_name)
            pic.save(pic_path)
        else:
            row = Contacts.query.filter_by(id=uid).first()
            pic_savename = row.pic_name
            pic_path = row.pic_path
        data = Contacts.query.filter_by(id=uid).first()
        data.name = name
        data.type = typ
        data.phone = phone
        data.email = email
        data.com = com
        data.pic_name = pic_savename
        data.pic_path = pic_path
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
            pic_savename = "images/"+pic_name
            pic_path = os.path.join(IMAGE_DIR, pic_name)
            pic.save(pic_path)
        new_contact = Contacts(name=name, type=type, phone=phone, email=email, com=com, pic_name=pic_savename, pic_path=pic_path, user_id=user_id)
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
    if request.method == 'POST':
        fileN = request.form.get('fileName')
        fileName = fileN+'.csv'
        csv_data = "Name, Type, Phone, Email, Company, \n"
        contacts = Contacts.query.filter_by(user_id=current_user.id).all()
        for c in contacts:
            csv_data += f"{c.name}, {c.type}, {c.phone}, {c.email}, {c.com}, \n"
        with open(fileName, "w") as csv_file:
            csv_file.write(csv_data)
        return send_file('../'+fileName, as_attachment=True, download_name=fileName)
    return render_template('impexp.html', user=current_user)


@view.route('/import', methods=['POST'])
def importfile():
    if request.method == 'POST':
        uploadFile = request.files['upload_file']
        filename = secure_filename(uploadFile.filename)
        path = os.path.join(UPLOAD_DIR, filename)
        uploadFile.save(path)
        with open(os.path.join(UPLOAD_DIR, filename), 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for read in reader:
                new_con = Contacts(name=read[0], type=read[1], phone=read[2], email=read[3], com=read[4], user_id=current_user.id)
                db.session.add(new_con)
                db.session.commit()
            flash('Data Imported', category='success')
            return redirect(url_for('view.impexp'))
    return redirect(url_for('view.impexp'))
