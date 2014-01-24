#! /usr/bin/env python
#-*- coding: utf-8 -*-
import csv 
import sqlite3
import sys
import replaceheader as rh

rh.replaceheader()

#sqlite3 db from student records

conn = sqlite3.connect("../evaluation/db/PUAFdb.db")
curs = conn.cursor()

clear_table = ['DROP TABLE if exists directory;',\
'DROP TABLE if exists student;',\
'DROP TABLE if exists reg;',\
'DROP TABLE if exists start;']

for table in clear_table:
    curs.execute(table)
    conn.commit()

#Create inquiry table
qry_create_inquiry_table = '''CREATE TABLE IF NOT EXISTS inquiry 
            (ID integer PRIMARY KEY autoincrement, 
            date_stamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
            UID integer, student_inquiry text, response text, 
            next_action_student text, next_action_adviser text, 
            adviser_id integer);'''
curs.execute(qry_create_inquiry_table)
conn.commit()

#Create course_request table
qry_create_course_request = '''CREATE TABLE IF NOT EXISTS course_request 
(ID integer PRIMARY KEY autoincrement, 
      date_stamp DATETIME DEFAULT CURRENT_TIMESTAMP, UID integer, 
      request_type text, course_number text, course_title text, 
      puaf_equivalent text, evidence_type text, decision text, 
      decision_reason text, grantor text, adviser_id integer);'''
curs.execute(qry_create_course_request)
conn.commit()

#Create start table
qry_create_start = '''CREATE TABLE start (ID integer PRIMARY KEY autoincrement,
 UID Integer, M_Start text, M_Finish text, M_Graduate text, P_Start text,
 P_Finish text, P_Graduate text, C_Start text, C_Finish text);'''
curs.execute(qry_create_start)
with open("../evaluation/db/student_startdate_tab.csv", "r+") as infile:
      dr = csv.DictReader(infile, delimiter='\t')
      to_db = [(i['UID'], i['M_Start'], i['M_Finish'], i['M_Graduate'],\
      i['P_Start'], i['P_Finish'], i['P_Graduate'], i['C_Start'],\
      i['C_Finish']) for i in dr]
curs.executemany('''INSERT INTO start (UID, M_Start, M_Finish, M_Graduate, 
      P_Start, P_Finish, P_Graduate, C_Start, C_Finish) 
      VALUES (?,?,?,?,?,?,?,?,?);''', to_db)
conn.commit()

#Create the student table
qry_create_student = '''CREATE TABLE student (ID integer PRIMARY KEY autoincrement,
      UID integer, Sem integer, Class text, Core text, Section text,
      Description text, Transfer text, Spec_Att text, Credits text, Grade text, 
      Current text);''' 
curs.execute(qry_create_student)
with open("../evaluation/db/student_records_tab.csv", "r+") as infile:
	dr = csv.DictReader(infile, delimiter = '\t')
	to_db = [(i['UID'], i['Sem'], i['Class'], i['Core'], i['Section'], i['Description'],\
      i['Transfer'], i['Spec_Att'], i['Credits'], i['Grade'], i['Current']) for i in dr]

curs.executemany('''INSERT INTO student (UID, Sem, Class, Core, Section, 
      Description, Transfer, Spec_Att, Credits, Grade, Current) 
      VALUES (?,?,?,?,?,?,?,?,?,?,?);''', to_db)
conn.commit()

#Create reg table
qry_create_reg = '''CREATE TABLE reg (ID integer PRIMARY KEY autoincrement, 
      UID integer, Sem integer, Fulltime_sis text, Fulltime_our text, 
      Eligible text, Off_campus text, M text, P text, C text, Degree text, 
      Secondary text, Continue text);'''
curs.execute(qry_create_reg)
with open("../evaluation/db/student_reg_tab.csv", "r+") as infile:
	dr = csv.DictReader(infile, delimiter = '\t')
	to_db = [(i['UID'], i['Sem'], i['Fulltime_sis'], i['Fulltime_our'],\
      i['Eligible'], i['Off_campus'], i['M'], i['P'], i['C'], i['Degree'],\
      i['Secondary'], i['Continue']) for i in dr]

