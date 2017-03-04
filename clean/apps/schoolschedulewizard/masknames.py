from misc_utils import os_file_to_list
from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query
import sswizard_utils
from random import random

import sswizard_query_utils

def mask(oldlist,newlist,map,namemap=None):
    if namemap==None:
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
                        print exec_str
                    
    
adultdbloc =dict(adult=['name'],session=['teacher','code'],lesson=['teacher','session'])
studentdbloc =dict(student=['name'],lesson=['student'])
subjectdbloc =dict(subject=['name'],session=['subject','code'],lesson=['subject','session'])
formatsdbloc =dict(formats=['name'])

new_names = os_file_to_list('names.txt',strip=True)
_new_subjects="AnimalScience,Bacteriology,Biology,Botany,Cellular&MolecularBiology,CellularPhysiology,EarthScience,Ecology,Evolution,Genetics,Hematology,Histology,Immunology,Microbiology,NaturalScience,Oceanography,Pathology,PhysicalScience,ZoologyCHEMISTRY:Biochemistry,BioorganicChemistry,Chemistry,InorganicChemistry,MedicalChemistry,OrganicChemistry,PharmaceuticalChemistry,PhysicalChemistry,PhysiologicalChemistry,Structures&Bonds,Composition,English,TechnicalWriting,Algebra,BehavioralStatistics,Biostatistics,Calculus,ChemicalMath,Math,Statistics,Acting,Archeology,ArtHistory,Banking,BibleLiterature,Business,Communication,Dance,Debate,Economics,Education,ESL,Ethics,FirstAid,ForeignLanguage,Geography,Government,History,Humanities,Journalism,Law,Literature,Logic,Management,Marketing,MedicalTerminology,MilitaryScience,Philosophy,PhysicalEducation,Poetry,PoliticalScience,PublicSpeaking,ReadingSkills,Religion,Theater,Theology"
new_subjects = _new_subjects.split(",")

dbname,_ = sswizard_utils.getdatabase()

database = Database(dbname)
with database:
    _,adults,_ = sswizard_query_utils._distinct(database,'name','adult')
    _,students,_ = sswizard_query_utils._distinct(database,'name','student')
    _,subjects,_ = sswizard_query_utils._distinct(database,'name','subject')
    _,formats,_ = sswizard_query_utils._distinct(database,'name','formats')

current_adults = [adult[0] for adult in adults] 
current_students = [student[0] for student in students]
current_subjects = [subject[0] for subject in subjects]
current_formats = [format[0] for format in formats]

current_adults.pop(current_adults.index('A'))
current_adults.pop(current_adults.index('B'))
current_adults.pop(current_adults.index('C'))
current_adults.pop(current_adults.index('D'))

mask(current_adults ,new_names,adultdbloc)
mask(current_students ,new_names,studentdbloc)
mask(current_subjects ,new_subjects,subjectdbloc)

usednamemap = {u'Paraic': 'Vilma', u'SONJA': 'Deana', u'Aaron': 'Eulah', 
           u'Melissa': 'Carlene', u'Alberto': 'Johnetta', u'John': 'Ginger', 
           u'Daryl': 'Tara', u'Alexa': 'Jude', u'Karolina': 'Vonda', 
           u'Samantha': 'Shaunna', u'Thea': 'Norberto', u'Issey': 'Vinnie', 
           u'Stan': 'Tara', u'Amelia': 'Arlean', u'Rahul': 'Cary', u'??': 'Thersa', 
           u'Dylan': 'Eleonora', u'Moira': 'Jamila', u'John Zink': 'Lynna', 
           u'Patti': 'Drucilla', u'Francisco': 'Janey', u'Alyssa': 'Ezequiel', 
           u'Sam': 'Divina', u'Johnny': 'Clinton', u'Galina': 'Norberto', 
           u'Jess': 'Jude', u'Izzy': 'Drucilla', u'Bari': 'Zonia', u'Jacki': 'Joette', 
           u'Eric': 'Lynna', u'Nicole': 'Cleotilde', u'Profeshor': 'Natasha',
           u'Yosef': 'Kaycee', u'Coby': 'Becki', u'OmerC': 'Iola', u'Bruno': 'Tien', 
           u'Stephen': 'Ezequiel', u'Nathaniel': 'Trish', u'Jake': 'Hillary', 
           u'Tristan': 'Vonda', u'Shane': 'Divina', u'Oscar': 'Hillary', 
           u'Clayton': 'Debbra', u'Jack': 'Lauralee', u'Ashley': 'Donny', 
           u'Lucy': 'Vilma', u'Asher': 'Colleen', u'Donovan': 'Madie', 
           u'Simon B': 'Lynna', u'Booker': 'Natasha', u'Simon A': 'Kira', 
           u'Thomas': 'Joya', u'Liam': 'Kisha', u'Nick': 'Carlene', 
           u'Mackenzie': 'Ezequiel', u'Prep 4':'Ike', u'Luke': 'Daysi', 
           u'Peter': 'Thersa', u'Tris': 'Dorcas', u'Orig': 'Vonda', 
           u'Psychology': 'Calculus', u'Humanities': 'ESL', u'Activity Period': 'Literature', 
           u'STEM': 'ForeignLanguage', u'Music': 'CellularPhysiology', 
           u'Chess': 'PharmaceuticalChemistry', u'Piano': 'Dance', 
           u'Reading': 'MedicalChemistry', u'Psychology Reading': 'History', 
           u'Math': 'Poetry', u'Movement': 'Composition', u'Core': 'Evolution', 
           u'Biology': 'Marketing', u'Track': 'FirstAid', u'Independent Reading': 'PhysicalScience', 
           u'Italian': 'Cellular&MolecularBiology', u'Game Period': 'PhysiologicalChemistry', 
           u'??': 'Immunology', u'Computer Time': 'Poetry', u'Science': 'Composition', 
           u'ELA': 'English', u'Supervision': 'ChemicalMath', u'Drama':'Government', 
           u'Quad Cafe': 'ReadingSkills', u'Independent Art': 'Law',  u'Counseling': 'Math', 
           u'Math Activity Period': 'Math', u'Work Period': 'BehavioralStatistics', 
           u'Mentorship': 'ChemicalMath', u'History': 'MedicalChemistry', u'Art': 'Calculus', 
           u'Engineering': 'Economics', u'Spanish': 'PharmaceuticalChemistry', 
           u'Speech': 'Biostatistics', u'Student News': 'Marketing', u'OT': 'Marketing', 
           u'Debate': 'Oceanography'}

mask(current_formats ,new_names,formatsdbloc,namemap=usednamemap)
