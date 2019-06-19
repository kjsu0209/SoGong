import functools
import click

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('owner', __name__, url_prefix='/owner')

@bp.route('/', methods=['GET'])
def find():
    db = get_db()
    #주차장 렌트 기록 가져오기
    rent_history = db.execute(
            "SELECT Place_id,id,name,phone,Sdate,Edate FROM User_sp,SHARING WHERE User_id = id and Owner_id = '"+session['user_id']+"'"
        ).fetchall()

    #주차장 리스트 가져오기
    my_place = db.execute(
        "SELECT Place_id,Adr,Price FROM PARKING_Place WHERE Owner_Id = '" + session['user_id'] + "'"
    ).fetchall()

    return render_template('owner/add_place.html', rent_history= rent_history, my_place=my_place)
@bp.route('/add_place', methods=['POST'])
def add_place():
    db = get_db()
    plcnum = 1
    ID = session['user_id']
    adr = request.form['adr']
    price = request.form['price']

    #주차장 번호 설정
    plc_list = db.execute(
                "select Place_ID from PARKING_PLACE order by Place_ID desc"
            ).fetchall()
    if(plc_list):
        for rent in plc_list:
            plcnum+=1
    #주차장 생성
    db.execute( 
        "INSERT INTO PARKING_PLACE VALUES ("+str(plcnum)+", '"+ID+"','"+adr+"',"+str(price)+")" 
         )
    db.commit()
    return redirect(url_for('owner.find'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view