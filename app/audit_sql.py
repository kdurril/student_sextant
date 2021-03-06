#!/usr/bin/env python
#-*- coding: utf-8 -*-

#audit_sql.py
#This page contains the queries for the site
#Be careful of the ? that allow for secure queries
#


#main page navigation directory list
qry_directory_list = '''SELECT UID, Last_name, first_name, 
                                email, major, program_code 
                        FROM directory 
                        ORDER BY program_code, Last_name'''

#student directory info 
qry_directory_by_uid = '''SELECT UID, Last_name, first_name,
                               email, major, program_code
                          FROM directory 
                          WHERE UID=?'''

qry_directory_mapo = '''SELECT UID, Last_name, first_name, 
                        email, major, program_code 
                        FROM directory 
                        WHERE program_code = "MAPO" 
                        order by Last_name;'''

#
qry_specialization = '''SELECT DISTINCT major FROM directory'''

specializations = ["", "EDUC", "ENGY", "ENV", "FAM",
"HLTH", "IDEV", "ISEP", "LM", "LMPO", "MAPO", "MFL", "ML",
"NML", "OTH", "PSFM", "SOC"]

qry_program_start = '''SELECT UID, M_Start FROM start WHERE UID = ?'''


#get semesters of student's current program
#then use these semesters to get courses from current program
#many students have been in other programs,
#we only want courses that count toward current program
#however, bampp and advanced special students need previous program courses

current_semester = "1408"

qry_current_program_sem = '''SELECT reg.UID, reg.SEM 
FROM reg 
INNER JOIN (SELECT UID, Secondary FROM reg WHERE Sem = {current_sem}) 
AS current_program 
ON (reg.UID = current_program.UID)
AND (reg.Secondary = current_program.Secondary)
'''.format(current_sem=current_semester)

qry_cp_course = '''SELECT
                student.UID, student.Sem, student.Class, student.Credits, student.Grade
FROM
                student INNER JOIN (''' + qry_current_program_sem + ''') as c_p_s
                ON student.UID = c_p_s.UID
                AND student.Sem = c_p_s.Sem             
'''

qry_current_credits = '''SELECT
                student.UID, SUM(student.Credits) as SumofCredits 
FROM
                student INNER JOIN (''' + qry_current_program_sem + ''') as c_p_s
                ON student.UID = c_p_s.UID 
                AND student.Sem = c_p_s.Sem
                GROUP BY student.UID
'''

qry_current_credits = '''SELECT
                student.UID, SUM(student.Credits) as SumofCredits 
FROM
                student INNER JOIN (''' + qry_current_program_sem + ''') as c_p_s
                ON student.UID = c_p_s.UID 
                AND student.Sem = c_p_s.Sem
                GROUP BY student.UID
'''

qry_current_program_sem_in = '''
SELECT 
		prime.UID, prime.SEM 
FROM 
		reg prime INNER JOIN
		(SELECT 
			UID, Secondary 
		FROM reg 
		WHERE Sem = {current_sem}) as current_program
		ON prime.UID = current_program.UID
'''.format(current_sem=current_semester)

qry_cp_course_in = '''
SELECT
        p.UID, p.Class, p.Credits, p.Grade 
FROM
        student p INNER JOIN (''' + qry_current_program_sem_in + ''') c_p_s 
        ON p.UID = c_p_s.UID AND p.SEM = c_p_s.SEM
'''

qry_not_current_program_sem = '''
SELECT
		reg.UID, reg.SEM
FROM
		reg INNER JOIN
		(SELECT
			UID, Secondary
		FROM reg
		WHERE Sem = {current_sem}) as current_program
        ON reg.UID = current_program.UID
WHERE
		reg.Secondary != current_program.Secondary
'''.format(current_sem=current_semester)

qry_cp_course_out = '''
SELECT p.UID, p.Class, p.Credits, p.Grade 
FROM student p INNER JOIN (''' + qry_not_current_program_sem + ''') c_p_s 
ON p.UID = c_p_s.UID AND p.SEM = c_p_s.SEM
WHERE p.Class LIKE "%PUAF%"
'''