curs.executemany('''INSERT INTO reg (UID, Sem, Fulltime_sis, Fulltime_our,
    Eligible, Off_campus, M, P, C, Degree, Secondary, Continue) 
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?);''', to_db)
conn.commit()

#Create directory table
qry_create_directory = '''CREATE TABLE directory (Last_name text,   
first_name text,   middle_name text,
UID  integer INTEGER PRIMARY KEY ASC,   Applicants_only_sem text,
email text,   birthdate text,   major text,   program_code text,   
advisor text,   street1 text,   street2 text,   street3 text,   
city text,   state text,   zip text,   country text,   
degree_name text,   Applicants_only_GRE_v text,   
Applicants_only_GRE_a text,   Applicants_only_GRE_q text,   
Applicants_only_GRE_v_percentile text,   
Applicants_only_GRE_a_percentile text,   
Applicants_only_GRE_q_percentile text,  
Applicants_only_rating text, Applicants_only_TWE text,   
Applicants_only_TOEFL text, Applicants_only_GMAT text, 
Applicants_only_MAT_Miller text,
Applicants_only_MAT_New_Miller_New_Score_range text, 
Applicants_only_LSAT text,   
Certification_if_applicable text,   
Special_Program_if_applicable text,
Applicants_only_GRE_Subject_Score text,   
Applicants_only_GRE_Subject_Percentile text,   
Applicants_only_GRE_Subject_Name text,   
Applicants_only_Dept_Admission_Dec text,  
Applicants_only_GS_Admission_Dec text,   
Applicants_only_Dept_provision_codes text,   
Applicants_only_GS_provision_codes text,   
Applicants_only_GPA_Undergrad text,   
Home_Phone text,   Work_Phone text,   
Is_International text,   Applicants_only_ASF_Submit text,   
Applicants_only_Recommendation_1_Name text,   
Applicants_only_Recommendation_1_Received text,   
Applicants_only_Recommendation_2_Name text,   
Applicants_only_Recommendation_2_Received text,   
Applicants_only_Recommendation_3_Name text,   
Applicants_only_Recommendation_3_Received text,   
Local_address_street1 text,   Local_address_street2 text,   
Local_address_street3 text,   Local_address_city text,   
Local_address_state text,   Local_address_zip text,   
Local_address_country text,   Applicants_only_Num_Publications text,   
Last_Undergrad_Univ_code text, Applicants_only_Last_Undergrad_univs_Tier text,   
Last_Undergrad_univs_Long_Name text,   
Applicants_only_Last_Undergrad_univs_ASF_entered_GPA text,   
Applicants_only_Last_Undergrad_Univ_ASF_entered_Major_Department text,   
Applicants_only_Last_Undergrad_if_available_Transcript_Received text,   
Applicants_only_Last_Graduate_Univ_code text,   
Applicants_only_Last_Graduate_univs_Tier text,   
Applicants_only_Last_Graduate_univs_Long_Name text,   
Applicants_only_Last_Graduate_univs_ASF_entered_GPA text,   
Applicants_only_Last_Graduate_Univ_ASF_entered_Major_Department text,   
Applicants_only_Last_Graduate_if_available_Transcript_Received text,   
Applicants_only_Research_Interest_1 text,   
Applicants_only_Research_Interest_2 text,   
Applicants_only_Research_Interest_3 text,   
Applicants_only_Research_Interest_4 text,   visa text,   sex text,   
race text,   citizenship text,   
Applicants_only_Interview_Audition_Scheduled_Date text,   
Applicants_only_Interview_Audition_Scheduled_Location text,   
Applicants_only_Interview_Audition_Primary_Request_Date text,   
Applicants_only_Interview_Audition_Secondary_Request_Date text,   
Applicants_only_ASF_Checkbox_reponse text,   
Applicants_only_ASF_TextBox_1_reponse text,   
Applicants_only_ASF_TextBox_2_reponse text, 
Applicants_only_ASF_TextBox_3_reponse text,   
Applicants_only_ASF_TextBox_4_reponse text,   
Applicants_only_ASF_TextBox_5_reponse text,   
Minor text,   Hometown text,   hobbies text,   
Buckley_Confidentiality_Code text,   Birthday text,   
Applicants_only_Evaluations_1 text,   Applicants_only_Evaluations_2 text,   
Applicants_only_Evaluations_3 text,   Applicants_only_Evaluations_4 text,   
Applicants_only_Evaluations_5 text,   Applicants_only_Evaluations_6 text,   
Applicants_only_Evaluations_7 text,   Applicants_only_Evaluations_8 text,   
Applicants_only_Evaluations_9 text,   Applicants_only_Evaluations_10 text,   
Applicants_only_Evaluations_11 text,   Applicants_only_Evaluations_12 text,   
Applicants_only_Evaluations_13 text,   Applicants_only_Evaluations_14 text,   
Applicants_only_Aid_Request text,   Financial_Aid_this_sem_1_Semester text,   
Financial_Aid_this_sem_1_Department_offering text,   Financial_Aid_this_sem_1_PHR_ID text,   
Financial_Aid_this_sem_1_Type text,   Financial_Aid_this_sem_2_Semester text,   
Financial_Aid_this_sem_2_Department_offering text,   Financial_Aid_this_sem_2_PHR_ID text,   
Financial_Aid_this_sem_2_Type text,   forFuture1 text,   
forFuture2 text,   forFuture3 text,   forFuture4 text,   
forFuture5 text,   forFuture6 text,   forFuture7 text,   
forFuture8 text,   forFuture9 text,   forFuture10 text,   
forFuture11 text,   forFuture12 text,   forFuture13 text,   
forFuture14 text,   forFuture15 text,   forFuture16 text);'''

