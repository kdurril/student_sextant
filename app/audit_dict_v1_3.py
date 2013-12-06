#!/usr/bin/env python
#-*- coding: utf-8 -*-

import audit_sql.py
import sqlite3

## A student's goal is to graduate. To graduate, each student must complete a specialization
## Each specialization requires 3 parts: core requirements, specailization requirements and electives, and general electives
## Requirements need that all of a set (such as SOC requires 610 and 611) or a subset where 1 or more members of the set fulfills the requirement without regard to order
## General electives must equal the difference between the required courses the 48 units needed to graduate
## When a student completes the core requirement, the specialization electives and the general electives, the student can graduate, given it is within 5 years of beginning the program


## Student's course list should be a set, where each member is included only once, to avoid counting courses that have been taken twice
## The dictionary {Course: , MinReq: } pairs courses and the minimum quantity of courses from that set that are required for fulfillment
## The check fullfillment function will use the 
## If the all of the components are required, MinReq == len(x[Course]), the test could be made into as set().issubset(UID) type test

## Use set operations to determine how students may complete two specializations, given their currrent courses
## The union of the current and proposed additional specialization should not cause the student to increase the number of semesters until the student graduates
## The difference of the student's current courses and specialization requirements will tell what the student has left to take
## Testing the current courses against all specializations can determine which specialization will allow the student to finish soonest

## functions that determine outputs may become a class with methods such as:
## Core completion, Specialization completion, Elective completion, Graduation requirements completed
## Additional courses needed, additional semesters needed, specializations completed, specializations that can be added within a given number of semesters
## Specializations that can be completed without going over 48 units
## Which specialization allows a student to finish soonest given existing courses
## Number of additional semesters if you take 4, 3, 2 or 1 classes in each additional semesters
## Number of semesters needed if Winter/Summer courses are taken

## Reinvision this as an optimization problem
## Objective function: finish by Fall 2014, complete all requirements and min credits
## Constraints: Complete IDEV and ISEP
## Changing variables: courses, Semester, general elective courses

## Testing
## A course audit needs a test for each program case
## this includes the standard programs
## 
## as well as those who have been
## in multiple programs at UMD 
#  such as which includes those who have been undergrads).
## count of secondary or degree is 2 or greater
## 107038661 for POSI, masters and non-PUAF masters
## 108344945 for undergrad and masters
## 109939539 for BAMPP
## 109421515 for BAMPP and other masters program
## 112738358 for MPP who left program
## 112584269 for MPP traditional first year
## 110728443 for MPP with a waiver of continuous registration and part time
## 102720516 for MPM with spring start



## To adequately project a graduation semester, the semester when a course may be taken must be a factor

## The information on each student is stored in MEGS.
## Idealy, we should process all MPP students from the database with semester availability appended


## Test cases
## find new test cases
# a bampp, bapo, phd, undergrad and mapo but not bampp, advanced special student
test_uid = [] 

## Semester list
semester = ((str(y)+str(x)) for y in range(12,20) for x in ['01','05','08', '12'])

## Program reqs
## program = {"Minreq": ##, "Project": "Yes/No"}
MPP = {"Minreq": 48, "Project": 'Yes'}
MPM = {"Minreq": 36, "Project": 'No'}
PhD = {"Minreq": 24, "Project": 'No', "Qualifiers": 'Yes'} 
MPPMBA = {"Minreq": 66, "Project": 'Yes'}
BAMPP = {"Minreq": 48, "Project": 'Yes'}
MPPJD = {"Minreq": 48, "Project": 'Yes'}
CONS = {"Minreq": 60, "Project": 'Yes'}
MEPP = {"Minreq": 39, "Project": 'Yes'}

#Coursework requirements include two primary parts: core and specialization
#both part have the same functionality: complete a minimum of listed courses


## Core components
Stats = {"Course": ['PUAF610', 'PUAF611'], "MinReq": 1, "label": 'Statistics'}
Micro = {"Course": ['PUAF640'], "MinReq": 1, "label": "MicroEcon",\
         "waiver": ['PUAF689x']}
