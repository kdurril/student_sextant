#Student Evaluation Application
# all the imports
#-*- coding: utf-8 -*-

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from werkzeug import secure_filename
import os

from contextlib import closing
import audit_review_class as arc
import audit_dicts as ad
import audit_sql as asql

#import courseaudit_sql
#import audit_dict_v1_3 as sp_audit

DATABASE = '../evaluation/db/PUAFdb.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
UPLOAD_FOLDER = '../student'
ALLOWED_EXTENSIONS = set(['.docx', '.doc', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', '.xlsx', '.xls'])



# create the application
app = Flask(__name__)
app.config.from_object(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#app.session_interface = ItsdangerousSessionInterface()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, '../evaluation/db/PUAFdb.db', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

#def init_db():
#    with closing(connect_db()) as db:
#    	with app.open_resource('schema.sql', mode='r') as f:
#    		db.cursor().executescript(f.read())
#    	db.commit()

#Entry for student_notes
#Display student_notes by student
#Need search function for UID or Student Name

#Entry for waiver and make subunit of student_notes
#Display waiver by student



@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/', methods=['GET'])
def directory_entries():
    '''Landing page, navigate to specific student from here'''
    '''List for each specialization to identify students by program'''
    uid_check = g.db.execute('SELECT UID FROM directory')
    check = uid_check.fetchall()
    check = [x[0] for x in check] 
    
    cur = g.db.execute('''SELECT UID, Last_name, first_name, 
        email, major, program_code FROM directory order by Last_name;''')

    directory_list = [dict(UID=row[0], Last_name=row[1], first_name=row[2],
                      email=row[3], major=row[4], program_code=row[5]
                      ) for row in cur.fetchall()]

    mapo_list = [x for x in directory_list if x['program_code'] == "MAPO"]
    mamg_list = [x for x in directory_list if x['program_code'] == "MAMG"]
    bmpo_list = [x for x in directory_list if x['program_code'] == "BMPO"]
    lmpo_list = [x for x in directory_list if x['program_code'] == "LMPO"]
    posi_list = [x for x in directory_list if x['program_code'] == "POSI"]
    ppcn_list = [x for x in directory_list if x['program_code'] == "PPCN"]
    mepp_list = [x for x in directory_list if x['program_code'] == "MEPP"]

    program_code_list = ["BMPO","LMPO","MAMG","MAPO","MEPP", "POSI", "PPCN"]


    return render_template('show_directory.html',
                        directory_list=directory_list,
                        mapo_list=mapo_list, 
                        mamg_list=mamg_list, 
                        bmpo_list=bmpo_list,
                        lmpo_list=lmpo_list,
                        posi_list=posi_list,
                        ppcn_list=ppcn_list,
                        mepp_list=mepp_list)

@app.route('/<int:uid>', methods=['GET'])
def auditbyid(uid):
    '''Program and course info for student page'''
    '''Used to provide the audit and course review'''

    uid_check = g.db.execute('''SELECT UID FROM directory WHERE program_code="MAPO";''')
    check = uid_check.fetchall()
    check = [x[0] for x in check] 
    
    specialization = g.db.execute('SELECT DISTINCT major FROM directory')
    specialization_list = [dict(specialization=row[0]) for row in specialization.fetchall()]

    cur = g.db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE program_code = "MAPO" order by Last_name;')
    directory_all = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]

    
    cur = g.db.execute("SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE UID=?", [uid])
    directory_list = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]
    
    cur = g.db.execute("SELECT UID, M_Start FROM start WHERE UID = ?", [uid])
    program_start = [dict(UID=row[0], m_start=row[1]) for row in cur.fetchall()]
    
    directory_list[0]['m_start'] = program_start[0]['m_start']
    directory_list[0]['m_finish'] = [i for i in arc.semrev(directory_list[0]['m_start'], 0, 12, 48)][-1]
    major = directory_list[0]['major']
    
    #Make list of links to alternative specializations
    alt_spec_uri = [dict(uri="/{0}/auditalt/{1}".format(uid, x['specialization']), specialization=x['specialization']) for x in specialization_list]

    #find courses that are from the current program
    #see audit_sql.py for full query       

    cur = g.db.execute(asql.qry_cp_alt, [uid])
    
    current_program_list = [dict(UID=row[0], Class=row[1],\
    Credits=row[2], Grade=row[3], Sem=row[4]) for row in cur.fetchall()]
            
    #current semester courses
    #see audit_sql.py for full query
    
    cur = g.db.execute(asql.qry_current_sem, [uid])
    current_semester_list = [dict(UID=row[0], Class=row[1],\
     Credits=row[2], Grade=row[3], Sem=row[4]) for row in cur.fetchall()]

    current_program_list.extend(current_semester_list)

    #query for 600 level and above PUAF courses
    #see audit_sql.py for full query
    cur = g.db.execute(asql.nongrad_puafonly, [uid])
    nongrad_list = [dict(UID=row[0], Class=row[1], Grade=row[2],\
    Credits=row[3], Degree=row[4], Secondary=row[5])\
    for row in cur.fetchall()]

    current_program_list.extend(nongrad_list)

    #query for Advanced Special Student courses

    cur = g.db.execute(asql.qry_ass, [uid])
    ass_list = [dict(UID=row[0], Class=row[1], Grade=row[2],\
    Credits=row[3], Degree=row[4], Secondary=row[5])\
    for row in cur.fetchall()]

    current_program_list.extend(ass_list)

    #Completed and Remaining courses
    all_course = [x['Class'] for x in current_program_list]
    review = arc.CourseReview(all_course)

    #use audit_dicts All_dict as a lookup from the major
    completed = review.specialization_complete(ad.All_dict[directory_list[0]['major']])
    #completed = [list(x) for x in completed]
    complete_course = [dict(Complete=list(row)) for row in completed if row != []]

    #program credit
    program_credit = str(sum(int(item['Credits']) for item in current_program_list))
    current_program_credit = [dict(total=program_credit)]

    #original return page is auditmpp.html

    return render_template('auditmpp.html',\
        check = check,\
        specialization_list=specialization_list,\
        alt_spec_uri=alt_spec_uri,\
        directory_all=directory_all,\
        directory_list=directory_list,\
        current_program_list=current_program_list,\
        current_program_credit=current_program_credit,\
        current_semester_list=current_semester_list,\
        nongrad_list=nongrad_list,\
        ass_list=ass_list,\
        complete_course=complete_course)

@app.route('/<user_id>/auditalt/<specialization_id>', methods=['GET'])
def auditalt(user_id, specialization_id):
    "Alternative audits: review courses under another specializations rules"

    user_id_txt = user_id
    user_id = [user_id]
    #specialization_id = [specialization_id]
    uid_check = g.db.execute('''SELECT UID FROM directory WHERE program_code="MAPO";''')
    check = uid_check.fetchall()
    check = [x[0] for x in check] 
    
    specialization = g.db.execute('SELECT DISTINCT major FROM directory')
    specialization_list = [dict(specialization=row[0]) for row in specialization.fetchall()]

    cur = g.db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE program_code = "MAPO" order by Last_name;')
    directory_all = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]

    if request.method == 'GET' and specialization_id in ad.All_dict:
        cur = g.db.execute("SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE UID=?", user_id)
        directory_list = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]
        
        major = directory_list[0]['major']
        
        #Make list of links to alternative specializations
        alt_spec_uri = [dict(uri="/{0}/auditalt/{1}".format(user_id_txt, x['specialization']), specialization=x['specialization']) for x in specialization_list]


        qry_current_program_sem = '''SELECT reg.UID, reg.SEM FROM reg, (SELECT UID, Secondary FROM reg WHERE Sem = "1308"
        ) as current_program WHERE reg.UID = current_program.UID AND reg.Secondary = current_program.Secondary
        '''
        qry_cp_alt = '''SELECT cp1.UID, cp1.Class, cp1.Credits, cp1.Grade, cp1.SEM 
        FROM (SELECT * from student 
              WHERE student.Grade = "A" OR student.Grade = "A+" OR student.Grade = "A-" OR student.Grade LIKE "B%"
              OR student.Grade = "C" OR student.Grade = "C+" or student.Grade = "C-")
        AS cp1, (''' + qry_current_program_sem + ''') AS c_p_s 
        WHERE cp1.UID = c_p_s.UID AND cp1.UID = ?
        AND cp1.Sem = c_p_s.Sem
        ORDER BY cp1.Class'''
        cur = g.db.execute(qry_cp_alt, user_id)
        #program_list = [dict(UID=row[0], Class=row[1], Credits=row[2], Grade=row[3]) for row in cur.fetchall()]
        current_program_list = [dict(UID=row[0], Class=row[1],\
        Credits=row[2], Grade=row[3], Sem=row[4]) for row in cur.fetchall()]
                
        #current semester courses
        qry_current_sem = '''SELECT p.UID, p.Class, p.Credits, p.Grade, p.Sem
                             FROM student AS p
                             WHERE Sem = "1308" AND Class != "" AND p.UID = ? '''
        cur = g.db.execute(qry_current_sem, user_id)
        current_semester_list = [dict(UID=row[0], Class=row[1],\
         Credits=row[2], Grade=row[3], Sem=row[4]) for row in cur.fetchall()]

        current_program_list.extend(current_semester_list)

        nongrad_puafonly = '''SELECT student.UID,
        student.Class, student.Grade, student.Credits, 
        reg.Degree, reg.Secondary
        FROM
        directory INNER JOIN student
        ON directory.UID = student.UID INNER JOIN reg
        ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
        WHERE
        directory.UID = ?
        AND reg.Degree = ""
        AND student.Class like "PUAF%"
        AND substr(student.Class, 5, 1) >= "6" '''
        cur = g.db.execute(nongrad_puafonly, user_id)
        nongrad_list = [dict(UID=row[0], Class=row[1], Grade=row[2],\
        Credits=row[3], Degree=row[4], Secondary=row[5])\
        for row in cur.fetchall()]

        current_program_list.extend(nongrad_list)

        qry_ass = '''SELECT
        student.UID, student.Class, student.Grade, student.Credits,\
        reg.Degree, reg.Secondary
        FROM
        directory INNER JOIN student
        ON directory.UID = student.UID INNER JOIN reg
        ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
        WHERE
        reg.Degree = "A.S.S."
        AND directory.UID = ? '''

        cur = g.db.execute(qry_ass, user_id)
        ass_list = [dict(UID=row[0], Class=row[1], Grade=row[2],\
        Credits=row[3], Degree=row[4], Secondary=row[5])\
        for row in cur.fetchall()]

        current_program_list.extend(ass_list)

        #Completed and Remaining courses
        all_course = [x['Class'] for x in current_program_list]
        review = arc.CourseReview(all_course)

        #use audit_dicts All_dict as a lookup from the major
        completedALT = review.specialization_complete(ad.All_dict[specialization_id])
        #completed = [list(x) for x in completedALT]
        complete_courseALT = [dict(Complete=list(row)) for row in completedALT if row != []]

        #program credit
        program_credit = str(sum(int(item['Credits']) for item in current_program_list))
        current_program_credit = [dict(total=program_credit)]

        #directory_list = [dict(UID=request.form['UID'])] 
        #UID=request.form['UID'])
        #and request.form['UID'] in check
        return render_template('auditalt.html',\
            check = check,\
            user_id_txt=user_id_txt,\
            alt_spec_uri=alt_spec_uri,\
            specialization_id=specialization_id,\
            specialization_list=specialization_list,\
            directory_all=directory_all,\
            directory_list=directory_list,\
            current_program_list=current_program_list,\
            current_program_credit=current_program_credit,\
            current_semester_list=current_semester_list,
            nongrad_list=nongrad_list,\
            ass_list=ass_list,\
            complete_courseALT=complete_courseALT)
    else:
        return render_template('auditalt.html',\
         directory_all=directory_all,\
         specialization_list=specialization_list)


