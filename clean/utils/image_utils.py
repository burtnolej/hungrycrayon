import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils_generic import GenericBase
from misc_utils_process import *
from misc_utils import os_file_exists
from os import mkdir, getcwd
from os.path import join as ospathjoin
from datetime import datetime

settings = ['gravity','background','pointsize','font']
image_operator = ['rotate','size','extent']

def parse_convert_stdout(p,label):
    
    ''' parse stdout and sterr messages created by imagemagick
    convert command
    
    stdout:
    label:label=>label LABEL 28x13 28x13+0+0 16-bit DirectClass 0.030u 0:00.030
    label:label=>/tmp/foobar.gif LABEL 28x13 28x13+0+0 16-bit Palette PseudoClass 88c 0.040u 0:00.039
    
    stderr:
    convert.im6: unrecognized option `-verboe' @ error/convert.c/ConvertImageCommand/2975.
    
    returns:
    for sucess (0,size of output file widthxheight,outputfile)
    for failire (1,stderr message)
    '''
    
    stdout = p.stdout.read().split("\n")[1]
    
    if stdout.startswith('label:'+label) == True:
        size = stdout.split(" ")[2]
        outputfile = stdout.split(">")[1].split(" ")[0]
        return((0,stdout,size,outputfile))
    else:
        return((1,stdout))

def rgbstr_get(r,g,b):
    return("rgb({r},{g},{b})".format(r=r, g=g,b=b))

def sizestr_get(x,y):
    return("{x}x{y}".format(x=x, y=y))
           
def labelstr_get(label):
    return("label:{label}".format(label=label))
 
def now():
    return(str(datetime.now().strftime("%m%d%y")))

def get_gif_filename(dir,label,args):    
    argcopy = args.copy()
    filename =""
    for s in settings:
        if args.has_key(s) == True:
            filename = filename + str(args[s])
            
    filename = filename + label
        
    for io in image_operator:
        if args.has_key(io) == True:
            filename = filename + str(args[io])

    filename = filename+ ".gif"
    filename = filename.replace("#","")
    
    filename = ospathjoin(dir,filename)
    
    return(filename)

class ImageCreate(GenericBase):
    
    def create_image_file(self,labels, **kw):

        if not kw.has_key('overwrite'):
            kw['overwrite'] = False
            
        if not isinstance(labels,list):
            labels = [labels]
        
        self.outputfiles = []
        self.labels = labels
        self.outputdirname = "ic_"+now()
        cwd = getcwd()
        
        try:
            mkdir(ospathjoin(cwd,self.outputdirname))
        except OSError: # directory exists
            pass
        
        self.log.log(self,3,"mkdir="+self.outputdirname)

        for lbl in self.labels:
            
            cmd = ['convert','-verbose']

            outputfilename = get_gif_filename(self.outputdirname,lbl,kw)
            #filename = lbl + "-" + "-".join(map(str,kw.values())) + ".gif"  
            #outputfilename = ospathjoin(self.outputdirname,filename)
            
            if os_file_exists(outputfilename) == False or kw['overwrite'] == True:
                
                # settings go before the input label/file
                for s in settings:
                    if kw.has_key(s):
                        cmd = cmd + ["-"+s,str(kw[s])]
        
                cmd.append(labelstr_get(lbl))  
                
                # image operators come afterwards
                for im in image_operator:
                    if kw.has_key(im):
                        cmd = cmd + ["-"+im,str(kw[im])]
                
                cmd.append(outputfilename)
    
                p = process_start(cmd)
                
                status = parse_convert_stdout(p,lbl)
                
                if status[0] == 0:
                    self.log.log(self,3,
                                 "created image="+outputfilename,
                                 "status"," ".join(map(str,status)))
                else:
                    self.log.log(self,3,"failed","status="," ".join(map(str,status)))
                    raise Exception("ImageCreate failure",status)
            else:
                self.log.log(self,3,"reused image="+outputfilename)
                
            self.outputfiles.append(outputfilename)
                
        return(self.outputfiles)
    
        
if __name__ == "__main__":
    tkgrey = rgbstr_get(240,240,237)
    white = rgbstr_get(255,255,255)
    black = rgbstr_get(0,0,0)
    
    ic = ImageCreate()
    
    inputfiles = ["foobar","foobar2","foobar3"]
    outputfiles = ic.create_image_file(inputfiles,
                                       background=tkgrey,
                                       fill=black,
                                       pointsize=22,
                                       rotate=270,
                                       font='Bookman-Light',
                                       gravity='center',
                                       extent=sizestr_get(30,100))