#!/usr/bin/env python
#-*- coding: utf-8 -*-

## Program requirements for each program and each specialization
## Programs include: BMPO, LMPO, MAMG, MAPO, MEPP, POSI, PPCN


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
         "waiver": ['PUAF689B']}
Macro_fin = {"Course": ['PUAF641', 'PUAF670'], "MinReq": 1,\
             "label": 'MacroEcon/Finance'}
Macro = {"Course": ['PUAF641'], "MinReq": 1, "label": 'MacroEcon'}
Fin = {"Course": ['PUAF641', 'PUAF670'], "MinReq": 1, "label": 'Finance'}
Poly = {"Course": ['PUAF620', 'PUAF688A'], "MinReq": 1,\
          "label": 'Political, Ethical and Management Analysis'}
Ethics = {"Course": ['PUAF650'], "MinReq": 1,\
          "label": 'Political, Ethical and Management Analysis'}
Mngt = {"Course": ['PUAF711'], "MinReq": 1,\
          "label": 'Political, Ethical and Management Analysis'}
Project = {"Course": ['PUAF790'], "MinReq": 1,\
           "label": 'Project Course'}

CORE = [Stats, Micro, Macro, Ethics, Poly, Mngt]
CORE_MFL = [Stats, Micro, Fin, Ethics, Poly, Mngt]
CORE_ISEP = [Stats, Micro, Macro, Ethics, Poly, Mngt]


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

ENV = [Stats, Micro, Macro_fin, Ethics, Poly, Mngt, ENV_1, ENV_Project]

## Energy Policy
ERG_1 = {"Course": ['PUAF699'], "MinReq": 1, "label": "Energy Policy 1"}
ERG_2 = {"Course": ['PUAF798N', 'PUAF798O', 'PUAF798K'], "MinReq": 1,\
         "label": "Energy Policy 2"}

ENGY = [Stats, Micro, Macro_fin, Ethics, Poly, Mngt, ENV_1, ERG_1, ERG_2, ENV_Project]

##International Development
#Components
IDEV_1 = {"Course": ['PUAF698R','PUAF699J'],
          "MinReq": 1, "label": "IDEV Req 1"}
IDEV_2 = {"Course": ['PUAF781', 'PUAF782'], 
          "MinReq": 2, "label": "IDEV Req 2"}
IDEV_3 = {"Course": ['PUAF611', 'PUAF699K','PUAF720', 'PUAF698O', 'PUAF699D',\
                  'PUAF699K', 'PUAF699Q', 'PUAF798C', 'PUAF798E',
                  'PUAF698I', 'PUAF798T'], "MinReq": 1, "label": "IDEV Req 3"}


IDEV = [Stats, Micro, Macro, Ethics, Poly, Mngt, IDEV_1, IDEV_2, Project]


##International Security and Economic Policy
#Components
ISEP_1 = {"Course":['PUAF720','PUAF780', 'PUAF781'], "MinReq": 3,\
          "label": "ISEP Req 1"}

ISEP = [Stats, Micro, Macro, Ethics, Poly, Mngt, ISEP_1, Project]

##Management, Leadership and Finance
#Leadership and Management Components
LM_1 =  {"Course": ['PUAF698P', 'PUAF798Y', 'PUAF689Y', 'PUAF689Z'],\
         "MinReq": 2, "label": "LM Req 1"}
LM_2 = {"Course": ['PUAF752', 'PUAF753'], "MinReq": 1, "label": "LM Req 2"}

LM = [Stats, Micro, Fin, Ethics, Poly, Mngt, LM_1, LM_2, Project]

ML = LM #alias because of MEGS specialization name

#Public Sector Financial Management Components
PSFM_1 = {"Course": ['PUAF699E', 'PUAF712','PUAF716','PUAF717'], "MinReq": 3,\
          "label": "PSFM Req 1"} 
PSFM_2 = {"Course": ['PUAF698P', 'PUAF699C','PUAF752','PUAF753'], "MinReq": 1,\
          "label": "PSFM Req 2"}

PSFM = [Stats, Micro, Fin, Ethics, Poly, Mngt, PSFM_1, PSFM_2, Project]

