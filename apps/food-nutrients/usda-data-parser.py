# Field Name  Type  Blank Description
# --------------------------------------------------------------
# NDB_No      A 5*  N 5-digit Nutrient Databank number that uniquely identifies a food item. 
#                     If this field is defined as numeric, the leading zero will be lost.
#
# FdGrp_Cd    A 4   N 4-digit code indicating food group to which a food item belongs.
#
# Long_Desc   A 200 N 200-character description of food item.
#
# Shrt_Desc   A 60  N 60-character abbreviated description of food item. Generated from the 
#                     200-character description using abbreviations in Appendix A. If short 
#                     description is longer than 60 characters, additional abbreviations are made.
#
# ComName     A 100 Y Other names commonly used to describe a food, including local or regional 
#                     names for various foods, for example, “soda” or “pop” for “carbonated beverages.”
#
# ManufacName A 65  Y Indicates the company that manufactured the product, when appropriate.
#
# Survey      A 1   Y Indicates if the food item is used in the USDA Food and Nutrient Database 
#                     for Dietary Studies (FNDDS) and thus has a complete nutrient profile for 
#                     the 65 FNDDS nutrients.
#
# Ref_desc    A 135 Y Description of inedible parts of a food item (refuse) such as seeds or bone.
#
# Refuse      N 2   Y Percentage of refuse.
#
# SciName     A 65  Y Scientific name of the food item. Given for the least processed form of 
#                     the food (usually raw), if applicable.
#
# N_Factor    N 4.2 Y Factor for converting nitrogen to protein (see p. 12).
#
# Pro_Factor  N 4.2 Y Factor for calculating calories from protein (see p.14).
#
# Fat_Factor  N 4.2 Y Factor for calculating calories from fat (see p. 14).
#
# CHO_Factor  N 4.2 Y Factor for calculating calories from carbohydrate(see p. 14).


from sys import path,stdout
path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import read_delim_text_from_file
from os import curdir
from os import path as ospath


DATADIR = ospath.join(curdir,"food-data")
FOOD_DES_FILE = ospath.join(DATADIR,"FOOD_DES.txt")

data = read_delim_text_from_file(FOOD_DES_FILE,"^")


field_enum = [
               {field:"NDB_No",     datatype:,nullable:},
               {field:"FdGrp_Cd",   datatype:,nullable:},
               {field:"Long_Desc",  datatype:,nullable:},
               {field:"Shrt_Desc",  datatype:,nullable:},
               {field:"ComName",    datatype:,nullable:},
               {field:"ManufacName",datatype:,nullable:},
               {field:"Survey",     datatype:,nullable:},
               {field:"Ref_desc",   datatype:,nullable:},
               {field:"Refuse",     datatype:,nullable:},
               {field:"SciName",    datatype:,nullable:},
               {field:"N_Factor",   datatype:,nullable:},
               {field:"Pro_Factor", datatype:"N4.2",nullable:"Y"}, 
               {field:"Fat_Factor", datatype:"N4.2",nullable:"Y"},
               {field:"CHO_Factor", datatype:"N4.2",nullable:"Y"}]

print len(data)