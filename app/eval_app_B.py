# all the imports
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
ALLOWED_EXTENSIONS = set(['.docx', '.doc', 'txt', 'pdf', '.xlsx', '.xls'])



# create our little application :)
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


#inquiry display
@app.route('/inquiry')
def show_entries():

    cur = g.db.execute('SELECT UID, student_inquiry, response, next_action_student, next_action_adviser FROM inquiry order by UID desc;')
    inquiry_list = [dict(UID=row[0], student_inquiry=row[1], response=row[2], next_action_student=row[3], next_action_adviser=row[4]) for row in cur.fetchall()]
    return render_template('student_notes.html', inquiry_list=inquiry_list)

#inquiry form
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into inquiry (UID, student_inquiry, response, next_action_student, next_action_adviser) values (?, ?, ?, ?, ?)',
                 [request.form['UID'], request.form['student_inquiry'], request.form['response'], request.form['next_action_student'], request.form['next_action_adviser']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/', methods=['GET'])
def directory_entries():
    uid_check = g.db.execute('SELECT UID FROM directory')
    check = uid_check.fetchall()
    check = [x[0] for x in check] 
    
    cur = g.db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory order by Last_name;')
    directory_list = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]
    return render_template('show_directory.html', directory_list=directory_list)

@app.route('/<int:uid>', methods=['GET'])
def auditbyid(uid):
    uid_check = g.db.execute('''SELECT UID FROM directory WHERE program_code="MAPO";''')
    check = uid_check.fetchall()
    check = [x[0] for x in check] 
    
    specialization = g.db.execute('SELECT DISTINCT major FROM directory')
    specialization_list = [dict(specialization=row[0]) for row in specialization.fetchall()]

    cur = g.db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE program_code = "MAPO" order by Last_name;')
    directory_all = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]

    
    cur = g.db.execute("SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE UID=?", [uid])
    directory_list = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]
    
    major = directory_list[0]['major']
    
    #Make list of links to alternative specializations
    alt_spec_uri = [dict(uri="/{0}/auditalt/{1}".format(uid, x['specialization']), specialization=x['specialization']) for x in specialization_list]

    #find courses that are in from the current program        
    qry_current_program_sem = '''SELECT reg.UID, reg.SEM FROM reg, (SELECT UID, Secondary FROM reg WHERE Sem = "1308"
    ) as current_program WHERE reg.UID = current_program.UID AND reg.Secondary = current_program.Secondary
    '''
    qry_cp_alt = '''SELECT cp1.UID, cp1.Class, cp1.Credits, cp1.Grade, cp1.Sem 
    FROM (SELECT * from student 
          WHERE student.Grade = "A" OR student.Grade = "A+" OR student.Grade = "A-" OR student.Grade LIKE "B%"
          OR student.Grade = "C" OR student.Grade = "C+" or student.Grade = "C-")
    AS cp1, (''' + qry_current_program_sem + ''') as c_p_s 
    WHERE cp1.UID = c_p_s.UID AND cp1.UID = ?
    AND cp1.Sem = c_p_s.Sem
    ORDER BY cp1.Class'''
    cur = g.db.execute(qry_cp_alt, [uid])
    #program_list = [dict(UID=row[0], Class=row[1], Credits=row[2], Grade=row[3]) for row in cur.fetchall()]
    current_program_list = [dict(UID=row[0], Class=row[1],\
    Credits=row[2], Grade=row[3], Sem=row[4]) for row in cur.fetchall()]
            
    #current semester courses
    qry_current_sem = '''SELECT p.UID, p.Class, p.Credits, p.Grade, p.Sem
                         FROM student AS p
                         WHERE Sem = "1308" AND Class != "" AND p.UID = ? '''
    cur = g.db.execute(qry_current_sem, [uid])
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
    cur = g.db.execute(nongrad_puafonly, [uid])
    nongrad_list = [dict(UID=row[0], Class=row[1], Grade=row[2],\
    Credits=row[3], Degree=row[4], Secondary=row[5])\
    for row in cur.fetchall()]

    current_program_list.extend(nongrad_list)

    qry_ass = '''SELECT
    student.UID, student.Class, student.Grade, student.Credits,
    reg.Degree, reg.Secondary
    FROM
    directory INNER JOIN student
    ON directory.UID = student.UID INNER JOIN reg
    ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
    WHERE
    reg.Degree = "A.S.S."
    AND directory.UID = ? '''

    cur = g.db.execute(qry_ass, [uid])
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


