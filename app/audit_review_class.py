#!/usr/bin/env python
#-*- coding: utf-8 -*-


# A class to contain the UID object and its methods
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
    '''count to expected completion semester'''
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


 