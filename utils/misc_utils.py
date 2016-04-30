def write_text_to_file(filename,text):
    fh = open(filename,'w+')
    fh.write(text)
    fh.close
    
def file_exists(filename):
    from os.path import exists
    
    if exists(filename):
        return(True)
    else:
        return(False)
     
def read_text_from_file(filename):
    '''returns a list of strings'''
    l=[]
    fh = open(filename, 'r+')
    return [line.rstrip() for line in fh]

def file2string(filename):
    '''returns a string'''
    s=""
    fh = open(filename, 'r+')
    
    for line in fh:
        s+=line
    return s

def read_delim_text_from_file(filename,delim):
    'returns a list of lists'
    l=[]
    fh = open(filename, 'r+')
    
    #for line in fh:
    #    l.append(line.rstrip().split(delim))
    #        
    #return l

    return [l.append(line.rstrip().split(delim)) for line in fh]

def print_dict_of_dict(d):
    ''' takes a dict of dicts an input like :
    
    {'abc': {'a': 1, 'c': 3, 'b': 2}, 'ghi': {'a': 7, 'c': 9, 'b':8}}
    
    and prints a bordered grid in the below format:
    
    |--------------------|--------------------|--------------------|
    |         a          |         c          |         b          |
    |--------------------|--------------------|--------------------|
    |         1          |         3          |         c          |
    |         7          |         9          |         8          |
    |--------------------|--------------------|--------------------| '''
       
    def _print_hz_BORDER(num_cols): 
        ''' prints a horizontal border of the form :
        |--------------------|--------------------|--------------------| '''
        out_str= VZ_BORDER
        for i in range(num_cols):
                out_str += ULINE.ljust(PAD,ULINE)+VZ_BORDER
        print out_str
        
    PAD=20
    VZ_BORDER="|"
    ULINE="-"
    
    num_keys = len(d[d.keys()[0]].keys())
        
    # ensure table starts on a new line
    print
        
    # print top VZ_BORDER for column names/table
    _print_hz_BORDER(num_keys)
            
    # print column names
    out_str = VZ_BORDER
    for key in d[d.keys()[0]].keys():
        out_str += str(key).center(PAD) + VZ_BORDER
    print out_str
        
    # print bottom VZ_BORDER for column names
    _print_hz_BORDER(num_keys)

    # print values
    for key1 in d.keys():
        out_str= VZ_BORDER
        for key2,val2 in d[key1].iteritems():
            out_str += str(val2).center(PAD)+VZ_BORDER
        print out_str
    
    # print bottom VZ_BORDER for table
    _print_hz_BORDER(num_keys)
    
    # ensure blanl line between table and any additional output
    print