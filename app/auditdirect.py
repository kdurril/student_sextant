#-*- coding: utf-8 -*-

#Create document with course requirement audit

#
from jinja2 import Template, Environment, PackageLoader, FileLoader
import sqlite3
import codecs
from datetime import date
from os import path, mkdir
import time

import audit_review_class as arc
import audit_dicts as ad
import audit_sql as asql


#env = Environment(loader=PackageLoader('yourapplication', 'templates'))


conn = sqlite3.connect('../evaluation/db/PUAFdb.db')
db = conn.cursor()


def create_path():
    '''create folder for new files'''
    #format today's date year month day
    today_folder = date.today()
    today_folder = today_folder.strftime("%Y_%m_%d")

    if not path.isdir(today_dir):
        mkdir(today_dir)

# Process to move data from app folder to local folder
# this could also be direct
# Create list of folders
# paths = os.findpath('U:\\2013_08\\Students')
# convert paths to a dictionary lookup table with uid key, path item
# seek the key, then move file to associated path
# paths_dict = {x[-9]: 'U:\\2013_08\\Students'+x for x in paths}
# Then find files in the app\students folder tagged with uid, move to path
#


# ids = db.execute("SELECT UID FROM students")
# ids.fetchall()
# ids = [x[0] for x in ids]

#with open('templates/auditdirect.html', 'r+') as direct:
#    directread = direct.read()
#initialize the template
#directread = Template(directread)
#send
#directread.render()



#From db, get all user ids

#From db, get all specialization ids



#Create a file name
#Create file with UTF-8 encoding
#Send file via email

#create file
#See MakeDirectories.py for basics

# cur = db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE program_code = "MAPO" order by Last_name;')
# directory_all = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]

# date_txt = date.today()
# date_txt = date_txt.strftime("%Y_%m_%d")

#dir_str = "{0}, {1} {2} {3}".format(directory_all['Last_name'], directory_all['first_name'], directory_all['UID'], date_txt)
# Marcy_Cara_999111222.html
#
#Encode as UTF-8
# with open('name.html', 'a+') as student_direct:
#    student_direct.write(directread.render())


def auditalt(user_id, specialization_id):
    "Alternative audits: review courses under another specializations rules"

    user_id_txt = user_id
    user_id = [user_id]
    #specialization_id = [specialization_id]
    uid_check = db.execute('''SELECT UID FROM directory WHERE program_code="MAPO";''')
    check = uid_check.fetchall()
    check = [x[0] for x in check] 
    
    specialization = db.execute('SELECT DISTINCT major FROM directory')
    specialization_list = [dict(specialization=row[0]) for row in specialization.fetchall()]

    cur = db.execute('SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE program_code = "MAPO" order by Last_name;')
    directory_all = [dict(UID=row[0], Last_name=row[1], first_name=row[2], email=row[3], major=row[4], program_code=row[5]) for row in cur.fetchall()]

    if specialization_id in ad.All_dict:
        cur = db.execute("SELECT UID, Last_name, first_name, email, major, program_code FROM directory WHERE UID=?", user_id)
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
        cur = db.execute(qry_cp_alt, user_id)
        #program_list = [dict(UID=row[0], Class=row[1], Credits=row[2], Grade=row[3]) for row in cur.fetchall()]
        current_program_list = [dict(UID=row[0], Class=row[1],\
        Credits=row[2], Grade=row[3], Sem=row[4]) for row in cur.fetchall()]
                
        #current semester courses
        qry_current_sem = '''SELECT p.UID, p.Class, p.Credits, p.Grade, p.Sem
                             FROM student AS p
                             WHERE Sem = "1308" AND Class != "" AND p.UID = ? '''
        cur = db.execute(qry_current_sem, user_id)
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
        cur = db.execute(nongrad_puafonly, user_id)
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

        cur = db.execute(qry_ass, user_id)
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

        return render_template('auditalt.html',\
            check = check,\
            user_id_txt=user_id_txt,\
            #alt_spec_uri=alt_spec_uri,\
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