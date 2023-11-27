from flask import Flask, request, make_response, jsonify,redirect
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy import text
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

import jwt 
import json ,re,os,random

import datetime

def validate_date(date_text):
	try:
		datetime.datetime.strptime(date_text,"%Y-%m-%d")
		return True
	except ValueError:
		print("Incorrect data format({0}), should be YYYY-MM-DD".format(date_text))
		return False

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:159357jim@localhost:3306/testdb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
SECRET_KEY = 'apple'
db = SQLAlchemy(app)

#테이블 생성

meta = MetaData()

db1 = Table(
   'users', meta, 
   Column('id', Integer, primary_key = True), 
   Column('userId', String(32)), 
   Column('userName', String(8)),
   Column('userPassword', String(64)),

   Column('birthday', String(32)),
   Column('gender', String(32)),
   Column('height', Integer),
   Column('weight', Integer),
)

db2 = Table(
   'exercises', meta, 
   Column('id', Integer, primary_key = True),
   Column('userId', String(32)), 
   Column('exerciseCount', Integer), 
   Column('exerciseDate', String(64)),
   Column('exerciseNo', Integer),
   Column('historyNo', Integer)
)

db3 = Table(
   'foods', meta, 
   Column('id', Integer, primary_key = True),
   Column('weight', Integer), 
   Column('foodName', String(64))
)

db3 = Table(
   'diet', meta, 
   Column('id', Integer, primary_key = True),
   Column('userId', String(32)),
   Column('diaryNo', Integer),
   Column('description', String(64)),
   Column('diaryDate',String(64)),
   Column('mealTime', String(64)), 
   Column('isShared', String(64)),
   Column('saveImagePath', String(64)),
   Column('dietList', String(1000)),
   Column('weight', Integer)

)

engine = create_engine('mysql+pymysql://root:159357jim@localhost:3306/testdb', echo = True)
meta.create_all(engine)
Session = sessionmaker(bind=engine)

#db 모듈에 접근
class User(db.Model):
    __tablename__ = 'users'   #테이블 이름 : users

    id = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    userId = db.Column(db.String(32))
    userName = db.Column(db.String(8))
    userPassword = db.Column(db.String(64))
    birthday = db.Column(db.String(32))
    gender = db.Column(db.String(32))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

class exercises(db.Model):
    __tablename__ = 'exercises'   #테이블 이름 : exercises

    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.String(32))
    exerciseCount = db.Column(db.Integer)
    exerciseDate = db.Column(db.String(64))
    exerciseNo = db.Column(db.Integer)
    historyNo = db.Column(db.Integer)

class diet(db.Model):
    __tablename__ = 'diet'
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.String(32))
    diaryNo = db.Column(db.Integer)
    description = db.Column(db.String(64))
    diaryDate = db.Column(db.String(64))
    mealTime = db.Column(db.String(64))
    isShared = db.Column(db.String(64))
    saveImagePath = db.Column(db.String(64))
    dietList = db.Column(db.String(1000))
    weight = db.Column(db.Integer)

class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column(db.Integer, primary_key = True)
    foodName = db.Column(db.String(64))
    weight = db.Column(db.Integer)


food_list = [
    {'foodName': '샐러드', 'weight': 100 ,'kcal':100,'fat':1,'protein':1,'carbohydrate':1},
    {'foodName': '사과', 'weight': 100 ,'kcal':100,'fat':1,'protein':1,'carbohydrate':1},
    {'foodName': '감자', 'weight': 100, 'kcal':100,'fat':1,'protein':1,'carbohydrate':1},
]

