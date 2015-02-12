#Audit
# -*- coding: utf-8 -*-
#SQL based revision to requirements audit
#SQL is set based and so are audit rules, so use the standard 

from itertools import chain

#Requirements base is the traditional format for specializations
requirement_base = '''SELECT student.UID
FROM requirements INNER JOIN student ON requirements.course_num = student.Class
WHERE requirements.Specialization = ? AND requirements.Requirement_type = ? 
GROUP BY student.UID
HAVING Count(student.Class) = ? '''

#PSFM requires at least 1 from req 2 and at least 1 from req 4
#the count from both req 2 and req 4 must be at least 3 
requirement_psfm = '''SELECT student.UID
FROM requirements INNER JOIN student ON requirements.course_num = student.Class
WHERE requirements.Specialization = ? AND requirements.Requirement_type = ?
GROUP BY student.UID
HAVING Count(student.Class) >= ? '''

#Extra input for student id
#Create a list for with the student id e.g. [112444222]
#then extend the requirement to list
#Requirements base is the traditional format for specializations
requirement_base_std = '''SELECT student.UID
FROM requirements INNER JOIN student ON requirements.course_num = student.Class
WHERE student.UID = ? AND requirements.Specialization = ? AND requirements.Requirement_type = ?
GROUP BY student.UID
HAVING Count(student.Class) = ? '''

#PSFM requires at least 1 from req 2 and at least 1 from req 4
#the count from both req 2 and req 4 must be at least 3 
requirement_psfm_std = '''SELECT student.UID
FROM requirements INNER JOIN student ON requirements.course_num = student.Class
WHERE student.UID = ? requirements.Specialization = ? AND requirements.Requirement_type = ?
GROUP BY student.UID
HAVING Count(student.Class) >= ? '''

#Compound queries for linking program elements
qry_one = requirement_base
qry_two = 'SELECT a.UID FROM ( ' + requirement_base +\
          ' ) as a INNER JOIN (' + requirement_base +\
          ' ) as b ON a.UID = b.UID GROUP BY a.UID'

qry_three = 'SELECT c.UID FROM (' + qry_two +\
          ') as c INNER JOIN ( ' + requirement_base +\
          ') as d ON c.UID = d.UID GROUP BY c.UID'

qry_four = 'SELECT e.UID FROM (' + qry_three +\
          ') as e INNER JOIN ( ' + requirement_base +\
          ') as f ON e.UID = f.UID GROUP BY e.UID'

qry_five = 'SELECT g.UID FROM (' + qry_four +\
          ') as g INNER JOIN ( ' + requirement_base +\
          ') as h ON g.UID = h.UID GROUP BY g.UID'

#Compound queires for with UID attribute for student
qry_two_std = 'SELECT a.UID FROM ( ' + requirement_base_std +\
          ' ) as a INNER JOIN (' + requirement_base_std +\
          ' ) as b ON a.UID = b.UID GROUP BY a.UID'

qry_three_std = 'SELECT c.UID FROM (( ' + requirement_base_std +\
        ' ) as a INNER JOIN (' + requirement_base_std +\
        ' ) as b ON a.UID = b.UID) as c INNER JOIN ( '+\
          requirement_base_std +\
        ') as d ON c.UID = d.UID GROUP BY c.UID'

def attr_build(*reqs):
    "build list of multiple requirements"
    qry_args =[]
    for req in reqs:
        qry_args.extend(req)
    return qry_args

def attr_build_std(uid, *reqs):
    "this function builds list for queries by student"
    qry_args =[]
    for req in reqs:
        qry_args.append(uid)
        qry_args.extend(req)
    return qry_args

def db_to_set(db_tuples):
    'create set from returned db tuples'
    'db_tuples should be single column vector'
    if len(db_tuples[0][0]) > 1:
        return db_tuples
    else:
        return [{y for y in chain.from_iterable(x)} for x in db_tuples]
    return db_tuples

#adust for cursor name
def multi_fetch(*args):
    'add all requirements from a specialization, or multiple specializations'
    reqs = [curs.execute(requirement_base, req).fetchall() for req in [x for x in args]]
    return reqs
def qry_multi_base(qry_base, count):
    "base query builder"
    alpha = [ltr for ltr in 'abcedfghijklmnop']
    for y in range(count):
        qry_new = 'SELECT '+alpha[y]+'.UID FROM ( ' + qry_base +\
          ' ) as '+alpha[y]+' INNER JOIN (' + qry_base +\
          ' ) as '+alpha[y +1]+' ON '+alpha[y]+'.UID = '+\
          alpha[y +1]+'.UID GROUP BY '+alpha[y]+'.UID'
    return qry_new