Macro_fin = {"Course": ['PUAF641', 'PUAF670'], "MinReq": 1,\
             "label": 'MacroEcon/Finance'}
Macro = {"Course": ['PUAF641'], "MinReq": 1, "label": 'MacroEcon'}
Fin = {"Course": ['PUAF641', 'PUAF670'], "MinReq": 1, "label": 'Finance'}
Ethics = {"Course": ['PUAF620', 'PUAF650', 'PUAF711'], "MinReq": 3,\
          "label": 'Political, Ethical and Management Analysis'}
Project = {"Course": ['PUAF790'], "MinReq": 1,\
           "label": 'Project Course'}

CORE = [Stats, Micro, Macro, Ethics]
CORE_MFL = [Stats, Micro, Fin, Ethics]
CORE_ISEP = [Stats, Micro, Macro, Ethics]


def coursepull(specialization):
    'Build a course superset of the specialization requirements'
    
    component = [x['Course'][:x['MinReq']] for x in specialization]
    flat = list()

    while component:
        entry = component.pop()
        if isinstance(entry, list):
            component.extend(entry)
        else:
            flat.append(entry)
    return flat
    

##Environmental Policy

#Components
#ENV Core
ENV_1 = {"Course":['PUAF740', 'PUAF741', 'PUAF745'], "MinReq": 3,\
         "label": "ENV Req 1"}

#ENV Electives 
ENV_2 = {"Course":['PUAF698B','PUAF698L', 'PUAF698W', 'PUAF699Z', 'PUAF742',\
                   'PUAF743', 'PUAF744', 'PUAF746', 'PUAF798L','PUAF798T'],\
                 "MinReq": 1, "label": "ENV Req 2"}

#ENV Project Course. Only ENV has multiple ENV courses
ENV_Project = {"Course": ['PUAF660', 'PUAF790'], "MinReq": 1,\
               "label": "ENV Project"}

ENV = [Stats, Micro, Macro_fin, Ethics, ENV_1, ENV_Project]

## Energy Policy
ERG_1 = {"Course": ['PUAF699'], "MinReq": 1, "label": "Energy Policy 1"}
ERG_2 = {"Course": ['PUAF798N', 'PUAF798O', 'PUAF798K'], "MinReq": 1,\
         "label": "Energy Policy 2"}

ENGY = [Stats, Micro, Macro_fin, Ethics, ENV_1, ERG_1, ERG_2, ENV_Project]

##International Development
#Components
IDEV_1 = {"Course": ['PUAF698R','PUAF699J'], "MinReq": 1, "label": "IDEV Req 1"}
IDEV_2 = {"Course": ['PUAF781', 'PUAF782'], "MinReq": 2, "label": "IDEV Req 2"}
IDEV_3 = {"Course": ['PUAF611', 'PUAF699K','PUAF720', 'PUAF698O', 'PUAF699D',\
                     'PUAF699K', 'PUAF699Q', 'PUAF798C', 'PUAF798E', 'PUAF698I',\
                     'PUAF798T'], "MinReq": 1, "label": "IDEV Req 3"}


IDEV = [Stats, Micro, Macro, Ethics, IDEV_1, IDEV_2, Project]


##International Security and Economic Policy
#Components
ISEP_1 = {"Course":['PUAF720','PUAF780', 'PUAF781'], "MinReq": 3,\
          "label": "ISEP Req 1"}

ISEP = [Stats, Micro, Macro, Ethics, ISEP_1, Project]

##Management, Leadership and Finance
#Leadership and Management Components
LM_1 =  {"Course": ['PUAF698P', 'PUAF798Y', 'PUAF689Y', 'PUAF689Z'],\
         "MinReq": 2, "label": "LM Req 1"}
LM_2 = {"Course": ['PUAF752', 'PUAF753'], "MinReq": 1, "label": "LM Req 2"}

