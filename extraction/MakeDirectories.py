from os import mkdir
import csv


def mk_std():
    '''create folders for current students'''
    directory = open("../evaluation/db/directory_tab.csv", "r+b")
    dReader = csv.DictReader(directory)
    mydict = [x for x in dReader]

    for line in mydict:
        dir_str = "{0}, {1} {2}".format(line['Last_name'], line['first_name'], line['UID'])
        mkdir(dir_str)


#def mk_course_dir():
#    '''create folders for current students'''
#    directory = open("../evaluation/db/Query1.csv", "r+b")
#    dReader = csv.DictReader(directory)
#    mydict = [x for x in dReader]

#    for line in mydict:
#        new_dir = [v for (k,v) in line.iteritems() if k in {'Last_name', 'first_name', 'UID'}]
#        dir_str = "{0}, {1} {2}".format(new_dir[0], new_dir[1], new_dir[2])
#        mkdir(dir_str)