# Acquisitions Management
ACQ_1 = {"Course": ['PUAF689A', 'PUAF698G', 'PUAF689F'], "MinReq": 3,\
         "label": "ACQ Req 1"}

ACQ = [Stats, Micro, Fin, Ethics, Poly, Mngt, ACQ_1, Project]

FAM = ACQ #alias because of MEGS specialization name


# Nonprofit Management Focus, must be completed in addition to another specialization
NML_1 = {"Course": [ 'PUAF798Y'], "MinReq": 1, "label": "NPM Req 1"}
NML_2 = {"Course": [ 'PUAF689Y', 'PUAF689Z'], "MinReq": 2, "label": "NPM Req 2"} 
#This will be the nonprofit management finance course
NML_3 = {"Course": [ 'PUAF689L'], "MinReq": 1, "label": "NPM Req 3"} 

NML = [Stats, Micro, Fin, Ethics, Poly, Mngt, NML_1, NML_2, NML_3, Project]

#Social Policy
#Soc
Soc_1 = {"Course": ["PUAF611", 'PUAF734', 'PUAF689E'], "MinReq": 3, "label": "Soc Req"}

#Health
Health_1 = {"Course": ['PUAF698G','PUAF698K', 'PUAF699D'], "MinReq": 1, "label": "Health_1 Req"}
Health_2 = {"Course": ['PUAF735'], "MinReq": 1, "label": "Health_2 Req"}

#EDUC
Educ_1 = {"Course": ['PUAF732', 'EDPL615'], "MinReq": 2, "label": "Edu Req"}

SOC = [Stats, Micro, Macro_fin, Ethics, Poly, Mngt, Soc_1, Project]
HLTH = [Stats, Micro, Macro_fin, Ethics, Poly, Mngt, Soc_1, Health_1, Health_2, Project]
EDUC = [Stats, Micro, Macro_fin, Ethics, Poly, Mngt, Soc_1, Educ_1, Project]

OTH = [Stats, Micro, Macro_fin, Ethics]

MAPO = [Stats, Micro, Macro_fin, Ethics]

LMPO = [Stats, Micro, Macro_fin, Ethics]

All = [ENV, ENGY, IDEV, ISEP, LM, PSFM, ACQ, NML, SOC, EDUC, HLTH]
All_label = ['ENV', 'ENGY', 'IDEV', 'ISEP', 'LM', 'PSFM', 'ACQ', 'NPM', 'SOC', 'EDUC', 'HLTH']

#Use All_dict as a lookup table to place the specialization objects for specialization strings
All_dict = {'ENV': ENV, 'ENGY': ENGY, 'IDEV': IDEV, 'ISEP': ISEP, 
            'LM': LM, 'PSFM': PSFM, 'ACQ': ACQ, 'NML': NML, 'SOC': SOC,
            'EDUC': EDUC, 'HLTH': HLTH, 'OTH': OTH, 'ML': ML, "LMPO": LMPO, "MAPO": MAPO}


#MEPP
mepp_1 = {"Course":['PUAF740', 'PUAF741', 'PUAF745'], "MinReq": 3,\
         "label": "ENV Req 1"}
mepp_polanlysis = {"Course": ['PUAF620', 'PUAF688A'], "MinReq": 1,\
          "label": 'Political, Ethical and Management Analysis'}
mepp_ethics = {"Course": ['PUAF620', 'PUAF650', 'PUAF711', 'PUAF688A'], "MinReq": 3,\
          "label": 'Political, Ethical and Management Analysis'}
mepp_project = {"Course": ['PUAF790'], "MinReq": 1,\
           "label": 'Project Course'}


## Check for fulfillments
## useful if partial set required to meet requirement

## Check fulfillment with dictionary

def req_diff(req_list1, req_list2):
    '''set difference from requirement 1 to requirement 2'''
    return [x for x in req_list1 if x not in req_list2]

def req_intersection(req_list1, req_list2):
    '''set intersection for requirement 1 and requirement 2'''
    return [x for x in req_list1 if x in req_list2]

def req_semdiff(req_list1, req_list2):
    '''semetric difference from req_list1 to req_list2'''
    diff = req_diff(req_list1, req_list2)
    intersection = req_intersection(req_list1, req_list2)
    diff.extend(intersection)
    return diff