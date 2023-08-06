# ------------------------------------ 
# 			string/text Related Functions 
# ------------------------------------


import re 



def count_occurance(sub,parent,case_sensitive = False):
    '''
    Counts the occurance of a sub-string in a parent string
    Usage : sirex.count_occurance('He', 'Hello there' , True) # Searches for h and H
    Returns : int
    '''
    pattern  = sub
    if not case_sensitive:
        pattern = "(?i)"+sub
    count = len((re.findall(pattern,parent)))            
    return count 