# consider combining these ie [A-C][+,-]
# convert to IN operator
# review values to leave out "CC"

qry_cp_alt = '''SELECT cp1.UID, cp1.Class, cp1.Credits, cp1.Grade, cp1.Sem
    FROM (SELECT * from student 
          WHERE student.GRADE 
          IN ("A", "A+", "A-", "B", "B+", "B-", "C", "C+", "C-")
          )
    AS cp1 INNER JOIN ({current_program_sem}) as c_p_s
    ON (cp1.UID = c_p_s.UID) AND (cp1.Sem = c_p_s.Sem)
    WHERE cp1.UID = ?
    ORDER BY cp1.Sem, cp1.Class'''.format(current_program_sem=qry_current_program_sem)

qry_cp_all_grades = '''SELECT cp1.UID, cp1.Class, cp1.Credits, cp1.Grade, cp1.Sem
    FROM (SELECT * from student)
    AS cp1 
    INNER JOIN (''' + qry_current_program_sem + ''') as c_p_s
    ON (cp1.UID = c_p_s.UID) AND (cp1.Sem = c_p_s.Sem)
    ORDER BY cp1.Class'''

qry_cp_all_grades_sum = '''SELECT cp1.UID, Sum(cp1.Credits) as SumofCredit
    FROM (SELECT * from student) AS cp1 
    INNER JOIN ({current_program_sem}) as c_p_s
    ON (cp1.UID = c_p_s.UID) AND (cp1.Sem = c_p_s.Sem)
    GROUP BY cp1.UID
    '''.format(current_program_sem=qry_current_program_sem)

qry_creditsum_directory = '''SELECT directory.Last_name, directory.first_name, 
    creditcount.UID, directory.program_code, creditcount.SumofCredit
    FROM ({0}) AS creditcount 
    INNER JOIN directory
    ON (creditcount.UID = directory.UID)
    GROUP BY directory.program_code, directory.Last_name
    '''.format(qry_cp_all_grades_sum)

qry_cp_alt_current = '''SELECT cp1.UID, cp1.Class, cp1.Credits, cp1.Grade, cp1.Sem
    FROM (SELECT * from student 
          WHERE student.GRADE 
          IN ("A", "A+", "A-", "B", "B+", "B-", "C", "C+", "C-", "")
          )
    AS cp1 INNER JOIN ({current_program_sem}) as c_p_s
    ON (cp1.UID = c_p_s.UID) AND (cp1.Sem = c_p_s.Sem)
    WHERE cp1.UID = ?
    ORDER BY cp1.Sem, cp1.Class'''.format(current_program_sem=qry_current_program_sem)

#Get sum of credits by semester
qry_cp_alt_subtotal = '''SELECT UID, Sem, Count(Sem) as CountSem, Sum(Credits) as SumCredits
FROM ({qry_cp_alt_current})
GROUP BY UID, Sem'''.format(qry_cp_alt_current=qry_cp_alt_current)

#Count of credits, count of semester
qry_cp_alt_final = '''SELECT UID, Count(CountSem) as TotalSem, 
Sum(SumCredits) as TotalCredit, (Sum(SumCredits)/Count(CountSem)) as AveSemCredit
FROM ({qry_cp_alt_subtotal})
GROUP BY UID'''.format(qry_cp_alt_subtotal=qry_cp_alt_subtotal)


qry_cp_alt_coursebysem = '''SELECT UID, Sem, Count(Class) as CountClass, Sum(Credits) as CreditTotal
FROM ({qry_cp_alt_current})
GROUP BY UID, Sem'''.format(qry_cp_alt_current=qry_cp_alt_current)



qry_pregrad = '''
SELECT 
		reg.UID, reg.SEM 
FROM 
		reg INNER JOIN 
		(SELECT 
			UID, Sem, Secondary 
		FROM reg 
		WHERE secondary LIKE "2%"
		) as old_program 
        ON reg.UID = old_program.UID 
        AND reg.Sem = old_program.Sem
'''

