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
    slot_open = db.Column(db.Boolean, default=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False, default='')
    marks = db.Column(db.Integer, nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete='CASCADE'), nullable=False)


class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_date = db.Column(db.String(100), nullable=False)
    slot_time = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete='CASCADE'), nullable=False)
    examinor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    marks = db.Column(db.Integer, nullable=False)




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
        'name': user.name,
        'user_id': user.id
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



@app.route('/create_examinor_profile', methods=['POST'])
def create_examinor_profile():
    data = request.json
    old_profile = Staff_Profile.query.filter_by(user_id=data['user_id']).first()
    if old_profile:
        return jsonify({'message': 'Profile already exists'})
    new_profile = Staff_Profile(
        address=data['address'],
        phone=data['phone'],
        past_experience=data['past_experience'],
        user_id=data['user_id']
    )
    db.session.add(new_profile)
    db.session.commit()
    return jsonify({'message': 'Profile created successfully'})

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
        slots = Slot.query.filter_by(exam_id=exam.id).all()
        for slot in slots:
            bookings = Booking.query.filter_by(slot_id=slot.id).all()
            for booking in bookings:
                Mark.query.filter_by(booking_id=booking.id).delete()
            Booking.query.filter_by(slot_id=slot.id).delete()
        Slot.query.filter_by(exam_id=exam.id).delete()
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
                'examinor_id': examination.examinor_id,
                'slot_open': bool(examination.slot_open)
            }
        )
    return jsonify({'data': all_examinations_list})

@app.route('/admin_exam_detail/<int:exam_id>', methods=['GET', 'POST'])
def admin_exam_detail(exam_id):
    exam = Exam.query.filter_by(id=exam_id).first()
    course = Course.query.filter_by(id=exam.course_id).first()
    examinor = User.query.filter_by(id=exam.examinor_id).first()
    slots = []
    for slot in Slot.query.filter_by(exam_id=exam_id).all():
        booked_names = []
        for booking in Booking.query.filter_by(slot_id=slot.id).all():
            student = User.query.filter_by(id=booking.user_id).first()
            if student:
                booked_names.append(student.name)
        slots.append({
            'id': slot.id,
            'slot_date': slot.slot_date,
            'slot_time': slot.slot_time,
            'capacity': slot.capacity,
            'booked_by': ', '.join(booked_names)
        })
    return jsonify({'data': {
        'id': exam.id,
        'name': exam.exam_name,
        'description': exam.exam_description,
        'examinor_slot_create_start_date': exam.examinor_slot_create_start_date,
        'examinor_slot_create_end_date': exam.examinor_slot_create_end_date,
        'booking_start_time': exam.booking_start_time,
        'booking_end_time': exam.booking_end_time,
        'exam_start_date': exam.exam_start_date,
        'exam_end_date': exam.exam_end_date,
        'course_name': course.coures_name if course else '',
        'examinor_name': examinor.name if examinor else '',
        'slot_open': bool(exam.slot_open),
        'slots': slots
    }})

@app.route('/create_questionbank/<int:exam_id>',methods=['POST'])
def create_questionbank(exam_id):
    data = request.json
    print(data)
    new_question = Question(
        question=data['question'],
        description=data.get('description') or '',
        marks=data['marks'],
        exam_id=exam_id
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'message': 'Question bank created successfully'})

@app.route('/provide_rubric_details/<int:exam_id>', methods=['GET', 'POST'])
def provide_rubric_details(exam_id):
    exam = Exam.query.filter_by(id=exam_id).first()
    questions = Question.query.filter_by(exam_id=exam_id).all()
    rubric_list = []
    for question in questions:
        rubric_list.append({
            'id': question.id,
            'criterion': question.question,
            'description': question.description,
            'marks': question.marks,
            'exam_id': question.exam_id
        })
    return jsonify({
        'data': rubric_list,
        'exam_name': exam.exam_name if exam else ''
    })

@app.route('/create_rubric/<int:exam_id>', methods=['POST'])
def create_rubric(exam_id):
    data = request.json
    new_question = Question(
        question=data['criterion'],
        description=data['description'],
        marks=data['marks'],
        exam_id=exam_id
    )
    db.session.add(new_question)
    db.session.commit()
    return jsonify({'message': 'Rubric created successfully'})

