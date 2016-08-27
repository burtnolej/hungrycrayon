from collections import OrderedDict

rotate=['',0,90,270]
gravity=['','center']
background=['','\'#d6d2d0\'','\'#0000ff\'','\'#ff0000\'']
extent=['','200x200','200x800','800x200']
pointsize=['',8,10,12,18,24,48]
font=['','Helvetica']
label=['foobar','barfoo']

settings = ['-gravity ','-background ','-pointsize ','-font ']
file_input= [' label:']
image_operator = ['-rotate ','-extent ']
args = settings + file_input + image_operator

def cmd_write_file(cmd):
    cmdexec="convert -verbose"
    for k,v in cmd.iteritems():
        if v <> '':
            cmdexec = cmdexec + " {0}{1}".format(k,v)
    
    f.write("echo '\n\n{0}'\n".format(cmdexec))
    cmdexec += "\n"
    f.write(cmdexec)
    
def run(depth,cmd):
    depth+=1
    if depth < len(args):
        settingtype = args[depth]
        for item in globals()[settingtype[1:-1]]:
            cmd[settingtype] = item
            run(depth,cmd)
    else:
        cmdcopy = cmd.copy()
        filename = "".join(map(str,cmdcopy.values())) + ".gif"
        
        # convert output files cannot start with #
        cmdcopy[' '] = filename.replace('\'','').replace('#','')
        
        cmd_write_file(cmdcopy)
        cmd = initcmd()

def initcmd():
    
    cmd=OrderedDict()
    
    for s in settings:
        cmd[s] = None
    
    for fi in file_input:
        cmd[s] = None    

    for io in image_operator:
        cmd[s] = None
    return(cmd)

f = open("gifcmd.sh",'w+')
f.write("#!/bin/bash \n\n")


cmd = initcmd()
depth = -1
run(depth,cmd)

f.close()
