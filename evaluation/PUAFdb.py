#! /usr/bin/env python
#-*- coding: utf-8 -*-
import csv, sqlite3, sys

#sqlite3 db from student records

conn = sqlite3.connect(":memory:")
curs = conn.cursor()

#Create start table
curs.execute("CREATE TABLE start (ID integer PRIMARY KEY autoincrement, UID Integer,     M_Start text,      M_Finish text,    M_Graduate text,  P_Start text,     P_Finish text,    P_Graduate text,  C_Start text, C_Finish text);")
with open("../evaluation/db/student_startdate_tab.csv", "r+") as infile:
      dr = csv.DictReader(infile, delimiter='\t')
      to_db = [(i['UID'],  i['M_Start'],     i['M_Finish'],    i['M_Graduate'],  i['P_Start'],     i['P_Finish'],    i['P_Graduate'],  i['C_Start'], i['C_Finish']) for i in dr]
curs.executemany("INSERT INTO start (UID, M_Start, M_Finish, M_Graduate, P_Start, P_Finish, P_Graduate, C_Start, C_Finish) VALUES (?,?,?,?,?,?,?,?,?);", to_db)
conn.commit()

#Create the student table
curs.execute("CREATE TABLE student (ID integer PRIMARY KEY autoincrement, UID INTEGER, Sem integer, Class text, Core text, Section text, Description text, Transfer text, Spec_Att text, Credits text, Grade text, Current text);")
with open("../evaluation/db/student_records_tab.csv", "r+") as infile:
	dr = csv.DictReader(infile, delimiter = '\t')
	to_db = [(i['UID'], i['Sem'], i['Class'], i['Core'], i['Section'], i['Description'], i['Transfer'], i['Spec_Att'], i['Credits'], i['Grade'], i['Current']) for i in dr]

curs.executemany("INSERT INTO student (UID, Sem, Class, Core, Section, Description, Transfer, Spec_Att, Credits, Grade, Current) VALUES (?,?,?,?,?,?,?,?,?,?,?);", to_db)
conn.commit()

#Create reg table
curs.execute("CREATE TABLE reg (ID integer PRIMARY KEY autoincrement, UID integer, Sem integer, Fulltime_sis text, Fulltime_our text, Eligible text, Off_campus text, M text, P text, C text, Degree text, Secondary text, Continue text);")
with open("../evaluation/db/student_reg_tab.csv", "r+") as infile:
	dr = csv.DictReader(infile, delimiter = '\t')
	to_db = [(i['UID'], i['Sem'], i['Fulltime_sis'], i['Fulltime_our'], i['Eligible'], i['Off_campus'], i['M'], i['P'], i['C'], i['Degree'], i['Secondary'], i['Continue']) for i in dr]

curs.executemany("INSERT INTO reg (UID, Sem, Fulltime_sis, Fulltime_our, Eligible, Off_campus, M, P, C, Degree, Secondary, Continue) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);", to_db)
conn.commit()