@app.route('/auditmpp', methods=['GET', 'POST'])
def auditmpp():
    uid_check = g.db.execute('''SELECT UID FROM directory WHERE program_code="MAPO";''')
    check = uid_check.fetchall()
    check = [x[0] for x in check] 
    
    specialization = g.db.execute('SELECT DISTINCT major FROM directory')
    specialization_list = [dict(specialization=row[0]) for row in specialization.fetchall()]

    cur = g.db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE program_code = "MAPO" order by Last_name;')
    directory_all = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]

    if request.method == 'POST':
        cur = g.db.execute("SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE UID=?", [request.form['UID']])
        directory_list = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]
        
        major = directory_list[0]['major']
        
        #Make list of links to alternative specializations
        alt_spec_uri = [dict(uri="/auditalt/{0}/{1}".format(request.form['UID'], x['specialization']), specialization=x['specialization']) for x in specialization_list]

        #find courses that are in from the current program        
        qry_current_program_sem = '''SELECT reg.UID, reg.SEM FROM reg, (SELECT UID, Secondary FROM reg WHERE Sem = "1308"
        ) as current_program WHERE reg.UID = current_program.UID AND reg.Secondary = current_program.Secondary
        '''
        qry_cp_alt = '''SELECT cp1.UID, cp1.Class, cp1.Credits, cp1.Grade 
        FROM (SELECT * from student 
              WHERE student.Grade = "A" OR student.Grade = "A+" OR student.Grade = "A-" OR student.Grade LIKE "B%"
              OR student.Grade = "C" OR student.Grade = "C+" or student.Grade = "C-")
        AS cp1, (''' + qry_current_program_sem + ''') as c_p_s 
        WHERE cp1.UID = c_p_s.UID AND cp1.UID = ?
        AND cp1.Sem = c_p_s.Sem
        ORDER BY cp1.Class'''
        cur = g.db.execute(qry_cp_alt, [request.form['UID']])
        #program_list = [dict(UID=row[0], Class=row[1], Credits=row[2], Grade=row[3]) for row in cur.fetchall()]
        current_program_list = [dict(UID=row[0], Class=row[1],\
        Credits=row[2], Grade=row[3]) for row in cur.fetchall()]
                
        #current semester courses
        qry_current_sem = '''SELECT p.UID, p.Class, p.Credits, p.Grade, p.Sem
                             FROM student AS p
                             WHERE Sem = "1308" AND Class != "" AND p.UID = ? '''
        cur = g.db.execute(qry_current_sem, [request.form['UID']])
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
        cur = g.db.execute(nongrad_puafonly, [request.form['UID']])
        nongrad_list = [dict(UID=row[0], Class=row[1], Grade=row[2],\
        Credits=row[3], Degree=row[4], Secondary=row[5])\
        for row in cur.fetchall()]

        current_program_list.extend(nongrad_list)

        qry_ass = '''SELECT
        student.UID, student.Class, student.Grade, student.Credits,
        reg.Degree, reg.Secondary
        FROM
        directory INNER JOIN student
        ON directory.UID = student.UID INNER JOIN reg
        ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
        WHERE
        reg.Degree = "A.S.S."
        AND directory.UID = ? '''

        cur = g.db.execute(qry_ass, [request.form['UID']])
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

        #use audit_dicts All_dict as a lookup from the major
        completedALT = review.specialization_complete(ad.All_dict[request.form['specialization']])
        completed = [list(x) for x in completed]
        complete_courseALT = [dict(Complete=list(row)) for row in completedALT if row != []]

        #program credit
        program_credit = str(sum(int(item['Credits']) for item in current_program_list))
        current_program_credit = [dict(total=program_credit)]

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
            complete_course=complete_course,\
            complete_courseALT=complete_courseALT)
    else:
        return render_template('auditmpp.html',\
         directory_all=directory_all,\
         specialization_list=specialization_list)


@app.route('/<user_id>/auditalt/<specialization_id>', methods=['GET'])
def auditalt(user_id, specialization_id):
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
    cur = g.db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE program_code = "MAPO" AND UID=?;', [uid])
    directory_list = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]

    cur = g.db.execute('SELECT UID, student_inquiry, response, next_action_student, next_action_adviser FROM inquiry WHERE UID=? order by date_stamp desc;', [uid])
    inquiry_list = [dict(UID=row[0], student_inquiry=row[1], response=row[2], next_action_student=row[3], next_action_adviser=row[4]) for row in cur.fetchall()]
    return render_template('student_notes.html', directory_list=directory_list, uid=uid, inquiry_list=inquiry_list)

#advising note form
@app.route('/advisingnote/add', methods=['POST'])
def advisingnote_add():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into inquiry (UID, student_inquiry, response, next_action_student, next_action_adviser) values (?, ?, ?, ?, ?)',
                 [request.form['UID'], request.form['student_inquiry'], request.form['response'], request.form['next_action_student'], request.form['next_action_adviser']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('directory_entries'))

#inquiry form
@app.route('/student/<int:uid>/courserequest')
def view_course_request(uid):

    return render_template('courserequest.html', uid=uid)

@app.route('/student/courserequest/add', methods=['POST'])
def add_course_request():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('''INSERT INTO course_request (UID, request_type, 
        course_number, course_title, puaf_equivalent, evidence_type,
        evidence_doc, decision, decision_reason, grantor)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',\
        [request.form['UID'],\
        request.form['request_type'], request.form['course_number'],\
        request.form['course_title'], request.form['puaf_equivalent'],\
        request.form['evidence_type'], request.form['evidence_doc'],\
        request.form['decision'], request.form['decision_reason'],\
        request.form['grantor']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('directory_entries'))

#file upload
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#Enhance the upload to append the UID to a file
@app.route('/<int:uid>/supportdocs', methods=['GET', 'POST'])
def upload_file_view(uid):
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