def multi(qry_base, count):
    "recursive query builder"
    alpha = [ltr for ltr in 'abcdefghijklmnop']
    for y in range(count):
        if count <= 1:
            y = 1
            qry_new = 'SELECT '+alpha[y]+'.UID FROM ( ' + qry_base +\
              ' ) as '+alpha[y]+' INNER JOIN (' + qry_base +\
              ' ) as '+alpha[y +1]+' ON '+alpha[y]+'.UID = '+\
              alpha[y +1]+'.UID GROUP BY '+alpha[y]+'.UID'
            return qry_new
        else:
            qry_new = 'SELECT '+alpha[y]+'.UID FROM ( ' + qry_base +\
              ' ) as '+alpha[y]+' INNER JOIN (' + qry_base +\
              ' ) as '+alpha[y +1]+' ON '+alpha[y]+'.UID = '+\
              alpha[y +1]+'.UID GROUP BY '+alpha[y]+'.UID'
            return multi(qry_new, count-2)

#requirements
#structure = (specialization, requirement, count)
#review requirements table for full listing of courses
qry_env_1 = ("ENV", 1, 6)
qry_env_2 = ("ENV", 2, 3)
qry_env_3 = ("ENV", 3, 1)
qry_env_4 = ("ENV", 4, 1)
reqs_env = [qry_env_1, qry_env_2, qry_env_3, qry_env_4]

qry_engy_2 = ("ENGY", 4, 2)
reqs_engy = [qry_env_1, qry_engy_2, qry_env_2, qry_env_3, qry_env_4]

qry_isep_1 = ("ISEP", 1, 6)
qry_isep_2 = ("ISEP", 2, 3)
qry_isep_3 = ("ISEP", 3, 1)
qry_isep_4 = ("ISEP", 4, 1)
reqs_isep = [qry_isep_1, qry_isep_2, qry_isep_3, qry_isep_4]

qry_idev_1 = ("IDEV", 1, 6)
qry_idev_2 = ("IDEV", 2, 3)
qry_idev_3 = ("IDEV", 3, 3)
qry_idev_4 = ("IDEV", 4, 1)
reqs_idev = [qry_idev_1, qry_idev_2, qry_idev_3, qry_idev_4]

qry_soc_1 = ("SOC", 1, 6)
qry_soc_2 = ("SOC", 2, 3)
qry_soc_3 = ("SOC", 3, 1)
qry_soc_4 = ("SOC", 4, 1)
reqs_soc = [qry_soc_1, qry_soc_2, qry_soc_3, qry_soc_4]

qry_educ_2 = ("EDU", 4, 2)
reqs_educ = [qry_soc_1, qry_soc_2, qry_soc_3, qry_soc_4, qry_educ_2]


qry_hlth_2 = ("HLTH", 4, 1)
qry_hlth_4 = ("HLTH", 5, 1)
reqs_hlth = [qry_soc_1, qry_soc_2, qry_soc_3, 
             qry_soc_4, qry_hlth_2, qry_hlth_4]

qry_ml_1  = ("ML", 1, 6)
qry_ml_2  = ("ML", 2, 2)
qry_ml_3  = ("ML", 3, 1)
qry_ml_4  = ("ML", 4, 1)
qry_ml_5  = ("ML", 5, 1)
reqs_ml = [qry_ml_1, qry_ml_2, qry_ml_3, qry_ml_4, qry_ml_5]

qry_nml_1  = ("NML", 1, 6)
qry_nml_2  = ("NML", 2, 2)
qry_nml_3  = ("NML", 3, 1)
qry_nml_4  = ("NML", 4, 2)
reqs_nml = [qry_nml_1, qry_nml_2, qry_nml_3, qry_nml_4]


qry_fam_1  = ("FAM", 1, 6)
qry_fam_2  = ("FAM", 2, 3)
qry_fam_3  = ("FAM", 3, 1)
qry_fam_4  = ("FAM", 4, 1)
reqs_fam = [qry_fam_1, qry_fam_2, qry_fam_3, qry_fam_4]

qry_psfm_1 = ("PSFM", 1, 6)
qry_psfm_2 = ("PSFM", 2, 1)
qry_psfm_3 = ("PSFM", 3, 1)
qry_psfm_4 = ("PSFM", 4, 1)
qry_psfm_5 = ("PSFM", 5, 1)
reqs_psfm = [qry_psfm_1, qry_psfm_2, qry_psfm_3, qry_psfm_4, qry_psfm_5]

lookup = {"EDUC": reqs_educ, "ENV": reqs_env, "ENGY": reqs_engy, 
          "FAM": reqs_fam, "HLTH":reqs_hlth, "ISEP": reqs_isep, 
          "IDEV": reqs_idev,"ML":reqs_ml, "NML": reqs_nml,
          "PSFM": reqs_psfm, "SOC":reqs_soc} 