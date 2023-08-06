# ------------------------------------ 
# 			File Related Functions 
# ------------------------------------

print("utils initialized")

def file_to_str(fpath,singleline=True,convert_lower_case = False) : 
    '''
    
    Reads a file and converts all the text into one string 
    arg ( singleline)  - convert everything to one single line, strips newline and carriage feeds
    
    Usage : sirex.file_to_str('f.txt')  
    Returns : str

    '''
    with open(fpath) as f:
        if singleline :  
            all_str =  " ".join(line.strip() for line in f)  
        else : 
            all_str =  " ".join(line  for line in f)  
        if convert_lower_case :
            all_str = all_str.lower()
    return all_str
