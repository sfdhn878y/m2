import jwt
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'exam-portal-secret'
db = SQLAlchemy(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    role = db.Column(db.String(100),nullable=False) # studnet , examinor , admin
    is_blocked = db.Column(db.Boolean,default=False)



class User_profile(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    address = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(100),nullable=False)
    past_experience = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,unique=True)


class Staff_Profile(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    address = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(100),nullable=False)
    past_experience = db.Column(db.String(100),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,unique=True)



class Course(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    coures_name = db.Column(db.String(100),nullable=False)
    coures_description = db.Column(db.String(100),nullable=False)
    course_duration = db.Column(db.Integer,nullable=False)




class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(100), nullable=False)
    exam_description = db.Column(db.String(100), nullable=False)
    examinor_slot_create_start_date = db.Column(db.String(100), nullable=False)
    examinor_slot_create_end_date = db.Column(db.String(100), nullable=False)
    booking_start_time = db.Column(db.String(100), nullable=False)
    booking_end_time = db.Column(db.String(100), nullable=False)
    exam_start_date = db.Column(db.String(100), nullable=False)
    exam_end_date = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)
    examinor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete='CASCADE'), nullable=False)


class Rubric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    criterion = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete='CASCADE'), nullable=False)




@app.route('/register',methods=['POST'])
def register():
    data = request.json
    old_user = User.query.filter_by(email=data['email']).first()
    if old_user:
        return jsonify({'message': 'User already exists'})
    new_user = User(name=data['username'], email=data['email'], password=data['password'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': data})



@app.route('/login',methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'User not found'})
    if user.password != data['password']:
        return jsonify({'message': 'Invalid password'})
    if user.is_blocked:
        return jsonify({'message': 'User is blocked'})

    token = jwt.encode(
        {
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
          
        },
        app.config['SECRET_KEY'],
       
    )
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'role': user.role,
        'name': user.name
    })


