import functools
import click

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('/user/user.html')

@bp.route('/find', methods=['GET'])
def find():
    db = get_db()
    #주차장 렌트 기록 가져오기
    rent_history = db.execute(
            "select Sdate, Edate, Place_id FROM Sharing WHERE User_id = '" + session['user_id']+"'"
        ).fetchall()

    #주차장 리스트 가져오기
    place = db.execute(
        "SELECT Adr, Price FROM PARKING_PLACE"
    ).fetchall()

    return render_template('find.html', rent_history= rent_history, place=place)

@bp.route('/find', methods=['POST'])
def find_pro():
    #파라미터 가져오기
    ID = session['user_id']
    adr = request.form['adr']
    price = request.form['price']
    syear= request.form['syear']
    smonth= request.form['smonth']
    sday= request.form['sday']
    shour= request.form['shour']
    smin= request.form['smin']
    eyear= request.form['eyear']
    emonth= request.form['emonth']
    eday= request.form['eday']
    ehour= request.form['ehour']
    emin= request.form['emin']
    sdate= syear+'-'+smonth+'-'+sday+' '+shour+":"+smin+":00"
    edate= eyear+'-'+emonth+'-'+eday+' '+ehour+":"+emin+":00"
    db = get_db()
    #대여번호 받기
    rent_list = db.execute(
                "select SHARING_ID from SHARING order by SHARING_ID asc"
            ).fetchall()
    shanum = 1
    if(rent_list):
        for rent in rent_list:
            shanum+=1

    #주차장 정보 받기
    place_data = db.execute(
         "SELECT owner_id, place_id FROM PARKING_PLACE WHERE adr = '"+adr+"'"
    ).fetchone()

    owner = place_data[0]
    place = place_data[1]

    click.echo( "INSERT INTO SHARING VALUES ("+str(shanum)+", '"+sdate+"', '"+edate+"', '"+ID+"', '"+owner+"', "+str(place)+", "+str(price)+")")

    #대여 정보 넣기
    db.execute(
       "INSERT INTO SHARING VALUES ("+str(shanum)+", '"+sdate+"','"+edate+"', '"+ID+"', '"+owner+"', "+str(place)+", "+str(price)+")"
    )
    db.commit()
    return redirect(url_for('user.home'))

@bp.route('/valet', methods=['GET'])
def valet():
    db = get_db()
    #발렛 이용기록 가져오기
    valet_history = db.execute(
        "select Sdate, Edate, Place_id, status_now FROM Valet WHERE User_id = '" + session['user_id']+"'"
        ).fetchall()
    return render_template('/user/valet.html', valet_history=valet_history)

@bp.route('/valet', methods=['POST'])
def valet_ask():
    #파라미터 가져오기
    ID = session['user_id']
    adr = request.form['adr']
    price = request.form['price']
    smonth= request.form['smonth']
    sday= request.form['sday']
    smin= request.form['smin']
    eyear= request.form['eyear']
    emonth= request.form['emonth']
    eday= request.form['eday']
    ehour= request.form['ehour']
    emin= request.form['emin']
    sdate= syear+'-'+smonth+'-'+sday+' '+shour+":"+smin+":00"
    edate= eyear+'-'+emonth+'-'+eday+' '+ehour+":"+emin+":00"
    db = get_db()
    #대여번호 받기
    rent_list = db.execute(
                "select Valet_ID from Valet order by Valet_ID asc"
            ).fetchall()
    shanum = 1
    if(rent_list):
        for rent in rent_list:
            shanum+=1

    #대여 정보 넣기
    db.execute(
       "INSERT INTO VALET VALUES ("+str(shanum)+", '"+sdate+"','"+edate+"', '"+ID+"', '"+owner+"', '"+str(place)+"', 0, 0, 0)"
    )
    db.commit()
    return redirect(url_for('user.home'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view