#advising note display
@app.route('/<int:uid>/advisingnote')
def advisingnote(uid):
    '''Subform of auditbyid, each advising note gets UID as hidden field,
     foreign key'''
    '''Primary form for recording advising sessions'''

    cur = g.db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE program_code = "MAPO" AND UID=?;', [uid])
    directory_list = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]

    cur = g.db.execute('SELECT UID, student_inquiry, response, next_action_student, next_action_adviser FROM inquiry WHERE UID=? order by date_stamp desc;', [uid])
    inquiry_list = [dict(UID=row[0], student_inquiry=row[1], response=row[2], next_action_student=row[3], next_action_adviser=row[4]) for row in cur.fetchall()]
    return render_template('student_notes.html',\
        directory_list=directory_list,\
        uid=uid,\
        inquiry_list=inquiry_list)

#advising note form
@app.route('/advisingnote/add', methods=['POST'])
def advisingnote_add():
    '''Inserts the advisingnote into the database'''

    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into inquiry (UID, student_inquiry, response, next_action_student, next_action_adviser) values (?, ?, ?, ?, ?)',
                 [request.form['UID'], request.form['student_inquiry'], request.form['response'], request.form['next_action_student'], request.form['next_action_adviser']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('directory_entries'))

#inquiry form
@app.route('/<int:uid>/courserequest', methods=['GET', 'POST'])
def view_course_request(uid):
    "Subform of auditbyid, each request has UID as hidden field FK"
    "Secondary advising form"

    cur = g.db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE program_code = "MAPO" AND UID=?;', [uid])
    directory_list = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]

    cur = g.db.execute('''SELECT UID, request_type, course_number, course_title, puaf_equivalent, evidence_type,
     decision, decision_reason, grantor FROM course_request WHERE UID=? order by date_stamp desc;''', [uid])
    request_list = [dict(UID=row[0], request_type=row[1], course_number=row[2], course_title=row[3], puaf_equivalent=row[4],
        evidence_type=row[5], decision=row[6], decision_reason=row[7], grantor=row[8] ) for row in cur.fetchall()]

    return render_template('courserequest.html',
        directory_list=directory_list,
        request_list=request_list,
        uid=uid)