#Create directory table
qry_create_directory = "CREATE TABLE directory (Last_name text, first_name text, middle_name text, UID  integer INTEGER PRIMARY KEY ASC, sem text, email text, birthdate text, major text, program_code text, advisor text, street1 text, street2 text, street3 text, city text, state text, zip text, country text, degree_name text, GRE_v text, GRE_a text, GRE_q text, GRE_v_percentile text, GRE_a_percentile text, GRE_q_percentile text, rating text, TWE text, TOEFL text, GMAT text, MAT_Miller text, MAT_New_Miller_New_Score_range text, LSAT text, Certification text, Special_Program text, GRE_Subject_Score text, GRE_Subject_Percentile text, GRE_Subject_Name text, Dept_Admission_Dec text, GS_Admission_Dec text, Dept_provision_codes text, GS_provision_codes text, GPA_undergrad text, Home_Phone text, Work_Phone text, Is_International text, ASF_Submit text, Recommendation_1_Name text, Recommendation_1_Received text, Recommendation_2_Name text, Recommendation_2_Received text, Recommendation_3_Name text, Recommendation_3_Received text, Local_address_street1 text, Local_address_street2 text, Local_address_street3 text, Local_address_city text, Local_address_state text, Local_address_zip text, Local_address_country text, Num_Publications text, Last_Undergrad_Univ_code text, Last_Undergrad_Univs_Tier text, Last_Undergrad_Univ_Long_Name text, Last_Undergrad_Univ_ASF_entered_GPA text, Last_Undergrad_Univ_ASF_entered_Major_Department text, Last_Undergrad_Univ_Transcript_Received text, Last_Graduate_Univ_code text, Last_Graduate_Univs_Tier text, Last_Graduate_Univ_Long_Name text, Last_Graduate_Univ_ASF_entered_GPA text, Last_Graduate_Univ_ASF_entered_Major_Department text, Last_Graduate_Transcript_Received text, Research_Interest_1 text, Research_Interest_2 text, Research_Interest_3 text, Research_Interest_4 text, visa text, sex text, race text, citizenship text, Interview_Audition_Scheduled_Date text, Interview_Audition_Scheduled_Location text, Interview_Audition_Primary_Request_Date text, Interview_Audition_Secondary_Request_Date text, ASF_Checkbox text, ASF_TextBox_1 text, ASF_TextBox_2 text, ASF_TextBox_3 text, ASF_TextBox_4 text, ASF_TextBox_5 text, Minor text, For_students_only_Hometown text, For_students_only_Hobbies text, For_students_only_Buckley_code text, Birthday_birthdate_with_no_year text, Faculty_Evaluator_1_name text, Faculty_Evaluator_1_rank text, Faculty_Evaluator_2_name text, Faculty_Evaluator_2_rank text, Faculty_Evaluator_3_name text, Faculty_Evaluator_3_rank text, Faculty_Evaluator_4_name text, Faculty_Evaluator_4_rank text, Faculty_Evaluator_5_name text, Faculty_Evaluator_5_rank text, Faculty_Evaluator_6_name text, Faculty_Evaluator_6_rank text, Faculty_Evaluator_7_name text, Faculty_Evaluator_7_rank text, Requested_Financial_Aid text, Financial_Aid_this_sem_1_Semester text, Financial_Aid_this_sem_1_Department_offering text, Financial_Aid_this_sem_1_PHR_ID text, Financial_Aid_this_sem_1_Type text, Financial_Aid_this_sem_2_Semester text, Financial_Aid_this_sem_2_Department_offering text, Financial_Aid_this_sem_2_PHR_ID text, Financial_Aid_this_sem_2_Type text, forFuture1 text, forFuture2 text, forFuture3 text, forFuture4 text, forFuture5 text, forFuture6 text, forFuture7 text, forFuture8 text, forFuture9 text, forFuture10 text, forFuture11 text, forFuture12 text, forFuture13 text, forFuture14 text, forFuture15 text, forFuture16 text);"

curs.execute(qry_create_directory)