@app.route('/edit_rubric/<int:id>', methods=['POST'])
def edit_rubric(id):
    data = request.json
    question = Question.query.filter_by(id=id).first()
    question.question = data['criterion']
    question.description = data['description']
    question.marks = data['marks']
    db.session.commit()
    return jsonify({'message': 'Rubric updated successfully'})

@app.route('/delete_rubric/<int:id>', methods=['POST'])
def delete_rubric(id):
    question = Question.query.filter_by(id=id).first()
    Mark.query.filter_by(question_id=id).delete()
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Rubric deleted successfully'})

@app.route('/create_slot/<int:exam_id>', methods=['POST'])
def create_slot(exam_id):
    data = request.json
    exam = Exam.query.filter_by(id=exam_id).first()
    if not exam:
        return jsonify({'message': 'Examination not found'})

    today = date.today()
    slot_start = date.fromisoformat(str(exam.examinor_slot_create_start_date)[:10])
    slot_end = date.fromisoformat(str(exam.examinor_slot_create_end_date)[:10])
    in_window = slot_start <= today <= slot_end
    if not in_window and not exam.slot_open:
        return jsonify({'message': 'You can only create a slot between the slot start date and the slot end date'})

    slot_date = date.fromisoformat(str(data['slot_date'])[:10])
    exam_start = date.fromisoformat(str(exam.exam_start_date)[:10])
    exam_end = date.fromisoformat(str(exam.exam_end_date)[:10])
    if slot_date < exam_start or slot_date > exam_end:
        return jsonify({'message': 'Slot date must be between the exam start date and the exam end date'})

    new_slot = Slot(
        slot_date=data['slot_date'],
        slot_time=data['slot_time'],
        capacity=data['capacity'],
        exam_id=exam_id,
        examinor_id=data['examinor_id']
    )
    db.session.add(new_slot)
    db.session.commit()
    return jsonify({'message': 'Slot created successfully'})

@app.route('/provide_slot_details/<int:exam_id>', methods=['GET', 'POST'])
def provide_slot_details(exam_id):
    exam = Exam.query.filter_by(id=exam_id).first()
    slots = Slot.query.filter_by(exam_id=exam_id).all()
    slot_list = []
    for slot in slots:
        examinor = User.query.filter_by(id=slot.examinor_id).first()
        slot_list.append({
            'id': slot.id,
            'slot_date': slot.slot_date,
            'slot_time': slot.slot_time,
            'capacity': slot.capacity,
            'examinor_name': examinor.name if examinor else ''
        })
    return jsonify({
        'data': slot_list,
        'exam_name': exam.exam_name if exam else ''
    })

@app.route('/assigned_examination', methods=['POST'])
def assigned_examination():
    data = request.json
    examinor_id = data['examinor_id']

    exams = Exam.query.filter_by(examinor_id=examinor_id).all()
    assigned = []
    for examination in exams:
        course = Course.query.filter_by(id=examination.course_id).first()
        assigned.append({
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
            'course_name': course.coures_name if course else '',
            'examinor_id': examination.examinor_id,
            'slot_open': bool(examination.slot_open)
        })
    return jsonify({'data': assigned, 'message': 'Assigned examinations'})

@app.route('/open_slot/<int:exam_id>', methods=['POST'])
def open_slot(exam_id):
    exam = Exam.query.filter_by(id=exam_id).first()
    if not exam:
        return jsonify({'message': 'Examination not found'})
    exam.slot_open = True
    db.session.commit()
    return jsonify({'message': 'Slot creation opened'})

@app.route('/close_slot/<int:exam_id>', methods=['POST'])
def close_slot(exam_id):
    exam = Exam.query.filter_by(id=exam_id).first()
    if not exam:
        return jsonify({'message': 'Examination not found'})
    exam.slot_open = False
    db.session.commit()
    return jsonify({'message': 'Slot creation closed'})


@app.route('/user/submitForm', methods=['POST'])
def submitForm():
    data = request.json
    old_profile = User_profile.query.filter_by(user_id=data['user_id']).first()
    if old_profile:
        return jsonify({'message': 'Profile already exists'})
    new_user_profile = User_profile(
        address=data['address'],
        phone=data['phone'],
        past_experience=data['past_experience'],
        user_id=data['user_id']
    )
    db.session.add(new_user_profile)
    db.session.commit()
    return jsonify({'message': 'User profile created successfully'})