@app.route('/courserequest/add', methods=['POST'])
def add_course_request():
    '''Inserts the view_course_request into the database'''
    if not session.get('logged_in'):
        abort(401)

    g.db.execute('''INSERT INTO course_request (UID, request_type, 
        course_number, course_title, puaf_equivalent, evidence_type, decision, decision_reason, grantor)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?)''',\
        [request.form['UID'],\
        request.form['request_type'], request.form['course_number'],\
        request.form['course_title'], request.form['puaf_equivalent'],\
        request.form['evidence_type'], request.form['decision'], 
        request.form['decision_reason'], request.form['grantor']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('directory_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    "Login"
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('directory_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    "Logout"
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('directory_entries'))

#file upload
def allowed_file(filename):
    "qualifies files for upload"
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#Enhance the upload to append the UID to a file
@app.route('/<int:uid>/supportdocs', methods=['GET', 'POST'])
def upload_file_view(uid):
    "Form for uploading files"
    "This should be a subform of an advising note"
    
    return render_template('supportdocs.html', uid=uid)

@app.route('/supportdocs/add', methods=['POST'])
def upload_file_add():
    #ENACT Sessions
    #add the student's uid to the file name
    #then move the file to the student's folder
    uid = request.form['UID']
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], uid+"_"+filename))
        return redirect(url_for('directory_entries',
                                filename=filename))

if __name__ == '__main__':
    app.run()