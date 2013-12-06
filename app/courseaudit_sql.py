#!/usr/bin/env python
#-*- coding: utf-8 -*-

#These queries extract student audit information
#First restrict records to those from the current program
#Only the semesters that match the current program are returned

qry_current_program_sem = '''
SELECT 
		reg.UID, reg.SEM
FROM
		reg,
		(SELECT
			UID, Secondary 
		FROM reg 
		WHERE Sem = "1308"
		) as current_program 
WHERE 
		reg.UID = current_program.UID 
		AND 
		reg.Secondary = current_program.Secondary
		'''



qry_cp_course = '''
SELECT
                student.UID, student.Class, student.Credits, student.Grade 
FROM
                student, (''' + qry_current_program_sem + ''') as c_p_s 
WHERE
                student.UID = c_p_s.UID
                AND student.Sem = c_p_s.Sem
                '''

qry_current_credits = '''
SELECT
                student.UID, SUM(student.Credits) as SumofCredits 
FROM
                student, (''' + qry_current_program_sem + ''') as c_p_s 
WHERE
                student.UID string.
	
GROUP BY
                student.UID'''

qry_current_program_sem_in = '''
SELECT 
		prime.UID, prime.SEM 
FROM 
		reg prime INNER JOIN
		(SELECT 
                UID, Secondary 
		FROM reg 
		WHERE Sem = "1308") as current_program
		ON prime.UID = current_program.UID
'''

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
		reg,
		(SELECT
			UID, Secondary
		FROM reg
		WHERE Sem = "1208") as current_program
WHERE
		reg.UID = current_program.UID
		AND
		reg.Secondary != current_program.Secondary'''

qry_cp_course_out = '''
SELECT p.UID, p.Sem, p.Class, p.Credits, p.Grade 
FROM student p INNER JOIN (''' + qry_not_current_program_sem + ''') c_p_s 
ON p.UID = c_p_s.UID AND p.SEM = c_p_s.SEM
WHERE p.Class LIKE "%PUAF%"
'''

qry_cp_alt = '''
SELECT
                cp1.UID, cp1.Class, cp1.Credits, cp1.Grade
FROM
        (SELECT * from student
        WHERE student.Grade LIKE "A%" OR student.Grade LIKE "B%"
        OR student.Grade = "C" OR student.Grade = "C+" or student.Grade = "C-")
        AS cp1, (''' + qry_current_program_sem + ''') AS c_p_s
WHERE
      cp1.UID = c_p_s.UID
      AND cp1.Sem = c_p_s.Sem
       '''

qry_pregrad = '''
SELECT 
		reg.UID, reg.SEM 
FROM 
		reg, 
		(SELECT 
			UID, Sem, Secondary 
		FROM reg 
		WHERE secondary LIKE "2%"
		) as old_program 
WHERE 
		reg.UID = old_program.UID 
		AND 
		reg.Sem = old_program.Sem'''

qry_cp_pregrad = '''
SELECT
        cp1.UID, cp1.Class, cp1.Credits, cp1.Grade
FROM
        (SELECT * from student WHERE student.Grade LIKE "A%" OR student.Grade LIKE "B%"
        OR student.Grade = "C" OR student.Grade = "C+" or student.Grade = "C-") as cp1,
        (''' + qry_pregrad + ''') as c_p_s
WHERE
        cp1.UID = c_p_s.UID
        AND cp1.Sem = c_p_s.Sem
        AND cp1.Class LIKE "PUAF%"
        
       '''

qry_current_sem = '''
SELECT p.UID, p.Class, p.Credits, p.Grade, p.Sem from student p
WHERE Sem = "1301" AND Class != "" '''


str_bamppUID = "106453762 OR 110500100 OR 109903110 OR 101930305 OR 108875180\
OR 109513227 OR 108328204 OR 110000143 OR 109964944 OR 109411349 OR 110603481\
OR 108338074 OR 109389723 OR 110552222 OR 110116127 OR 108617506 OR 109902885\
OR 109422758 OR 109367783 OR 108867628 OR 109483186 OR 109029940 OR 108488373\
OR 103706038 OR 109988407 OR 109574457 OR 110097723 OR 108292925 OR 109930321\
OR 109968959 OR 110627777 OR 109471947 OR 110490180 OR 109396936 OR 109997386\
OR 109421515 OR 109926478 OR 109945295 OR 110132561 OR 110035794 OR 109939539\
OR 109902168 OR 110634713 OR 105988623 OR 109934688 OR 108442337 OR 104266449\
OR 108930667 OR 108834156 OR 110957805 OR 110177647 OR 108344945 OR 109371506\
OR 109598965 OR 109879927 OR 110024187 OR 110007036 OR 110065685"

allsem_puafonly = '''
SELECT
                directory.UID, directory.Last_name, directory.first_name,
                student.Class, student.Grade, student.Credits, reg.Degree,
                reg.Secondary
FROM
                directory INNER JOIN student
                ON directory.UID = student.UID INNER JOIN reg
                ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
'''


#this query returns the nongrad policy courses
nongrad_puafonly = '''
SELECT
        directory.UID, directory.Last_name, directory.first_name, student.Class,
        student.Grade, student.Credits, reg.Degree, reg.Secondary
FROM
        directory INNER JOIN student
        ON directory.UID = student.UID INNER JOIN reg
        ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
WHERE
        reg.Degree = ""
        AND student.Class like "PUAF%"
        AND substr(student.Class, 5, 1) >= "6"
        '''

#this query returns the advanced special student courses policy courses
qry_ass = '''
SELECT
        directory.UID, directory.Last_name, directory.first_name,
        student.Class, student.Grade, student.Credits, reg.Degree, reg.Secondary
FROM
        directory INNER JOIN student
        ON directory.UID = student.UID INNER JOIN reg
        ON (student.Sem = reg.Sem) AND (directory.UID = reg.UID)
WHERE
        reg.Degree = "A.S.S." '''


qry_directory ='''
SELECT
        UID, Last_name, first_name, major, degree_name
FROM
        directory
ORDER BY
        Last_name'''