@app.route('/get_user_profile', methods=['POST'])
def get_user_profile():
    data = request.json
    profile = User_profile.query.filter_by(user_id=data['user_id']).first()
    if not profile:
        return jsonify({'data': None})
    return jsonify({'data': {
        'id': profile.id,
        'address': profile.address,
        'phone': profile.phone,
        'past_experience': profile.past_experience,
        'user_id': profile.user_id
    }})

@app.route('/edit_user_profile', methods=['POST'])
def edit_user_profile():
    data = request.json
    profile = User_profile.query.filter_by(user_id=data['user_id']).first()
    profile.address = data['address']
    profile.phone = data['phone']
    profile.past_experience = data['past_experience']
    db.session.commit()
    return jsonify({'message': 'User profile updated successfully'})

@app.route('/user/getExaminations', methods=['POST','GET'])
def getExaminations():
    all_examinations_list = []
    slots = Slot.query.all()
    for slot in slots:
        examination = Exam.query.filter_by(id=slot.exam_id).first()
        all_examinations_list.append({
            'id': slot.id,
            'exam_id': slot.exam_id,
            'name': examination.exam_name if examination else '',
            'slot_date': slot.slot_date,
            'slot_time': slot.slot_time
        })
    return jsonify({'data1': all_examinations_list})

@app.route('/book_slot/<int:slot_id>', methods=['POST'])
def book_slot(slot_id):
    data = request.json
    old_booking = Booking.query.filter_by(slot_id=slot_id, user_id=data['user_id']).first()
    if old_booking:
        return jsonify({'message': 'Slot already booked'})
    slot = Slot.query.filter_by(id=slot_id).first()
    booked_count = Booking.query.filter_by(slot_id=slot_id).count()
    if booked_count >= slot.capacity:
        return jsonify({'message': 'Slot is full'})
    new_booking = Booking(slot_id=slot_id, user_id=data['user_id'])
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Slot booked successfully'})

@app.route('/exam_detail/<int:exam_id>', methods=['POST'])
def exam_detail(exam_id):
    data = request.json
    exam = Exam.query.filter_by(id=exam_id).first()
    course = Course.query.filter_by(id=exam.course_id).first()
    examinor = User.query.filter_by(id=exam.examinor_id).first()
    today = date.today().isoformat()
    booking_open = today <= exam.booking_end_time
    slots = []
    for slot in Slot.query.filter_by(exam_id=exam_id).all():
        booking = Booking.query.filter_by(slot_id=slot.id, user_id=data['user_id']).first()
        slots.append({
            'id': slot.id,
            'slot_date': slot.slot_date,
            'slot_time': slot.slot_time,
            'capacity': slot.capacity,
            'booked': booking is not None
        })
    return jsonify({'data': {
        'id': exam.id,
        'name': exam.exam_name,
        'description': exam.exam_description,
        'examinor_slot_create_start_date': exam.examinor_slot_create_start_date,
        'examinor_slot_create_end_date': exam.examinor_slot_create_end_date,
        'booking_start_time': exam.booking_start_time,
        'booking_end_time': exam.booking_end_time,
        'exam_start_date': exam.exam_start_date,
        'exam_end_date': exam.exam_end_date,
        'course_name': course.coures_name if course else '',
        'examinor_name': examinor.name if examinor else '',
        'booking_open': booking_open,
        'slots': slots
    }})

@app.route('/cancel_slot/<int:slot_id>', methods=['POST'])
def cancel_slot(slot_id):
    data = request.json
    slot = Slot.query.filter_by(id=slot_id).first()
    exam = Exam.query.filter_by(id=slot.exam_id).first()
    today = date.today().isoformat()
    if today > exam.booking_end_time:
        return jsonify({'message': 'Booking period is closed'})
    booking = Booking.query.filter_by(slot_id=slot_id, user_id=data['user_id']).first()
    if not booking:
        return jsonify({'message': 'Slot is not booked'})
    Mark.query.filter_by(booking_id=booking.id).delete()
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Slot cancelled successfully'})

@app.route('/my_booking', methods=['POST'])
def my_booking():
    data = request.json
    today = date.today().isoformat()
    bookings = Booking.query.filter_by(user_id=data['user_id']).all()
    booking_list = []
    for booking in bookings:
        slot = Slot.query.filter_by(id=booking.slot_id).first()
        exam = Exam.query.filter_by(id=slot.exam_id).first()
        booking_list.append({
            'id': booking.id,
            'slot_id': slot.id,
            'exam_id': exam.id if exam else '',
            'name': exam.exam_name if exam else '',
            'slot_date': slot.slot_date,
            'slot_time': slot.slot_time,
            'booking_open': today <= exam.booking_end_time if exam else False
        })
    return jsonify({'data': booking_list})

