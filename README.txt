To run: launch runserver.py from the app folder

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
## Objective funtion: finish by Fall 2014
## Constraints: Complete IDEV and ISEP
## Changing variables: Semester, general elective courses

## Testing
## A course audit needs a test for each program case
## this includes the standard programs MAPO, MPM, MEPP, POSI etc
## 
## as well as those who have been
## in multiple programs at UMD (which includes those who have been undergrads).
## count of secondary or degree is 2 or greater
## POSI, masters and non-PUAF masters
## undergrad and masters
## BAMPP
## BAMPP and other masters program
## MPP who left program
## MPP traditional first year
## MPP with a waiver of continuous registration and part time
## MPM with spring start
