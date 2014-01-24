#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Test DB for review and development

import sys
#sys.path.append("/media/kenneth/USB DISK/sd_revise_2013_11_22/evaluation")
sys.path.append("../evaluation")
import PUAFdb_perm as db

import sqlite3
import audit_review_class as arc
import audit_dicts as ad
import audit_sql as asql

conn = sqlite3.connect("../evaluation/db/PUAFdb.db")
curs = conn.cursor()

#Test cases
#PPCN
#LMPO
#BMPO
#MAPO
#MANG
#Undergrad and MAPO
#BAMPP

