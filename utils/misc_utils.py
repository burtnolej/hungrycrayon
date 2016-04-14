def write_text_to_file(filename,text):
    fh = open(filename,'w+')
    fh.write(text)
    fh.close
    
def read_text_from_file(filename):
    'returns a list of strings'
    l=[]
    fh = open(filename, 'r+')
    return [line.rstrip() for line in fh]

def read_delim_text_from_file(filename,delim):
    'returns a list of lists'
    l=[]
    fh = open(filename, 'r+')
    return [l.append(line.rstrip().split(delim) for line in fh)]