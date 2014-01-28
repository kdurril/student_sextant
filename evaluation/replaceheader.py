#! /usr/bin/env python
#-*- coding: utf-8 -*-

import codecs

newhead = u'Last_name,first_name,middle_name,UID,Applicants_only_sem,email,birthdate,major,program_code,advisor,street1,street2,street3,city,state,zip,country,degree_name,Applicants_only_GRE_v,Applicants_only_GRE_a,Applicants_only_GRE_q,Applicants_only_GRE_v_percentile,Applicants_only_GRE_a_percentile,Applicants_only_GRE_q_percentile,Applicants_only_rating,Applicants_only_TWE,Applicants_only_TOEFL,Applicants_only_GMAT,Applicants_only_MAT_Miller,Applicants_only_MAT_New_Miller_New_Score_range,Applicants_only_LSAT,Certification_if_applicable,Special_Program_if_applicable,Applicants_only_GRE_Subject_Score,Applicants_only_GRE_Subject_Percentile,Applicants_only_GRE_Subject_Name,Applicants_only_Dept_Admission_Dec,Applicants_only_GS_Admission_Dec,Applicants_only_Dept_provision_codes,Applicants_only_GS_provision_codes,Applicants_only_GPA_Undergrad,Home_Phone,Work_Phone,Is_International,Applicants_only_ASF_Submit,Applicants_only_Recommendation_1_Name,Applicants_only_Recommendation_1_Received,Applicants_only_Recommendation_2_Name,Applicants_only_Recommendation_2_Received,Applicants_only_Recommendation_3_Name,Applicants_only_Recommendation_3_Received,Local_address_street1,Local_address_street2,Local_address_street3,Local_address_city,Local_address_state,Local_address_zip,Local_address_country,Applicants_only_Num_Publications,Last_Undergrad_Univ_code,Applicants_only_Last_Undergrad_univs_Tier,Last_Undergrad_univs_Long_Name,Applicants_only_Last_Undergrad_univs_ASF_entered_GPA,Applicants_only_Last_Undergrad_Univ_ASF_entered_Major_Department,Applicants_only_Last_Undergrad_if_available_Transcript_Received,Applicants_only_Last_Graduate_Univ_code,Applicants_only_Last_Graduate_univs_Tier,Applicants_only_Last_Graduate_univs_Long_Name,Applicants_only_Last_Graduate_univs_ASF_entered_GPA,Applicants_only_Last_Graduate_Univ_ASF_entered_Major_Department,Applicants_only_Last_Graduate_if_available_Transcript_Received,Applicants_only_Research_Interest_1,Applicants_only_Research_Interest_2,Applicants_only_Research_Interest_3,Applicants_only_Research_Interest_4,visa,sex,race,citizenship,Applicants_only_Interview_Audition_Scheduled_Date,Applicants_only_Interview_Audition_Scheduled_Location,Applicants_only_Interview_Audition_Primary_Request_Date,Applicants_only_Interview_Audition_Secondary_Request_Date,Applicants_only_ASF_Checkbox_reponse,Applicants_only_ASF_TextBox_1_reponse,Applicants_only_ASF_TextBox_2_reponse,Applicants_only_ASF_TextBox_3_reponse,Applicants_only_ASF_TextBox_4_reponse,Applicants_only_ASF_TextBox_5_reponse,Minor,Hometown,hobbies,Buckley_Confidentiality_Code,Birthday,Applicants_only_Evaluations_1,Applicants_only_Evaluations_2,Applicants_only_Evaluations_3,Applicants_only_Evaluations_4,Applicants_only_Evaluations_5,Applicants_only_Evaluations_6,Applicants_only_Evaluations_7,Applicants_only_Evaluations_8,Applicants_only_Evaluations_9,Applicants_only_Evaluations_10,Applicants_only_Evaluations_11,Applicants_only_Evaluations_12,Applicants_only_Evaluations_13,Applicants_only_Evaluations_14,Applicants_only_Aid_Request,Financial_Aid_this_sem_1_Semester,Financial_Aid_this_sem_1_Department_offering,Financial_Aid_this_sem_1_PHR_ID,Financial_Aid_this_sem_1_Type,Financial_Aid_this_sem_2_Semester,Financial_Aid_this_sem_2_Department_offering,Financial_Aid_this_sem_2_PHR_ID,Financial_Aid_this_sem_2_Type,forFuture1,forFuture2,forFuture3,forFuture4,forFuture5,forFuture6,forFuture7,forFuture8,forFuture9,forFuture10,forFuture11,forFuture12,forFuture13,forFuture14,forFuture15,forFuture16,forFuture17,forFuture18,forFuture19,forFuture20\n'

def replaceheader():
    #with codecs.open('db/directory_header.csv', 'r+', 'utf-8') as f:
        #newhead = f.read()

    with codecs.open('./db/directory_tab.csv', 'r+', 'utf-8') as g:
        body = g.readlines()

    with codecs.open('./db/directory_tab.csv', 'w+', 'utf-8') as h:
        h.write(newhead)
        for line in body[1:]:
            h.write(line)
