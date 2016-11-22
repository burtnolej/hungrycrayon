from misc_utils import os_file_to_list
from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

from random import random

import sswizard_query_utils

def mask(oldlist,newlist,map):
    namemap={}
    for i in range(len(oldlist)):
        namemap[oldlist[i]] = newlist[int(random()*len(newlist))]
    
    with database:

        for tablename,colnames in map.iteritems():        
            for colname in colnames:            
                for oldname,newname in namemap.iteritems():
                
                    exec_str = " select __id,{0} ".format(colname)
                    exec_str += " from {0} ".format(tablename)
                    exec_str += " where {0} like \"%{1}%\"".format(colname,oldname)
                
                    _,results,_ = tbl_query(database,exec_str)
                    
                    for row in results:
                        __id = row[0]
                        _old = row[1]
                        _new = _old.replace(oldname,newname)
                        
                        exec_str = " update {0} ".format(tablename)
                        exec_str += " set {0} = \"{1}\"".format(colname,_new)
                        exec_str += " where __id = \"{0}\"".format(__id)
                        
                        tbl_query(database,exec_str)
                        #print exec_str
                    
    
adultdbloc =dict(adult=['name'],session=['teacher','code'],lesson=['teacher','session'])
studentdbloc =dict(student=['name'],lesson=['student'])
subjectdbloc =dict(subject=['name'],session=['subject','code'],lesson=['subject','session'])

new_names = os_file_to_list('names.txt',strip=True)
_new_subjects="AnimalScience,Bacteriology,Biology,Botany,Cellular&MolecularBiology,CellularPhysiology,EarthScience,Ecology,Evolution,Genetics,Hematology,Histology,Immunology,Microbiology,NaturalScience,Oceanography,Pathology,PhysicalScience,ZoologyCHEMISTRY:Biochemistry,BioorganicChemistry,Chemistry,InorganicChemistry,MedicalChemistry,OrganicChemistry,PharmaceuticalChemistry,PhysicalChemistry,PhysiologicalChemistry,Structures&Bonds,Composition,English,TechnicalWriting,Algebra,BehavioralStatistics,Biostatistics,Calculus,ChemicalMath,Math,Statistics,Acting,Archeology,ArtHistory,Banking,BibleLiterature,Business,Communication,Dance,Debate,Economics,Education,ESL,Ethics,FirstAid,ForeignLanguage,Geography,Government,History,Humanities,Journalism,Law,Literature,Logic,Management,Marketing,MedicalTerminology,MilitaryScience,Philosophy,PhysicalEducation,Poetry,PoliticalScience,PublicSpeaking,ReadingSkills,Religion,Theater,Theology"
new_subjects = _new_subjects.split(",")

dbname="quad"

database = Database(dbname)
with database:
    _,adults,_ = sswizard_query_utils._distinct(database,'name','adult')
    _,students,_ = sswizard_query_utils._distinct(database,'name','student')
    _,subjects,_ = sswizard_query_utils._distinct(database,'name','subject')

current_adults = [adult[0] for adult in adults] 
current_students = [student[0] for student in students]
current_subjects = [subject[0] for subject in subjects]

current_adults.pop(current_adults.index('A'))
current_adults.pop(current_adults.index('B'))
current_adults.pop(current_adults.index('C'))
current_adults.pop(current_adults.index('D'))

mask(current_adults ,new_names,adultdbloc)
mask(current_students ,new_names,studentdbloc)
mask(current_subjects ,new_subjects,subjectdbloc)