curs.execute(qry_create_directory)

with open("../evaluation/db/directory_tab.csv", "r+") as infile:
    dr = csv.DictReader(infile, delimiter = ',')
    to_db = [(i['Last_name'], i['first_name'], i['middle_name'], i['UID'],\
            i['Applicants_only_sem'], i['email'], i['birthdate'], i['major'],\
            i['program_code'], i['advisor'], i['street1'], i['street2'], i['street3'], i['city'],\
            i['state'], i['zip'], i['country'], i['degree_name'], i['Applicants_only_GRE_v'], i['Applicants_only_GRE_a'],\
            i['Applicants_only_GRE_q'], i['Applicants_only_GRE_v_percentile'], i['Applicants_only_GRE_a_percentile'],\
            i['Applicants_only_GRE_q_percentile'], i['Applicants_only_rating'], i['Applicants_only_TWE'], i['Applicants_only_TOEFL'],\
            i['Applicants_only_GMAT'], i['Applicants_only_MAT_Miller'], i['Applicants_only_MAT_New_Miller_New_Score_range'],\
            i['Applicants_only_LSAT'], i['Certification_if_applicable'], i['Special_Program_if_applicable'],\
            i['Applicants_only_GRE_Subject_Score'], i['Applicants_only_GRE_Subject_Percentile'],\
            i['Applicants_only_GRE_Subject_Name'], i['Applicants_only_Dept_Admission_Dec'], i['Applicants_only_GS_Admission_Dec'],\
            i['Applicants_only_Dept_provision_codes'], i['Applicants_only_GS_provision_codes'], i['Applicants_only_GPA_Undergrad'],\
            i['Home_Phone'], i['Work_Phone'], i['Is_International'], i['Applicants_only_ASF_Submit'],\
            i['Applicants_only_Recommendation_1_Name'], i['Applicants_only_Recommendation_1_Received'],\
            i['Applicants_only_Recommendation_2_Name'], i['Applicants_only_Recommendation_2_Received'],\
            i['Applicants_only_Recommendation_3_Name'], i['Applicants_only_Recommendation_3_Received'],\
            i['Local_address_street1'], i['Local_address_street2'], i['Local_address_street3'], i['Local_address_city'],\
            i['Local_address_state'], i['Local_address_zip'], i['Local_address_country'], i['Applicants_only_Num_Publications'],\
            i['Last_Undergrad_Univ_code'], i['Applicants_only_Last_Undergrad_univs_Tier'], i['Last_Undergrad_univs_Long_Name'],\
            i['Applicants_only_Last_Undergrad_univs_ASF_entered_GPA'], i['Applicants_only_Last_Undergrad_Univ_ASF_entered_Major_Department'],\
            i['Applicants_only_Last_Undergrad_if_available_Transcript_Received'], i['Applicants_only_Last_Graduate_Univ_code'],\
            i['Applicants_only_Last_Graduate_univs_Tier'], i['Applicants_only_Last_Graduate_univs_Long_Name'],\
            i['Applicants_only_Last_Graduate_univs_ASF_entered_GPA'], i['Applicants_only_Last_Graduate_Univ_ASF_entered_Major_Department'],\
            i['Applicants_only_Last_Graduate_if_available_Transcript_Received'], i['Applicants_only_Research_Interest_1'], i['Applicants_only_Research_Interest_2'],\
            i['Applicants_only_Research_Interest_3'], i['Applicants_only_Research_Interest_4'], i['visa'], i['sex'], i['race'], i['citizenship'],\
            i['Applicants_only_Interview_Audition_Scheduled_Date'], i['Applicants_only_Interview_Audition_Scheduled_Location'],\
            i['Applicants_only_Interview_Audition_Primary_Request_Date'], i['Applicants_only_Interview_Audition_Secondary_Request_Date'],\
            i['Applicants_only_ASF_Checkbox_reponse'], i['Applicants_only_ASF_TextBox_1_reponse'], i['Applicants_only_ASF_TextBox_2_reponse'],\
            i['Applicants_only_ASF_TextBox_3_reponse'], i['Applicants_only_ASF_TextBox_4_reponse'], i['Applicants_only_ASF_TextBox_5_reponse'],\
            i['Minor'], i['Hometown'], i['hobbies'], i['Buckley_Confidentiality_Code'], i['Birthday'],\
            i['Applicants_only_Evaluations_1'], i['Applicants_only_Evaluations_2'], i['Applicants_only_Evaluations_3'],\
            i['Applicants_only_Evaluations_4'], i['Applicants_only_Evaluations_5'], i['Applicants_only_Evaluations_6'],\
            i['Applicants_only_Evaluations_7'], i['Applicants_only_Evaluations_8'], i['Applicants_only_Evaluations_9'],\
            i['Applicants_only_Evaluations_10'], i['Applicants_only_Evaluations_11'], i['Applicants_only_Evaluations_12'],\
            i['Applicants_only_Evaluations_13'], i['Applicants_only_Evaluations_14'], i['Applicants_only_Aid_Request'],\
            i['Financial_Aid_this_sem_1_Semester'], i['Financial_Aid_this_sem_1_Department_offering'], i['Financial_Aid_this_sem_1_PHR_ID'],\
            i['Financial_Aid_this_sem_1_Type'], i['Financial_Aid_this_sem_2_Semester'], i['Financial_Aid_this_sem_2_Department_offering'],\
            i['Financial_Aid_this_sem_2_PHR_ID'], i['Financial_Aid_this_sem_2_Type'], i['forFuture1'], i['forFuture2'], i['forFuture3'],\
            i['forFuture4'], i['forFuture5'], i['forFuture6'], i['forFuture7'], i['forFuture8'], i['forFuture9'], i['forFuture10'],\
            i['forFuture11'], i['forFuture12'], i['forFuture13'], i['forFuture14'], i['forFuture15'], i['forFuture16']) for i in dr]