qry_cp_pregrad = '''
SELECT
        cp1.UID, cp1.Class, cp1.Credits, cp1.Grade
FROM
        (SELECT * from student WHERE student.Grade LIKE "A%" OR student.Grade LIKE "B%"
        OR student.Grade = "C" OR student.Grade = "C+" or student.Grade = "C-") as cp1
        INNER JOIN (''' + qry_pregrad + ''') as c_p_s
        ON (cp1.UID = c_p_s.UID)
        AND (cp1.Sem = c_p_s.Sem)
        
WHERE
        cp1.Class LIKE "PUAF%"
        
'''

qry_current_sem = '''SELECT p.UID, p.Class, p.Credits, p.Grade, p.Sem
                    FROM student AS p
                    WHERE Sem = "{current_sem}" AND Class != "" AND p.UID = ? 
                    '''.format(current_sem=current_semester)

allsem_puafonly = ''' SELECT directory.UID, directory.Last_name, 
directory.first_name, student.Class, student.Grade, student.Credits, 
reg.Degree, reg.Secondary
FROM directory INNER JOIN student
ON (directory.UID = student.UID) 
INNER JOIN reg
ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
'''

#this query returns the nongrad policy courses
nongrad_puafonly = '''SELECT student.UID,
    student.Class, student.Grade, student.Credits, 
    reg.Degree, reg.Secondary
    FROM directory INNER JOIN student
    ON directory.UID = student.UID INNER JOIN reg
    ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
    WHERE
    reg.Degree = ""
    AND student.Class like "PUAF%"
    AND substr(student.Class, 5, 1) >= "6"
    AND directory.UID = ?
    '''
#this query returns the advanced special student courses policy courses
qry_ass = '''SELECT
    student.UID, student.Class, student.Grade, 
    student.Credits, reg.Degree, reg.Secondary
    FROM
    directory INNER JOIN student
    ON directory.UID = student.UID INNER JOIN reg
    ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
    WHERE
    reg.Degree = "A.S.S."
    AND directory.UID = ? 
    '''

#Use this for course audit for current specialization
qry_requirment_base = '''SELECT DISTINCT a.UID, a.Last_name, a.first_name,
a.Class
FROM requirement INNER JOIN 
(directory INNER JOIN student ON directory.UID = student.UID) as a
ON requirement.Course_number = a.Class AND requirement.Specialization = a.major
WHERE requirement.req_type < 4
AND a.UID = ?
'''

#Use this for course audit for alternative specialization
qry_req_alt = '''SELECT DISTINCT a.UID, a.Last_name, a.first_name, a.Class
FROM requirement INNER JOIN 
(directory INNER JOIN student ON directory.UID = student.UID) as a
ON requirement.Course_number = a.Class
WHERE a.UID = ?
AND requirement.Specialization = ?
'''

#Advising Notes
qry_advisingnote = '''SELECT ID, UID, student_inquiry, response,
 next_action_student, next_action_adviser, date_stamp 
 FROM inquiry WHERE UID=?  order by date_stamp desc'''

qry_advisingnote_add = '''INSERT INTO inquiry 
 (UID, student_inquiry, response, next_action_student, next_action_adviser) 
 values (?, ?, ?, ?, ?)'''

qry_advisingnote_edit = '''SELECT ID, UID, student_inquiry, response, 
            next_action_student, next_action_adviser, date_stamp 
            FROM inquiry 
            WHERE ID =? 
            ORDER BY date_stamp desc;'''

qry_advisingnote_edit_update = '''UPDATE inquiry
        SET student_inquiry = ?,
        response = ?,
        next_action_student = ?,
        next_action_adviser = ?
        WHERE ID = ?;'''

qry_advisingnote_edit_delete = '''DELETE FROM inquiry WHERE ID = ?;'''

qry_request = '''SELECT UID, request_type, course_number, course_title, puaf_equivalent, evidence_type,
     decision, decision_reason, grantor FROM course_request WHERE UID=? order by date_stamp desc;'''

qry_request_add = '''INSERT INTO course_request (UID, request_type, 
        course_number, course_title, puaf_equivalent, evidence_type, decision, decision_reason, grantor)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?)'''