# directory_tab.csv should be an ASCII file
with open("../evaluation/db/directory_tab.csv", "r+") as infile:
    dr = csv.DictReader(infile, delimiter = ',')
    to_db = [(i['Last_name'], i['first_name'], i['middle_name'], i['UID'],\
    i['sem'], i['email'], i['birthdate'], i['major'], i['program_code'],\
    i['advisor'], i['street1'], i['street2'], i['street3'], i['city'],\
    i['state'], i['zip'], i['country'], i['degree_name'], i['GRE_v'],\
    i['GRE_a'], i['GRE_q'], i['GRE_v_percentile'], i['GRE_a_percentile'],\
    i['GRE_q_percentile'], i['rating'], i['TWE'], i['TOEFL'], i['GMAT'],\
    i['MAT_Miller'], i['MAT_New_Miller_New_Score_range'], i['LSAT'],\
    i['Certification'], i['Special_Program'], i['GRE_Subject_Score'],\
    i['GRE_Subject_Percentile'], i['GRE_Subject_Name'],\
    i['Dept_Admission_Dec'], i['GS_Admission_Dec'], i['Dept_provision_codes'],\
    i['GS_provision_codes'], i['GPA_undergrad'], i['Home_Phone'],\
    i['Work_Phone'], i['Is_International'], i['ASF_Submit'],\
    i['Recommendation_1_Name'], i['Recommendation_1_Received'],\
    i['Recommendation_2_Name'],\
    i['Recommendation_2_Received'], i['Recommendation_3_Name'],\
    i['Recommendation_3_Received'], i['Local_address_street1'],\
    i['Local_address_street2'], i['Local_address_street3'],\
    i['Local_address_city'], i['Local_address_state'], i['Local_address_zip'],\
    i['Local_address_country'], i['Num_Publications'],\
    i['Last_Undergrad_Univ_code'], i['Last_Undergrad_Univs_Tier'],\
    i['Last_Undergrad_Univ_Long_Name'],\
    i['Last_Undergrad_Univ_ASF_entered_GPA'],\
    i['Last_Undergrad_Univ_ASF_entered_Major_Department'],\
    i['Last_Undergrad_Univ_Transcript_Received'],\
    i['Last_Graduate_Univ_code'], i['Last_Graduate_Univs_Tier'],\
    i['Last_Graduate_Univ_Long_Name'], i['Last_Graduate_Univ_ASF_entered_GPA'],\
    i['Last_Graduate_Univ_ASF_entered_Major_Department'],\
    i['Last_Graduate_Transcript_Received'], i['Research_Interest_1'],\
    i['Research_Interest_2'], i['Research_Interest_3'],\
    i['Research_Interest_4'], i['visa'], i['sex'], i['race'],\
    i['citizenship'], i['Interview_Audition_Scheduled_Date'],\
    i['Interview_Audition_Scheduled_Location'],\
    i['Interview_Audition_Primary_Request_Date'],\
    i['Interview_Audition_Secondary_Request_Date'], i['ASF_Checkbox'],\
    i['ASF_TextBox_1'], i['ASF_TextBox_2'], i['ASF_TextBox_3'],\
    i['ASF_TextBox_4'], i['ASF_TextBox_5'], i['Minor'],\
    i['For_students_only_Hometown'], i['For_students_only_Hobbies'],\
    i['For_students_only_Buckley_code'], i['Birthday_birthdate_with_no_year'],\
    i['Faculty_Evaluator_1_name'], i['Faculty_Evaluator_1_rank'],\
    i['Faculty_Evaluator_2_name'], i['Faculty_Evaluator_2_rank'],\
    i['Faculty_Evaluator_3_name'], i['Faculty_Evaluator_3_rank'],\
    i['Faculty_Evaluator_4_name'], i['Faculty_Evaluator_4_rank'],\
    i['Faculty_Evaluator_5_name'], i['Faculty_Evaluator_5_rank'],\
    i['Faculty_Evaluator_6_name'], i['Faculty_Evaluator_6_rank'],\
    i['Faculty_Evaluator_7_name'], i['Faculty_Evaluator_7_rank'],\
    i['Requested_Financial_Aid'], i['Financial_Aid_this_sem_1_Semester'],\
    i['Financial_Aid_this_sem_1_Department_offering'],\
    i['Financial_Aid_this_sem_1_PHR_ID'], i['Financial_Aid_this_sem_1_Type'],\
    i['Financial_Aid_this_sem_2_Semester'],\
    i['Financial_Aid_this_sem_2_Department_offering'],\
    i['Financial_Aid_this_sem_2_PHR_ID'],\
    i['Financial_Aid_this_sem_2_Type'], i['forFuture1'], i['forFuture2'],\
    i['forFuture3'], i['forFuture4'], i['forFuture5'], i['forFuture6'],\
    i['forFuture7'], i['forFuture8'], i['forFuture9'], i['forFuture10'],\
    i['forFuture11'], i['forFuture12'], i['forFuture13'], i['forFuture14'],\
    i['forFuture15'], i['forFuture16']) for i in dr]
    
    