#로그인 페이지
@app.route('/users/auth/login', methods=['GET', 'POST', 'PUT', 'DELETE'])
def login():
    if request.method == 'POST':

        data_login = request.get_json()
        print(data_login)
        userid_login = data_login['userId']
        password_login = data_login['userPassword']
        
        data = User.query.filter(User.userId==userid_login ,User.userPassword==password_login).first()
        payload = {
			'id': userid_login,
		}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print(data)
        if data is not None:
            return jsonify({'result': 'success', 'userId':userid_login,'token': token})
        else:
            return KeyError



    if request.method == 'GET':
        print('GET')

    if request.method == 'PUT':
        print('PUT')

    if request.method == 'DELETE':
        print('DELETE')

    return make_response(jsonify({'status': True}), 200) 

#회원가입 페이지
@app.route('/users/user/register/signup', methods=['POST'])
def register():
    
    if request.method == 'POST':

        data_reg = request.get_json()

        userid_reg = data_reg['userId']
        password_reg = data_reg['userPassword']
        username_reg = data_reg['userName']


        new_user = User()
        new_user.userPassword = password_reg
        new_user.userId = userid_reg
        new_user.userName = username_reg

        db.session.add(new_user)
        db.session.commit()
        return data_reg
 
    return make_response(jsonify({'status': True}), 200)        

#정보 조회
@app.route('/users/user/find/me', methods=['GET'])
def myapi():
    if request.method == 'GET':
        
        access_token=request.headers.get('Authorization')
        payload=jwt.decode(access_token, SECRET_KEY, "HS256")

        id_data=payload['id']
       

        session = Session()
        my_data = session.query(User).filter(User.userId == id_data).first()
        #print(my_data.userPassword)

        my_userId = my_data.userId
        my_userPassword = my_data.userPassword
        my_userEmail = 'test@test.org'
        my_userName = my_data.userName
        my_gender = my_data.gender
        my_height = my_data.height
        my_weight = my_data.weight
        my_birthday = my_data.birthday
        my_isLogin = True

        return jsonify({'userId': my_userId, 'userPassword':my_userPassword,'userEmail': my_userEmail,'userName': my_userName,'gender': my_gender,'height': my_height,'weight': my_weight,'birthday': my_birthday,'isLogin': my_isLogin})

    return make_response(jsonify({'status': True}), 200) 

#유저정보 업데이트
@app.route('/users/user/register/AdditionalInfo', methods=['POST','PUT'])
def update1():
    
    if request.method == 'POST':
        access_token=request.headers.get('Authorization')
        payload=jwt.decode(access_token, SECRET_KEY, "HS256")
        id_data=payload['id']
        data_up = request.get_json()

        birthday_up = data_up['birthday']
        gender_up = data_up['gender']
        height_up = data_up['height']
        usernameweight_up = data_up['weight']

        shop_name = db.session.query(User).filter(User.id == id_data).update({'birthday': birthday_up,'gender': gender_up,'height': height_up,'weight': usernameweight_up})
        db.session.commit()

        return data_up
 
    return make_response(jsonify({'status': True}), 200)        

@app.route('/users/user/update', methods=['PUT'])
def update2():
    if request.method == 'PUT':
        data_up = request.get_json()
       
        userPassword_up = data_up['userPassword']

        birthday_up = data_up['birthday']
        gender_up = data_up['gender']
        height_up = data_up['height']
        usernameweight_up = data_up['weight']

        db.session.query(User).filter(User.userPassword == userPassword_up).update({'birthday': birthday_up,'gender': gender_up,'height': height_up,'weight': usernameweight_up})
        db.session.commit()
        return data_up



#비밀번호 체크
@app.route('/users/user/checkPassword', methods=['POST'])
def psCheck():
    pswd_ch = request.args.get('userPassword')
    
    data_ch = User.query.filter(User.userId==pswd_ch).first()

    if data_ch is not None:
        doc ={'data':False}
        return doc
    else:
        doc ={'data':True}
        return doc
    
#아이디 중복 체크
@app.route('/users/user/idCheck/', methods=['GET'])
def idCheck():
    user_ch = request.args.get('user')

    data_ch = User.query.filter(User.userId==user_ch).first()

    if data_ch is not None:
        doc ={'data':False}
        return doc
    else:
        doc ={'data':True}
        return doc

