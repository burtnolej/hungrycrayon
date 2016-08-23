

from collections import OrderedDict


rotate=[0,90,270]
gravity=['center']
background=['\'#d6d2d0\'']
size=['200x200','200x800','800x200']
pointsize=[12,18,24,48]

settings = ['-gravity ','-background ','-pointsize ']
image_operator = ['-rotate ','-size ']
args = settings + image_operator


def cmd_write_file(cmd):
    cmdexec="convert "
    for k,v in cmd.iteritems():
        cmdexec = cmdexec + " {0}{1}".format(k,v)
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
        #cmd['filename'] = "-".join(map(str,cmd.values()))
        cmdcopy = cmd.copy()
        filename = "-".join(map(str,cmdcopy.values())) + ".gif"
        cmdcopy[' '] = filename.replace('\'','')
        
        cmd_write_file(cmdcopy)
        cmd={}

cmd=OrderedDict()

for s in settings:
    cmd[s] = None

cmd['label:'] = 'foobar'

for io in image_operator:
    cmd[s] = None

f = open("gifcmd.sh",'w+')

depth = -1
run(depth,cmd)

f.close()