LM = [Stats, Micro, Fin, Ethics, LM_1, LM_2, Project]

#Public Sector Financial Management Components
PSFM_1 = {"Course": ['PUAF699E', 'PUAF712','PUAF716','PUAF717'], "MinReq": 3,\
          "label": "PSFM Req 1"} 
PSFM_2 = {"Course": ['PUAF698P', 'PUAF699C','PUAF752','PUAF753'], "MinReq": 1,\
          "label": "PSFM Req 2"}

PSFM = [Stats, Micro, Fin, Ethics, PSFM_1, PSFM_2, Project]

# Acquisitions Management
ACQ_1 = {"Course": ['PUAF689A', 'PUAF698G', 'PUAF689F'], "MinReq": 3,\
         "label": "ACQ Req 1"}

ACQ = [Stats, Micro, Fin, Ethics, ACQ_1, Project]

# Nonprofit Management Focus, must be completed in addition to another specialization
NML_1 = {"Course": [ 'PUAF798Y'], "MinReq": 1, "label": "NPM Req 1"}
NML_2 = {"Course": [ 'PUAF689Y', 'PUAF689Z'], "MinReq": 2, "label": "NPM Req 2"} 
#This will be the nonprofit management finance course
NML_3 = {"Course": [ 'PUAF689L'], "MinReq": 1, "label": "NPM Req 3"} 

NML = [Stats, Micro, Fin, Ethics, NML_1, NML_2, NML_3, Project]

#Social Policy
#Soc
Soc_1 = {"Course": ["PUAF611", 'PUAF734', 'PUAF689E'], "MinReq": 2, "label": "Soc Req"}

#Health
Health_1 = {"Course": ['PUAF698G','PUAF698K', 'PUAF699D'], "MinReq": 1, "label": "Health_1 Req"}
Health_2 = {"Course": ['PUAF735'], "MinReq": 1, "label": "Health_2 Req"}

#EDUC
Educ_1 = {"Course": ['PUAF732', 'EDPL615'],\
          "MinReq": 2, "label": "Edu Req"}

SOC = [Stats, Micro, Macro_fin, Ethics, Soc_1, Project]
HLTH = [Stats, Micro, Macro_fin, Ethics, Soc_1, Health_1, Health_2, Project]
EDUC = [Stats, Micro, Macro_fin, Ethics, Soc_1, Educ_1, Project]


All = [ENV, ENGY, IDEV, ISEP, LM, PSFM, ACQ, NML, SOC, EDUC, HLTH]
All_label = ['ENV', 'ENGY', 'IDEV', 'ISEP', 'LM', 'PSFM', 'ACQ', 'NPM', 'SOC', 'EDUC', 'HLTH']

#Use All_dict as a lookup table to place the specialization objects for specialization strings
All_dict = {'ENV': ENV, 'ENGY': ENGY, 'IDEV': IDEV, 'ISEP': ISEP, 'LM': LM, 'PSFM': PSFM, 'ACQ': ACQ, 'NML': NML, 'SOC': SOC, 'EDUC': EDUC, 'HLTH': HLTH}

## Check for fulfillments
## useful if partial set required to meet requirement

## Check fulfillment with dictionary

        
        
## Determine which specialization the student is closest to finishing
def closest(UID):
        return [len(leastreduce([leastremain(UID,x) for x in y])) for y in All]

def coursepull(specialization):
    '''flatten the courses of a specialization'''
    component = [x['Course'][:x['MinReq']] for x in specialization]
    flat = list()
    while component:
        entry = component.pop()
        if isinstance(entry, list):
            component.extend(entry)
        else:
            flat.append(entry)
    return flat