#운동등록
@app.route('/users/exerciseHistory/register', methods=['POST'])
def exerciseHistory():
    access_token=request.headers.get('Authorization')
    payload=jwt.decode(access_token, SECRET_KEY, "HS256")

    #print(payload)
    exer_data = request.get_json()
    id_data=payload['id']
    exerciseCount_data = exer_data['exerciseCount']
    exerciseDate_data = exer_data['exerciseDate']
    exerciseNo_data = exer_data['exerciseNo']
    historyNo_data = exer_data['historyNo']

    new_data = exercises()
    new_data.userId = id_data
    new_data.exerciseCount = exerciseCount_data
    new_data.exerciseDate = exerciseDate_data
    new_data.exerciseNo = exerciseNo_data
    new_data.historyNo = historyNo_data

    db.session.add(new_data)
    db.session.commit()
    return make_response(jsonify({'status': True}), 200)

#운동 기록 조회
@app.route('/users/exerciseHistory/findAll/', methods=['GET'])
def history_ch():
    year = request.args.get('year')
 
    access_token=request.headers.get('Authorization')
    payload=jwt.decode(access_token, SECRET_KEY, "HS256")

    id_data=payload['id']
    
    session = Session()

    result = session.query(exercises).filter(exercises.userId==id_data).all()
    
    exercise_history_list=[]
    
    ExerciseTypedict = {
    '1':'사이드 레터럴 레이즈',
    '2':'윗몸일으키기',
    '3':'턱걸이',
    '4':'팔굽혀펴기',
    '5':'스쿼트',
    '6':'런지',
    }

    for r in result:
        exercise_history = {
        'exerciseName': ExerciseTypedict[str(r.exerciseNo)],
        'exerciseCount': r.exerciseCount,
        'exerciseDate': r.exerciseDate
        }
        exercise_history_list.append(exercise_history)
    #print(exercise_history_list)

    return exercise_history_list
    

# Image Segmentation Endpoint
@app.route('/users/dietdiary/segmentation', methods=['POST'])
def my_diet_image_api():
    # Dummy image segmentation logic
    return jsonify({"result": "Image segmented successfully"})

# Diet Entry Registration Endpoint
@app.route('/users/dietdiary/register', methods=['POST'])
def my_diet_register_api():
    
    access_token=request.headers.get('Authorization')
    payload=jwt.decode(access_token, SECRET_KEY, "HS256")
    id_data=payload['id']

    json_data = request.files['key'].read()
    json_data = json.loads(json_data.decode('utf-8'))

    file = request.files.get('file')
    file_path=''
    filename=''
    if file:
        filename=file.filename
        file_path = os.path.join('../front/public/img/', filename)
        file.save(file_path)
    

    #matches = re.search(r'name="key"; filename="blob"\r\nContent-Type: application/json\r\n\r\n(.+?)\r\n------WebKitFormBoundary', raw_data, re.DOTALL)
    #if matches:
        #json_str = matches.group(1)
        #json_data = json.loads(json_str)
    print(json_data)

    original_list = json_data['dietRegisterReqList']

    additional_data = {'kcal': 100, 'fat': 4, 'protein': 4, 'carbohydrate': 4}

    updated_list = [dict(food, **additional_data) for food in original_list]
    print(updated_list)
    #updated_list.append({'foodName': 'potato', 'weight': 100, **additional_data})
    #print(updated_list)
    description = json_data['description']
    diary_date = json_data['diaryDate']
    diaryNo = random.randint(1000, 9999)
    weight = json_data['dietRegisterReqList'][0]['weight']
    is_shared = json_data['isShared']
    meal_time = json_data['mealTime']
    dietList = str(updated_list)
    save_image_path = filename

    new_data = diet()
    new_data.userId = id_data
    new_data.diaryNo = diaryNo
    new_data.description = description
    new_data.diaryDate = diary_date
    new_data.mealTime = meal_time
    new_data.isShared = is_shared
    new_data.saveImagePath = save_image_path
    new_data.dietList = dietList
    new_data.weight = weight

    db.session.add(new_data)
    db.session.commit()
    
    return jsonify({"result": "Diet entry registered successfully"})

