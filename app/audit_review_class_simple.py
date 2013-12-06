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
                '''evaluate whether a requirement is complete'''
                '''the intersection of the requirement and the student's courses'''
                
                complete = set(requirement["Course"]).intersection(self)
                if len(complete) >= requirement['MinReq']:
                        return True
                else:
                        return False

        def completeness(self, requirement):
                '''return count of completed courses or complete'''
                complete = set(requirement["Course"]).intersection(self)
                if len(complete) >= requirement['MinReq']:
                        return ['{0} is complete'.format(requirement['label'])]
                else:
                        return ['{0} of {0} complete'.format(len(complete), requirement['MinReq'])]

                
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