# A class to contain the UID object and its methods
# 
class CourseReview(list):
        '''initialize the object, create as a list'''
        def __init__(self,UID):
                list.__init__(self, UID)
                self.UID = UID

        
        def course_complete(self, requirement):
                '''return the completed requirement'''
                '''the intersection of the requirement and the student's courses'''
                return set(requirement["Course"]).intersection(self)
                
                
        def course_remainder(self, requirement):
                '''return the required courses that the student has not taken'''
                '''this is the difference of the student's courses from the requirement'''
                return set(requirement["Course"]).difference(self)

        def specialization_complete(self, specialization):
                "return the completed courses from a specialization"
                classlist1 = []
                [classlist1.append(self.course_complete(x)) for x in specialization]
                return classlist1

        def specialization_remainder(self, specialization):
                "return the remaining courses from a specialization"
                classlist1 = []
                [classlist1.append(self.course_remainder(x)) for x in specialization]
                return classlist1

        def req_fulfilled(self, requirement):
                '''return true for fulfilled requirement, else,
                return remainder of courses in requirement'''
                if len(self.course_complete(requirement)) >= requirement["MinReq"]:
                        return True
                else:
                        return self.course_remainder(requirement)

        def specialization_fulfilled(self, specialization):
                "check for completed specialization or return courses needed for completetion"
                req_list = []
                for x in specialization:
                        # x is a requirement
                        req_list.append(self.req_fulfilled(x))
                if req_list.count(True) == len(req_list):
                        return True
                else:
                        req_remain = []
                        [req_remain.extend(x) for x in req_list if x != True]

                        return req_remain
                # this needs to account for just the min req for a requirement
                # if I need to count the remaining reqs

        
class CourseAudit(dict):
        '''initialize the object, create as a list'''
        def __init__(self,UID):
                dict.__init__(self, UID)
                self.UID = UID
                
        def audit_report(self):

            y = All_dict[self['specialization']]
            
            report_out = '''
            Program Audit

            Dear {student_name},

            The following is an audit of your progress as a student in
            the School of Public Policy at the University of Maryland.

            Our records indicate that you are enrolled in the {degree_program} program and
            are pursuing the {specialization} specialization.

            You have completed the following courses:
            {specialization_complete}

            You must complete the following courses:
            {specialization_remainder}

            '''.format(student_name = self['name'],\
                       degree_program = self['degree'],\
                       specialization = self['specialization'],\
                       specialization_complete = list(self['allcourse'].specialization_complete(y)),\
                       specialization_remainder = list(self['allcourse'].specialization_remainder(y))
                       )
            return report_out   
        

        def report(self, Specialization):
                if Specialization == ENV:
                        label = "ENV"
                elif Specialization == IDEV:
                        label = "IDEV"
                elif Specialization == ISEP:
                        label = "ISEP"
                elif Specialization == LM:
                        label = "LM"
                elif Specialization == PSFM:
                        label = "PSFM"
                elif Specialization == SOC:
                        label = "SOC"
                elif Specialization == HEALTH:
                        label = "HEALTH"
                elif Specialization == EDUC:
                        label = "EDUCATION"
                elif Specialization == ACQ:
                         label = "Acquistions"
                elif Specialization == NPM:
                         label = "Non-Profit Management"
                print ("Summary of Status")
                print ("You have completed approximately {0} credits of the 48 credits that you need to graduate.".format("credit"))

                print ("You need to complete at least {0} more 3-credit classes.".format("count"))
        
                print ("\n")
                print ("Core")
                print ("You have completed {0} of 6 core requirements. You need to complete the following requirement(s) {1}."\
                .format("core", "core remainning"))
                print ("For the {0} specialization, you have completed {1} of the 4 requirements. \n"\
                      .format(str(label), "a number"))
                
                
                print ("Expect to graduate after {0} additional semesters".format())


def audit_report(x):

    y = All_dict[x['specialization']]
    
    report_out = '''
    Program Audit

    Dear {student_name},

    The following is an audit of your progress as a student in
    the School of Public Policy at the University of Maryland.

    Our records indicate that you are enrolled in the {degree_program} and
    are pursuing the {specialization} specialization.

    You have completed the following courses:
    {specialization_complete}

    You must complete the following courses:
    {specialization_remainder}

    '''.format(student_name = x['name'],\
               degree_program = x['degree'],\
               specialization = x['specialization'],\
               specialization_complete = x['allcourse'].specialization_complete(y),\
               specialization_remainder = x['allcourse'].specialization_remainder(y)
               )
    return report_out

