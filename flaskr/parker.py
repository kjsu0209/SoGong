import functools
import click

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('parker', __name__, url_prefix='/parker')

@bp.route('/valet', methods=['GET'])
def home():
    db = get_db()
    #발렛 이용기록 가져오기
    valet_history = db.execute(
        "select Sdate, Edate, pickup, fee FROM Valet WHERE Parker_id = '" + session['user_id']+"'  order by Sdate asc"
        ).fetchall()
    #발렛 요청 가져오기
    valet_ask = db.execute(
        "select Sdate, Edate, pickup, valet_id FROM Valet WHERE Parker_id = 'none' and Place_ID=0"
    ).fetchall()
    return render_template('/parker/valet.html', valet_history=valet_history, valet_ask=valet_ask)

@bp.route('/valet_ok', methods=['GET'])
def valet_ok():
    db = get_db()
    ID = session['user_id']
    valet_id = request.args.get('id')
    #발렛 요청 수락하기
    db.execute(
        "UPDATE VALET SET parker_id='" + ID + "' WHERE valet_ID='"+valet_id+"'"
    )
    db.commit()
    return redirect(url_for('parker.find'))

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

    return render_template('/parker/find.html', rent_history= rent_history, place=place)

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
         "SELECT owner_id, place_id, price FROM PARKING_PLACE WHERE adr = '"+adr+"'"
    ).fetchone()

    owner = place_data[0]
    place = place_data[1]

    #대여 정보 넣기
    db.execute(
       "INSERT INTO SHARING VALUES ("+str(shanum)+", '"+sdate+"','"+edate+"', '"+ID+"', '"+owner+"', "+str(place)+", "+str(price)+")"
    )
    db.commit()

    #발렛 정보 갱신
    db.execute(
        "UPDATE VALET SET Place_ID="+str(place)+", fee='"+str(price)+"', status_now= 1 WHERE parker_ID='"+ID+"' and status_now=0"
    )
    db.commit()

    return redirect(url_for('parker.home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view