@app.route('/create_course',methods=['POST'])
def create_course():
    data = request.json
    print(data)
    new_course = Course(coures_name=data['courseName'], coures_description=data['courseDescription'], course_duration=data['courseDuration'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Course created successfully'})

@app.route('/provide_examinor_details',methods=['POST','GET'])
def provide_examinor_details():
    all_examinors_list = []

    all_examinors = User.query.filter_by(role='examinor').all()             # i hve to fixed it latae i have to use.filter_by(role='examinor')
    for examinor in all_examinors:
            all_examinors_list.append(
                {
                    'id': examinor.id,
                    'name': examinor.name,
                    'email': examinor.email,
                    'role': examinor.role,
                    'is_blocked': examinor.is_blocked
                }
            )
    return jsonify({'data': all_examinors_list})




@app.route('/provide_course_details',methods=['POST'])
def provide_course_details():
    all_courses_list = []
    all_courses = Course.query.all()
    for course in all_courses:
        all_courses_list.append(
            {
                'id': course.id,
                'name': course.coures_name,
                'description': course.coures_description,
                'duration': course.course_duration
            }
        )
    return jsonify({'data': all_courses_list})

@app.route('/get_course_data_specific/<int:id>',methods=['POST'])
def get_course_data_specific(id):
   
    course = Course.query.filter_by(id=id).first()
   
    return jsonify({'data': {
        'name': course.coures_name,
        'description': course.coures_description,
        'duration': course.course_duration
    }}) 



@app.route('/edit_course/<int:id>',methods=['POST'])
def edit_course(id):
    data = request.json
    course = Course.query.filter_by(id=id).first()
    course.coures_name = data['name']
    course.coures_description = data['description']
    course.course_duration = data['duration']
    db.session.commit()
    return jsonify({'message': 'Course updated successfully'})


from datetime import date, time
@app.route('/create_exam', methods=['POST'])
def create_exam():
    data = request.json
    print(data)

    exam_name = data['exam_name'].strip()
    old_exam = Exam.query.filter(db.func.lower(Exam.exam_name) == exam_name.lower()).first()
    if old_exam:
        return jsonify({'message': 'Exam already exists'})

    new_exam = Exam(
        exam_name=exam_name,
        exam_description=data['exam_description'],
        examinor_slot_create_start_date=data['examinor_slot_create_start_date'],
        examinor_slot_create_end_date=data['examinor_slot_create_end_date'],
        booking_start_time=data['booking_start_time'],
        booking_end_time=data['booking_end_time'],
        exam_start_date=data['exam_start_date'],
        exam_end_date=data['exam_end_date'],
        course_id=data['course_id'],
        examinor_id=data['examinor_id']
    )

    db.session.add(new_exam)
    db.session.commit()

    return jsonify({'message': 'Exam created successfully'})



@app.route('/examinor_register',methods=['POST'])
def examinor_register():
    data = request.json
    print(data)
    new_examinor = User(name=data['username'], email=data['email'], password=data['password'], role='examinor')
    db.session.add(new_examinor)
    db.session.commit()
    return jsonify({'message': 'Examinor registered successfully'})

@app.route('/delete_course/<int:id>',methods=['POST'])
def delete_course(id):
    course = Course.query.filter_by(id=id).first()
    exams = Exam.query.filter_by(course_id=id).all()
    for exam in exams:
        Question.query.filter_by(exam_id=exam.id).delete()
        Rubric.query.filter_by(exam_id=exam.id).delete()
    Exam.query.filter_by(course_id=id).delete()
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'})

@app.route('/block_examinor/<int:id>',methods=['POST'])
def block_examinor(id):
    examinor = User.query.filter_by(id=id).first()
    examinor.is_blocked = True
    db.session.commit()
    return jsonify({'message': 'Examinor blocked successfully'})

@app.route('/unblock_examinor/<int:id>',methods=['POST'])
def unblock_examinor(id):
    examinor = User.query.filter_by(id=id).first()
    examinor.is_blocked = False
    db.session.commit()
    return jsonify({'message': 'Examinor unblocked successfully'})

@app.route('/provide_examination_details',methods=['POST','GET'])
def provide_examination_details():
    all_examinations_list = []
    all_examinations = Exam.query.all()
    for examination in all_examinations:
        all_examinations_list.append(
            {
                'id': examination.id,
                'name': examination.exam_name,
                'description': examination.exam_description,
                'examinor_slot_create_start_date': examination.examinor_slot_create_start_date,
                'examinor_slot_create_end_date': examination.examinor_slot_create_end_date,
                'booking_start_time': examination.booking_start_time,
                'booking_end_time': examination.booking_end_time,
                'exam_start_date': examination.exam_start_date,
                'exam_end_date': examination.exam_end_date,
                'course_id': examination.course_id,
                'examinor_id': examination.examinor_id
            }
        )
    return jsonify({'data': all_examinations_list})

@app.route('/create_questionbank/<int:exam_id>',methods=['POST'])
def create_questionbank(exam_id):
    data = request.json
    print(data)
    new_question = Question(question=data['question'], marks=data['marks'], exam_id=exam_id)
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'message': 'Question bank created successfully'})

@app.route('/provide_rubric_details/<int:exam_id>', methods=['GET', 'POST'])
def provide_rubric_details(exam_id):
    exam = Exam.query.filter_by(id=exam_id).first()
    rubrics = Rubric.query.filter_by(exam_id=exam_id).all()
    rubric_list = []
    for rubric in rubrics:
        rubric_list.append({
            'id': rubric.id,
            'criterion': rubric.criterion,
            'description': rubric.description,
            'marks': rubric.marks,
            'exam_id': rubric.exam_id
        })
    return jsonify({
        'data': rubric_list,
        'exam_name': exam.exam_name if exam else ''
    })

@app.route('/create_rubric/<int:exam_id>', methods=['POST'])
def create_rubric(exam_id):
    data = request.json
    new_rubric = Rubric(
        criterion=data['criterion'],
        description=data['description'],
        marks=data['marks'],
        exam_id=exam_id
    )
    db.session.add(new_rubric)
    db.session.commit()
    return jsonify({'message': 'Rubric created successfully'})

@app.route('/edit_rubric/<int:id>', methods=['POST'])
def edit_rubric(id):
    data = request.json
    rubric = Rubric.query.filter_by(id=id).first()
    rubric.criterion = data['criterion']
    rubric.description = data['description']
    rubric.marks = data['marks']
    db.session.commit()
    return jsonify({'message': 'Rubric updated successfully'})

@app.route('/delete_rubric/<int:id>', methods=['POST'])
def delete_rubric(id):
    rubric = Rubric.query.filter_by(id=id).first()
    db.session.delete(rubric)
    db.session.commit()
    return jsonify({'message': 'Rubric deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        old_user = User.query.filter_by(email='admin@example.com').first()
        if not old_user:
            user = User(name='admin', email='admin@example.com', password='admin', role='admin')
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)