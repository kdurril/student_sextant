# -*- coding: utf-8 -*-
#http://www.evanjones.ca/python-utf8.html

#Web Driver for Student Specialization Evaluation
# extract student's courses from MEGS
# convert courses to list
# evaluate list with Specialization eval tools

#non standard library imports
from selenium import webdriver

#standard library imports
import time
import csv
import re
import codecs
from datetime import date
from os import path, mkdir



def create_path(sem, dept="PUAF"):
    '''create path text for new files'''
    #format today's date year month day
    today_folder = date.today()
    today_folder = today_folder.strftime("%Y_%m_%d")
    today_sem = sem
    today_sem = "_"+today_sem+"_"+dept
    today_dir = "../evaluation/courseplan/"+today_folder+today_sem

    return today_dir

def make_path(today_dir):
    if not path.isdir(today_dir):
        mkdir(today_dir)

catalog_dir = "../evaluation/courseplan/"

#Select browser
driver = webdriver.Firefox()

def get_catalog(sem):
    "extract the catalog departments"
    driver.get('https://ntst.umd.edu/soc/'+sem)

    time.sleep(2)

    dept_base = driver.find_elements_by_xpath('//div[@class="course-prefix row"]') #use this selector for main page that list top level dept
    #Get all of the department names and abbreviations
    dept_text = [x.text.split("\n") for x in dept_base]
    return dept_text

def dept_get(sem, dept):
    "get page information by semester and department, pull dept from dept_text"
    
    #today_dir = create_path(sem, dept="PUAF")
    #make_path(today_dir) #create the folder

    driver.get("https://ntst.umd.edu/soc/"+sem+"/"+dept)
    time.sleep(5)
    #Department page
    sect_link = driver.find_elements_by_xpath('//a[@class="toggle-sections-link"]')

    #Open all sections
    [x.click() for x in sect_link]
    time.sleep(2)

    #Select all course containers
    course_box = driver.find_elements_by_xpath('//div[@class="course"]')
    
    for course in course_box:
        course_number = course.find_element_by_xpath(
            'descendant::div[@class="course-id"]').text
        course_title = course.find_element_by_xpath(
            'descendant::span[@class="course-title"]').text
        #course_description = course.find_element_by_xpath(
        #    'descendant::div[@class="approved-course-texts-container"]').text
        course_credit = course.find_element_by_xpath(
            'descendant::span[@class="course-min-credits"]').text
        course_grademethod = course.find_element_by_xpath(
            'descendant::span[@class="grading-method"]').text

        course_main = [sem, course_number, course_title, course_credit, course_grademethod]      

        with codecs.open("../evaluation/courseplan/courses.csv", "a+", "utf-8") as g:
            course_write = csv.writer(g, delimiter="\t", 
                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            course_write.writerow(course_main)

        #Section Extraction Below:
        section_row = course.find_elements_by_xpath(
            'descendant::div[@class="section"]')

        for row in section_row:

            row_text = row.text.split("\n")

            def row_parse(text):
                cap = re.compile("Total: (\d{,3}), Open: (\d{,3}), Waitlist: (\d{,3})")
                cap = cap.search(text)
                cap = [cap.group(1), cap.group(2), cap.group(3)]
                return cap

            def daytime_parse(text):
                cap = re.compile('\w{,4}')
                cap = cap.search(text)
                cap = cap.group(0)
                if 'Contact' in text or ":" not in text[:7]:
                    return [text]
                else:
                    cap2 = re.compile('\d.+m')
                    cap2 = cap2.search(text)
                    cap2 = cap2.group(0).split("-")
                    return [cap, cap2[0].strip(" "), cap2[1].strip(" ")]
            
                                  
            section = list()
            section.append(sem)
            section.append(course_number)
            section.extend(row_text[:2])
            section.extend(row_parse(row_text[2]))
            section.extend(daytime_parse(row_text[3]))
            if len(row_text) <= 5:
                section.extend(row_text[4:])
            else:
                section.append(row_text[4])
                section.extend(daytime_parse(row_text[5]))
                section.extend(row_text[6:])

            with codecs.open("../evaluation/courseplan/sections.csv", "a+", "utf-8") as f:
                section_write = csv.writer(f, delimiter="\t",
                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                section_write.writerow(section)
        

def get_all(sem):
    for x in get_catalog(sem):
        dept_get(sem, x[0])
    driver.close()

def get_some(sem, start):
    dept_list = get_catalog(sem) 
    for x in dept_list[start:]:
        dept_get(sem, x[0])
    driver.close()


#get_all("201401")
get_some("201401", 49)
#dept_get("201401", "COMM")
#driver.close()