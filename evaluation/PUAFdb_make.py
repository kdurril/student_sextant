#! /usr/bin/env python
#-*- coding: utf-8 -*-
import csv

#sqlite3 db from student records


def valuegen(x):
	p = ''
	for y in x:
		p += "?,"
	p = '('+p[:len(p)-1]+');'
	return p

def copyfrom():
      with open("../evaluation/db/directory_tab.csv", "r+") as infile:
            dr = csv.DictReader(infile, delimiter = ',')
            newoutfile = open("../evaluation/db/newoutfile.txt", "a")

            newoutfile.write('''to_db = "[(''')
            for field in dr.fieldnames:
                  newoutfile.write("i['{0}'], ".format(field))
            newoutfile.write(''') for i in dr]\n" ''')

            newoutfile.write(str(dr.fieldnames))
            newoutfile.write(") VALUES (")
            newoutfile.write(valuegen(dr.fieldnames))
            newoutfile.write(");")
            newoutfile.write("\n")

            




if __name__ == "__main__":
    sys.exit(main())


#Foot notes
#http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