qry_insert_directory = '''INSERT INTO directory ( 
      Last_name,  first_name,  middle_name,  UID,  Applicants_only_sem,  email,  
      birthdate,  major,  program_code,  advisor,  street1,  street2,  street3,
      city,  state,  zip,  country,  degree_name,  Applicants_only_GRE_v,
      Applicants_only_GRE_a,  Applicants_only_GRE_q,
      Applicants_only_GRE_v_percentile,  Applicants_only_GRE_a_percentile,
      Applicants_only_GRE_q_percentile, Applicants_only_rating,  
      Applicants_only_TWE,  Applicants_only_TOEFL,  Applicants_only_GMAT,  
      Applicants_only_MAT_Miller,  
      Applicants_only_MAT_New_Miller_New_Score_range,  Applicants_only_LSAT,  
      Certification_if_applicable,  Special_Program_if_applicable,  
      Applicants_only_GRE_Subject_Score,  Applicants_only_GRE_Subject_Percentile,  
      Applicants_only_GRE_Subject_Name,  Applicants_only_Dept_Admission_Dec, 
      Applicants_only_GS_Admission_Dec,  Applicants_only_Dept_provision_codes,  
      Applicants_only_GS_provision_codes,  Applicants_only_GPA_Undergrad,  
      Home_Phone,  Work_Phone,  Is_International,  
      Applicants_only_ASF_Submit,  Applicants_only_Recommendation_1_Name,  
      Applicants_only_Recommendation_1_Received,  
      Applicants_only_Recommendation_2_Name,  
      Applicants_only_Recommendation_2_Received,  
      Applicants_only_Recommendation_3_Name,  
      Applicants_only_Recommendation_3_Received,  
      Local_address_street1,  Local_address_street2,  Local_address_street3,
      Local_address_city,  Local_address_state,  Local_address_zip,  
      Local_address_country,  Applicants_only_Num_Publications,  
      Last_Undergrad_Univ_code,  Applicants_only_Last_Undergrad_univs_Tier,  
      Last_Undergrad_univs_Long_Name,  
      Applicants_only_Last_Undergrad_univs_ASF_entered_GPA,  
      Applicants_only_Last_Undergrad_Univ_ASF_entered_Major_Department,  
      Applicants_only_Last_Undergrad_if_available_Transcript_Received,  
      Applicants_only_Last_Graduate_Univ_code,  
      Applicants_only_Last_Graduate_univs_Tier,  
      Applicants_only_Last_Graduate_univs_Long_Name,  
      Applicants_only_Last_Graduate_univs_ASF_entered_GPA,  
      Applicants_only_Last_Graduate_Univ_ASF_entered_Major_Department,  
      Applicants_only_Last_Graduate_if_available_Transcript_Received,  
      Applicants_only_Research_Interest_1,  
      Applicants_only_Research_Interest_2,  
      Applicants_only_Research_Interest_3,  
      Applicants_only_Research_Interest_4,  
      visa,  sex,  race,  citizenship,
      Applicants_only_Interview_Audition_Scheduled_Date,  
      Applicants_only_Interview_Audition_Scheduled_Location,  
      Applicants_only_Interview_Audition_Primary_Request_Date,  
      Applicants_only_Interview_Audition_Secondary_Request_Date,  
      Applicants_only_ASF_Checkbox_reponse,  
      Applicants_only_ASF_TextBox_1_reponse,  
      Applicants_only_ASF_TextBox_2_reponse,  
      Applicants_only_ASF_TextBox_3_reponse,  
      Applicants_only_ASF_TextBox_4_reponse,  
      Applicants_only_ASF_TextBox_5_reponse,  
      Minor,  Hometown,  hobbies,  Buckley_Confidentiality_Code,  
      Birthday,  Applicants_only_Evaluations_1,  
      Applicants_only_Evaluations_2,  Applicants_only_Evaluations_3,  
      Applicants_only_Evaluations_4,  Applicants_only_Evaluations_5,  
      Applicants_only_Evaluations_6,  Applicants_only_Evaluations_7,  
      Applicants_only_Evaluations_8,  Applicants_only_Evaluations_9,  
      Applicants_only_Evaluations_10,  Applicants_only_Evaluations_11,  
      Applicants_only_Evaluations_12,  Applicants_only_Evaluations_13,  
      Applicants_only_Evaluations_14,  Applicants_only_Aid_Request,  
      Financial_Aid_this_sem_1_Semester,  
      Financial_Aid_this_sem_1_Department_offering,  
      Financial_Aid_this_sem_1_PHR_ID,  Financial_Aid_this_sem_1_Type,  
      Financial_Aid_this_sem_2_Semester,  
      Financial_Aid_this_sem_2_Department_offering,  
      Financial_Aid_this_sem_2_PHR_ID,  
      Financial_Aid_this_sem_2_Type,  
      forFuture1,  forFuture2,  forFuture3,  forFuture4,  forFuture5,  
      forFuture6,  forFuture7,  forFuture8,  forFuture9,  forFuture10,  
      forFuture11,  forFuture12,  forFuture13,  forFuture14,  forFuture15,  
      forFuture16) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
      ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
      ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
      ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
      ?,?,?,?);
'''
curs.executemany(qry_insert_directory, to_db)
conn.commit()



def valuegen(x):
	p = ''
	for y in x:
		p += "?,"
	p = '('+p[:len(p)-1]+')'
	return p




#Foot notes
#http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