qry_current_sem = PUAFdb.curs.execute(audit_sql.qry_current_sem)
qry_current_sem = qry_current_sem.fetchall()

nongrad = PUAFdb.curs.execute(audit_sql.nongrad_puafonly)
qry_nongrad = nongrad.fetchall()

qry_ass = PUAFdb.curs.execute(audit_sql.qry_ass)
qry_ass = qry_ass.fetchall()


view_current = PUAFdb.curs.execute(audit_sql.qry_cp_alt)
view_current = view_current.fetchall()

UIDlist = PUAFdb.curs.execute(audit_sql.qry_directory)
UIDlist = PUAFdb.curs.fetchall()


def dlist(UIDlist, view_current):
        '''Add a dictionary of the courses (or attribute) to the cur_dlist'''
        #UIDlist contains UIDs
        #view_current is view/table with UID and Courses
        
        cur_dlist = [] # current dictionary list
        
        #add UID key and UID to list
        for x in UIDlist:
                cur_dlist.append({'UID': x[0]})

        #add courses from current courses table
        for x in cur_dlist:
            h = []
            for y in view_current:
                if x['UID'] == y[0]:
                    h.append(y[1])
            x['courselist'] = h

        #add total credits
        for x in cur_dlist:
                h = 0
                for y in view_current:
                        if x['UID'] == y[0]:
                                h += int(y[2])
                x['credit'] = h

        #add name, specialization and degree to dictionary

        for x in cur_dlist:
                for y in UIDlist:
                        if x["UID"] == y[0]:
                                x["name"] = "{0}, {1}".format(y[1],y[2])
                                x["specialization"] = y[3]
                                x["degree"] = y[4]
                
        #convert the courselist to CourseReview       
        for x in cur_dlist:
                x['courselist'] = CourseReview(x['courselist'])

                

        return cur_dlist

def uid_dict(container, qry):
        "add keys and content"
        #add courses from current courses table
        for x in container:
                h = []
                for y in qry:
                        if x['UID'] == y[0]:
                                h.append(y[1])
                                x['credit'] += int(y[2])
                                
                x['coursenow'] = h


def assgrad(dlist, qry):
        '''match the UID and add the advanced special student courses'''
        for x in dlist:
                h = []
                for y in qry:
                        if x['UID'] == y[0]:
                                h.append(y[3])
                                if y[3] not in x['courselist']:
                                        x['credit'] += int(y[5])
                                
                x['ass'] = h

	

def pregrad(dlist, qry):
        '''match the UID and add the nongrad courses, find BAMPP students'''
        for x in dlist:
                h = []
                for y in qry:
                        if x['UID'] == y[0]:
                                if int(y[3][4:7]) > 600:
                                        if y[3] not in x['courselist']:
                                                x['courselist'].append(y[3])
                                                x['credit'] += int(y[5])
                                                
                                        else:
                                                h.append(y[3])
                                                
                                                
                x['nongrad'] = h
                                                                        

        
# Dictionary building section - this can be remade into a class
# alist is primary dictionary of 
alist = dlist(UIDlist, view_current)
uid_dict(alist, qry_current_sem)
assgrad(alist, qry_ass)
pregrad(alist, qry_nongrad)

def allcourse():
        for x in alist:
                x['allcourse'] = []
                [x['allcourse'].append(d) for d in x['ass']]
                [x['allcourse'].append(d) for d in x['coursenow']]
                [x['allcourse'].append(d) for d in x['nongrad']]
                [x['allcourse'].append(d) for d in x['courselist']]
                x['allcourse'] = set(x['allcourse'])
                x['allcourse'] = CourseReview(x['allcourse'])

allcourse()

#alist[54]['allcourse'].specialization_fulfilled(All_dict[alist[54]['specialization']])
