from subprocess import Popen, STDOUT, PIPE
from time import sleep
import sys
from misc_utils_enum import enum
from os import remove, kill
import signal
import unittest


__all__ = ['process_start','process_stdin','process_kill','process_instances_get', \
           'process_get_stdout']

def process_start(cmdlineargs,stdin=True):
    ''' pass stdin=True when you want the process to wait for 
    stdin '''
    args = dict(stderr=STDOUT,stdout=PIPE)
    
    if stdin == True:
        args['stdin'] = PIPE
    
    p = Popen(cmdlineargs,**args)

    return(p)

def process_get_stdout(process):
    return(process.stdout.read()) 
    
def process_stdin(process,stdinstr):
    ''' pass stdin to a process waiting for stdin '''
    return(process.communicate(input=stdinstr))

def process_kill(p):
    ''' accepts a Popen object and if not assumes its a PID str or int'''
    
    if isinstance(p,Popen) == True:
        _pid = p.pid
        p.kill()
    else:
        try:
            _pid = int(p)
            kill(_pid,signal.SIGTERM)
        except ValueError:
            raise Exception('requires an int or int as string')

    return()
    
def process_instances_get(match):

    cmd = ['ps','-ef']
    p = process_start(cmd)
    processlist = p.stdout.read()
    
    # put back into string format for grep -v an remove blank last item 
    process_str = "".join(list(processlist)[:-1]) 
    
    cmd = ['grep',match]
    pgrep1 = process_start(cmd,stdin=True)
    matches =  process_stdin(pgrep1,process_str)
    #pgrep1.communicate(input=process_str)
       
    # put back into string format for grep -v an remove blank last item 
    matches_str = "".join(list(matches)[:-1]) 
         
    cmd = ['grep','-v','defunct']
    pgrep2 = process_start(cmd,stdin=True)
    
    nondefunctmatches = process_stdin(pgrep2,matches_str)[0].split("\n")[:-1]

    pid = [(match.split(" ")[2],match.split(" ")[4]) for match in nondefunctmatches]
    
    return(pid)