@app.route('/examinor_bookings', methods=['POST'])
def examinor_bookings():
    data = request.json
    examinor_id = str(data['examinor_id'])
    booking_list = []
    bookings = Booking.query.all()
    for booking in bookings:
        slot = Slot.query.filter_by(id=booking.slot_id).first()
        if not slot:
            continue
        exam = Exam.query.filter_by(id=slot.exam_id).first()
        if not exam:
            continue
        if str(slot.examinor_id) != examinor_id and str(exam.examinor_id) != examinor_id:
            continue
        student = User.query.filter_by(id=booking.user_id).first()
        given_marks = Mark.query.filter_by(booking_id=booking.id).all()
        total_marks = sum(mark.marks for mark in given_marks)
        booking_list.append({
            'id': booking.id,
            'name': exam.exam_name,
            'student_name': student.name if student else '',
            'slot_date': slot.slot_date,
            'slot_time': slot.slot_time,
            'marks': total_marks if given_marks else ''
        })
    return jsonify({'data': booking_list})

@app.route('/give_marks/<int:booking_id>', methods=['GET', 'POST'])
def give_marks(booking_id):
    booking = Booking.query.filter_by(id=booking_id).first()
    slot = Slot.query.filter_by(id=booking.slot_id).first()
    exam = Exam.query.filter_by(id=slot.exam_id).first()
    student = User.query.filter_by(id=booking.user_id).first()
    if request.method == 'GET':
        questions = []
        for question in Question.query.filter_by(exam_id=exam.id).all():
            given = Mark.query.filter_by(booking_id=booking_id, question_id=question.id).first()
            questions.append({
                'id': question.id,
                'criterion': question.question,
                'description': question.description,
                'max_marks': question.marks,
                'marks': given.marks if given else ''
            })
        return jsonify({'data': {
            'booking_id': booking.id,
            'exam_name': exam.exam_name if exam else '',
            'student_name': student.name if student else '',
            'rubrics': questions
        }})
    data = request.json
    for item in data['rubrics']:
        question = Question.query.filter_by(id=item['question_id']).first()
        if int(item['marks']) > question.marks:
            return jsonify({'message': 'Marks cannot be more than rubric marks'})
        given = Mark.query.filter_by(booking_id=booking_id, question_id=item['question_id']).first()
        if given:
            given.marks = item['marks']
        else:
            db.session.add(Mark(booking_id=booking_id, question_id=item['question_id'], marks=item['marks']))
    db.session.commit()
    return jsonify({'message': 'Marks saved successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        question_columns = [row[1] for row in db.session.execute(db.text('PRAGMA table_info(question)')).fetchall()]
        if question_columns and 'description' not in question_columns:
            db.session.execute(db.text("ALTER TABLE question ADD COLUMN description VARCHAR(200) DEFAULT ''"))
            db.session.commit()
        rubric_table = db.session.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='rubric'")).fetchone()
        if rubric_table:
            rubric_rows = db.session.execute(db.text('SELECT criterion, description, marks, exam_id FROM rubric')).fetchall()
            for criterion, description, marks, exam_id in rubric_rows:
                exists = Question.query.filter_by(exam_id=exam_id, question=criterion, description=description, marks=marks).first()
                if not exists:
                    db.session.add(Question(question=criterion, description=description, marks=marks, exam_id=exam_id))
            db.session.commit()
        mark_columns = [row[1] for row in db.session.execute(db.text('PRAGMA table_info(mark)')).fetchall()]
        if mark_columns and 'question_id' not in mark_columns:
            db.session.execute(db.text('DROP TABLE mark'))
            db.session.commit()
            db.create_all()
        exam_columns = [row[1] for row in db.session.execute(db.text('PRAGMA table_info(exam)')).fetchall()]
        if 'slot_open' not in exam_columns:
            db.session.execute(db.text('ALTER TABLE exam ADD COLUMN slot_open BOOLEAN DEFAULT 0'))
            db.session.commit()
        old_user = User.query.filter_by(email='admin@example.com').first()
        if not old_user:
            user = User(name='admin', email='admin@example.com', password='admin', role='admin')
            db.session.add(user)
            db.session.commit()
    app.run(debug=True)