# ------------------------------------ 
# Functions related to number / numerics
# Modified : 2020, July 31 
# ------------------------------------

import re 
#from utils import file_to_str
import sirex.utils as utils
#from .utils import * 

def word_count(fname):
    '''

    Returns the number of words in the file 
    Usage : 
    sirex.word_count('f.txt')  
    Returns : int
    
    '''
    all_str = utils.file_to_str(fname)
    return len(re.findall("\S+",all_str))

def line_count(fname ):
    '''
    Returns the number of lines in the file 
    sirex.line_count('f.txt')  
    Returns : int
    '''
    all_str = file_to_str(fname,singleline=False)
    return  len(re.findall('\n',all_str)) + 1 



def occurance_file(str_, fname,case_sensitive = False):
    all_str = file_to_str(fname,convert_lower_case=not case_sensitive)
    if not case_sensitive:
        all_str = all_str.lower()
        str_ = str_.lower()
    
    return len(re.findall(str_,all_str))



def biggest_number_in_file(file_path) :
    '''
    Finds the biggest integer number mentioned in a text document
    Returns : 
    int ( if the there is a number in the file )
    None ( if there is no number in the file)
    '''
    biggest_num = biggest_number(file_to_str(file_path))
    
    return biggest_num    