qry_insert_directory = '''
INSERT INTO directory ( Last_name, first_name, middle_name, UID, sem, email, birthdate, major, program_code, advisor, street1, street2, street3, city, state, zip, country, degree_name, GRE_v, GRE_a, GRE_q, GRE_v_percentile, GRE_a_percentile, GRE_q_percentile, rating, TWE, TOEFL, GMAT, MAT_Miller, MAT_New_Miller_New_Score_range, LSAT, Certification, Special_Program, GRE_Subject_Score, GRE_Subject_Percentile, GRE_Subject_Name, Dept_Admission_Dec, GS_Admission_Dec, Dept_provision_codes, GS_provision_codes, GPA_undergrad, Home_Phone, Work_Phone, Is_International, ASF_Submit, Recommendation_1_Name, Recommendation_1_Received, Recommendation_2_Name, Recommendation_2_Received, Recommendation_3_Name, Recommendation_3_Received, Local_address_street1, Local_address_street2, Local_address_street3, Local_address_city, Local_address_state, Local_address_zip, Local_address_country, Num_Publications, Last_Undergrad_Univ_code, Last_Undergrad_Univs_Tier, Last_Undergrad_Univ_Long_Name, Last_Undergrad_Univ_ASF_entered_GPA, Last_Undergrad_Univ_ASF_entered_Major_Department, Last_Undergrad_Univ_Transcript_Received, Last_Graduate_Univ_code, Last_Graduate_Univs_Tier, Last_Graduate_Univ_Long_Name, Last_Graduate_Univ_ASF_entered_GPA, Last_Graduate_Univ_ASF_entered_Major_Department, Last_Graduate_Transcript_Received, Research_Interest_1, Research_Interest_2, Research_Interest_3, Research_Interest_4, visa, sex, race, citizenship, Interview_Audition_Scheduled_Date, Interview_Audition_Scheduled_Location, Interview_Audition_Primary_Request_Date, Interview_Audition_Secondary_Request_Date, ASF_Checkbox, ASF_TextBox_1, ASF_TextBox_2, ASF_TextBox_3, ASF_TextBox_4, ASF_TextBox_5, Minor, For_students_only_Hometown, For_students_only_Hobbies, For_students_only_Buckley_code, Birthday_birthdate_with_no_year, Faculty_Evaluator_1_name, Faculty_Evaluator_1_rank, Faculty_Evaluator_2_name, Faculty_Evaluator_2_rank, Faculty_Evaluator_3_name, Faculty_Evaluator_3_rank, Faculty_Evaluator_4_name, Faculty_Evaluator_4_rank, Faculty_Evaluator_5_name, Faculty_Evaluator_5_rank, Faculty_Evaluator_6_name, Faculty_Evaluator_6_rank, Faculty_Evaluator_7_name, Faculty_Evaluator_7_rank, Requested_Financial_Aid, Financial_Aid_this_sem_1_Semester, Financial_Aid_this_sem_1_Department_offering, Financial_Aid_this_sem_1_PHR_ID, Financial_Aid_this_sem_1_Type, Financial_Aid_this_sem_2_Semester, Financial_Aid_this_sem_2_Department_offering, Financial_Aid_this_sem_2_PHR_ID, Financial_Aid_this_sem_2_Type, forFuture1, forFuture2, forFuture3, forFuture4, forFuture5, forFuture6, forFuture7, forFuture8, forFuture9, forFuture10, forFuture11, forFuture12, forFuture13, forFuture14, forFuture15, forFuture16) VALUES ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
'''

curs.executemany(qry_insert_directory, to_db)
conn.commit()

def valuegen(x):
	p = ''
	for y in x:
		p += "?,"
	p = '('+p[:len(p)-1]+')'
	return p


if __name__ == "__main__":
    sys.exit(main())


#Foot notes
#http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