# Diet Entries List Endpoint
@app.route('/users/dietdiary/findAll', methods=['GET'])
def my_diet_diary_list_api():
    access_token=request.headers.get('Authorization')
    payload=jwt.decode(access_token, SECRET_KEY, "HS256")

    id_data=payload['id']
    
    session = Session()

    result = session.query(diet).filter(diet.userId==id_data).all()
    diet_history_list=[]
    food_list_eat=[]
    for r in result:
        data_string = r.dietList
        food_list_eat = json.loads(data_string.replace("'", "\""))

        data = {
            'diary_no': r.diaryNo,
            'description': r.description,
            'diary_date': r.diaryDate,
            'meal_time': r.mealTime,
            'isShared': r.isShared,
            'imagePath': r.saveImagePath,
            'weight': r.weight,
            'dietFindResList': food_list_eat
            }
        diet_history_list.append(data)
    print(diet_history_list)

    return diet_history_list

# Delete Diet Entry Endpoint
@app.route('/users/dietdiary/remove/<arg>', methods=['DELETE'])
def my_diet_diary_item_delete_api(arg):
    diaryNo = arg
    session = Session()

    session.query(diet).filter(diet.diaryNo == diaryNo).delete()

    session.commit()

    return jsonify({"result": "Diet entry deleted successfully"})

# Retrieve Detailed Diet Entry Information Endpoint
@app.route('/users/dietdiary/findAll/<arg>', methods=['GET'])
def my_diet_detail_api(arg):
    if validate_date(arg):
        diaryDate = arg
        
        access_token=request.headers.get('Authorization')
        payload=jwt.decode(access_token, SECRET_KEY, "HS256")

        id_data=payload['id']
        
        session = Session()
        diaryDate = diaryDate.date() if hasattr(diaryDate, 'date') else diaryDate

        result = session.query(diet).filter(func.date(diet.diaryDate) == diaryDate,diet.userId==id_data).all()
        diet_history_list=[]
        
        for r in result:
            data_string = r.dietList
            food_list_eat = json.loads(data_string.replace("'", "\""))

            data = {
                'diaryNo': r.diaryNo,
                'description': r.description,
                'diaryDate': r.diaryDate,
                'mealTime': r.mealTime,
                'isShared': r.isShared,
                'imagePath': r.saveImagePath,
                'weight': r.weight,
                'dietFindResList': food_list_eat
                }
            diet_history_list.append(data)
        print(diet_history_list)

        return diet_history_list
@app.route('/users/dietdiary/find/<arg>', methods=['GET'])
def my_diet_detail_api_2(arg):
    diaryNo = arg
    session = Session()

    r = session.query(diet).filter(diet.diaryNo == diaryNo).first()

    data_string = r.dietList
    food_list_eat = json.loads(data_string.replace("'", "\""))

    print(food_list_eat)
    print(r.saveImagePath)
    diet_history_list={
        'diaryNo': r.diaryNo,
        'description': r.description,
        'diaryDate': r.diaryDate,
        'mealTime': r.mealTime,
        'isShared': r.isShared,
        'imagePath': r.saveImagePath,
        'weight': r.weight,
        'dietFindResList': food_list_eat
        }
    
    #print(diet_history_list)

    return jsonify(diet_history_list)
    
# Retrieve List of All Foods Endpoint
@app.route('/users/food/findAll', methods=['GET'])
def food_list_api():
    return jsonify(food_list)



if __name__ == "__main__":
    app.run(debug = True)
    #app.run(host = 'localhost',port = 5000)