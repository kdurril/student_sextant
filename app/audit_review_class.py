#!/usr/bin/env python
#-*- coding: utf-8 -*-


# A class to contain the UID object and its methods
from math import ceil
# 
class CourseReview(list):
        '''initialize the object, subclass list, create as a list'''
        def __init__(self,UID):
                list.__init__(self, UID)
                self.UID = UID

        
        def course_complete(self, requirement):
                '''return the completed requirement'''
                '''the intersection of the requirement and the student's courses'''
                
                complete = set(requirement["Course"]).intersection(self)
                return [{'Complete': list(complete),\
                         'Incomplete':[x for x in requirement["Course"] if x not in complete and len(complete) < requirement['MinReq']],\
                         'MinReq': requirement['MinReq']}]

                
        def course_remainder(self, requirement):
                '''return the required courses that the student has not taken'''
                '''this is the difference of the student's courses from the requirement'''
                remains = set(requirement["Course"]).difference(self)
                return remains
                
                #elif requirement['MinReq'] > 1:
                #        return ["{0} {1}{2}".format(\
                #                'Complete at least', requirement['MinReq'],\
                #                'of the following:')].extend(remains)
                
                        


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
                        return [True]
                else:
                        return self.course_remainder(requirement)

        def specialization_fulfilled(self, specialization):
                "check for completed specialization or return courses needed for completetion"
                req_list = []
                for x in specialization:
                        # x is a requirement
                        req_list.append(self.req_fulfilled(x))
                if req_list.count(True) == len(req_list):
                        return [True]
                else:
                        req_remain = []
                        [req_remain.extend(x) for x in req_list if x != True]

                        return req_remain
                # this needs to account for just the min req for a requirement
                # if I need to count the remaining reqs



def semrev(year_base, currentcredit, creditpersem, creditend):
    '''semester review to count to expected completion semester'''
    semlist = ['01', '05', '07', '08', '12']
    #currentcredit += creditpersem
    year = int(year_base[:4])
    semstart = int(year_base[4:])

    while currentcredit < creditend:
        if semstart % 5 == 1:
        #spring semester
            currentcredit += creditpersem
            semstart += 1
            
        elif semstart % 5 == 2:
            #currentcredit += creditpersem
            semstart += 1
                        
        elif semstart % 5 == 4:
        #fall semester
            currentcredit += creditpersem  
            semstart += 1
        
        elif semstart % 5 == 0:
            semstart += 1
            year += 1
        else:
        #summerI, summerII
            semstart += 1
        yield (str(year)+str(semlist[(semstart%5)-1]), currentcredit)

class SemCal(object):
    '''
    revised semesters in current program 
    input current credits, current semester and min credits to graduate
    returns iterator of remesters remaining
    '''
    def sem_gen(start_y=2015, start_sem='08', duration_y=5):
            years = (x for x in range(start_y, start_y+duration_y))
            sems = ('01','05','07','08','12')
            max_credit = (15, 3, 3, 15, 3)
            start = str(start_y)+start_sem
            for y in years:
                for x in sems:
                    if str(y)+x >= start:
                        yield str(y)+x
    
    def __init__(self, start_y=2015, start_sem='08'):
        
        self.base_sems = self.sem_gen        
        self.start_y = start_y
        self.start_sem = start_sem
        self.end_sem = None
        self.end_y = None
        self.fall = 'fall'
        self.spring = 'spring'
        self.winter = None
        self.summer_1 = None
        self.summer_2 = None
        self.credit_per_sem = 12
        self.current_credits = 0
        self.current_sem = None
        self.sem_num = ('01','05','07','08','12')
        self.sem_max_credit = (15, 3, 3, 15, 3)
        self.term_name = ('spring', 'summer_1', 'summer_2',
                          'fall','winter')
        
    def __repr__(self):
        return str((str(self.start_y), self.start_sem))
        
    
    def sem_gen(self, start_y=2015, start_sem='08', duration_y=5):
        years = (x for x in range(start_y, start_y+duration_y))
        sems = ('01','05','07','08','12')
        max_credit = (15, 3, 3, 15, 3)
        start = str(start_y)+start_sem
        for y in years:
            for x in sems:
                if str(y)+x >= start:
                    yield str(y)+x
           
    def term_filter(self, fall='fall', spring='spring', winter=None, summer_1=None, summer_2=None):
        terms = {'fall':'08','winter':'12', 'spring':'01',
                 'summer_1':'05', 'summer_2':'07'}
        max_credit = {'fall':15,'winter':3, 'spring':15,
                 'summer_1':3, 'summer_2':3}
        include = [x for x in [fall,spring,winter,summer_1, summer_2] if x != None]
        selected = [terms[x] for x in [y for y in include]]
        return [x for x in self.base_sems(self.start_y, self.start_sem) if x[-2:] in selected]
    
    def sem_remain(self, program_min, current_credit, credit_per_sem):
        return ceil((program_min-current_credit)/credit_per_sem)     
    
    def final_term(self, start_y, start_sem, current_credit, program_min, credit_per_sem):
        remaining_sem = int(ceil((program_min-current_credit)/credit_per_sem))
        final = self.term_filter(self.fall, self.spring, self.winter, self.summer_1, self.summer_2)
        return final[:remaining_sem]


 