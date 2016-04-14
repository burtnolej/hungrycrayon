#!/usr/bin/python
from sys import path,stdout
import sys
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import file2list_gen
from inspect import getmembers

location = ['lon','ny','hk','tk','blr']
code = ['na','m2','s2','m1','s1','ad03']
title = ['vp','md','none']
code_val = {'md':4,'m2':3,'s2':3,'m1':2,'s1':2,'ad03':1,'ad02':0,'ad01':0}
field_nm = ['name','loc','locmgr','glbmgr','matmgr','title','code']
defs = {'name':'name of employee',
        'loc':'location of employee',
        'logmgr':'local manager',
        'glbmgr':'global manager',
        'matmgr':'matric manager',
        'title':'corporate title',
        'tenure':'length of tenure',
        'code':'job code',
        'count':'number of nodes lower than this point',
        'childvalue':'value of nodes lower than this point',
        'value':'value of this node',
        'levels':'number of levels below this node'}

assert len(sys.argv) == 3 # make sure a filename is passed as arg
assert sys.argv[2] in ['\\t',','] # pass in '\t' or ',' as a delim

class TreeBuilder(object):
    '''
    reads a file and builds a Tree class of TreeNodes nodes
    '''
    def __init__(self):
        self.tree=Tree()

        q_rec = []
        for record in self.process_inputfile(sys.argv[1],sys.argv[2]):
            print 'processing',record.__getitem__('name'),
            if not self.process_field(self.tree,**record):
                q_rec.append(record)
                print 'queueing'
            else:
                print 'done'

        # process things put in queue
        for record in q_rec:
            name = record.__getitem__('name'),
            print 'qprocessing',name
            if not self.process_field(self.tree,**record):
                print 'error'
                raise Exception(name) # mgr does not exist
            else:
                print 'done'

        # calc levels and widths
        self.tree.populate_vals(self.tree.head,0)
    
    def process_inputfile(self,filename,delim="\t"):
        '''
        a generator
        take a csv where each row is in format field_nm
        and yield dicts with the dict items = field_nm
        '''
        l=[]

        with open(filename) as fh:
            next(fh) # skip line as expecting a header
            for line in fh:
                field = {}
                i=0
                for itm in line.rstrip().split("\t"):
                    field.__setitem__(field_nm[i],itm)
                    i+=1
                yield field
        
    def process_field(self,tree,**kwargs):
        '''
        takes a dict as an arg and adds the node into the tree
        and recalculates count, values and levels
        '''
        tn = TreeNode(**kwargs)
    
        if not tree.add_node(tn):
            return False
        return(True)

class Logger(object):
    import sys
    def __init__(self,fn='/tmp/log.txt'):
        self.lh = open(fn,'w+')
        self.tmp_stdout = self.sys.stdout
        self.sys.stdout = self.lh

    def __del__(self):
        self.sys.stdout = self.tmp_stdout
        self.lh.close()
    
class TreeNode(object):
    def __init__(self,**kwargs):
        for key,value in kwargs.iteritems():
            setattr(self,key,value)

        # add a list for siblings to be added for tree traversing
        setattr(self,'childlist',list())
        setattr(self,'childcount',0) # number of children
        setattr(self,'descvalue',0) # descendant value
        setattr(self,'desccount',0) # descendant value

    def items(self):
        for k,v in getmembers(self):
            if not str(k).startswith("__") and not callable(v):
                yield k,v
            
class Tree(dict):
    count=0 # number of nodes
    head=None # ref to first node
    value=0 # total value of snrs in tree
    widths=[0,0,0,0,0,0,0,0,0,0,0,0] # width of each level
    def add_node(self,tn):
        '''
        takes a TreeNode ref as an arg
        adds the TreeNode to the Tree
        key=employee name; value=ref to TreeNode
        '''
        # if its a blank line skip
        if self.is_blank(tn):
            return(True)

        # if its a comment skip
        if self.is_comment(tn):
            return(True)
        
        assert self.get_node(tn.name) == False # node already added

        # if its not the head but glbmgr does not exist
        # put on queue to process later in case its later on in
        # the file
        if not self.is_node(tn.glbmgr) and not self.is_head(tn):
            return(False)

        # add the node to the Tree
        self.__setitem__(tn.name,tn)

        # update values for this node
        tn.value = code_val.__getitem__(tn.code)

        # check if this node is the head as it will have no parent
        if self.is_head(tn):
            self.value += tn.value
            self.head = tn
            return(True)
        
        # lookup glbmgr parent node and add a field glbmgr_node
        glbmgr_tn = self.get_node(tn.glbmgr)
        tn.glbmgr_node = glbmgr_tn

        # add a reference to the sibling in the glbmgr node
        l = glbmgr_tn.childlist
        l.append(tn)
        glbmgr_tn.childcount += 1
        
        # traverse up the tree updating values to account for the
        # new employee
        node = tn
        while not self.is_head(node):
            node = node.glbmgr_node
            node.descvalue += tn.value
            node.desccount += 1

        assert self.head != None # must be a head

        # keep checksums for tree
        self.value += tn.value
        self.count += 1

        return(True)

    def is_blank(self,tn):
        if tn.name == "":
            print "blank line skipped"
            return True

    def is_comment(self,tn):
        if tn.name[0:3] == "###":
            print "ignored comment",tn.name
            return True

    def is_head(self,tn):
        if tn.glbmgr == 'na':
            return True
        else:
            return False
        
    def get_node(self,name):
        if self.has_key(name):
            return(self.__getitem__(name)) 
        else:
            return(False)

    def is_node(self,name):
        if self.has_key(name):
            return True
        else:
            return False
        
    def pprint(self):
        for name,node in self.iteritems():
            print name,node
            for k,v in node.items():
                print k.rjust(15),v
            print

    def pprint_span(self):
        for name,node in self.iteritems():
            print name,node.childcount,node.desccount

    def _pad(self,level,*els):
        mystr = "".ljust(level* 4," ")
        for el in els:
            mystr+=" "+str(el)
        return(mystr)

    def calc_pyramid(self,node):
        if node.desccount == 0:
            return 0
        else:
            return(float(node.descvalue + node.value)/node.desccount)

    def pprint_tree(self,node,level,printleaves=False):

        prnstr = self._pad(level,
                           level,
                           node.name,
                           round(self.calc_pyramid(node),2),
                           node.desccount)
        
        if node.childcount > 0:
            print prnstr
            level+=1
            for childnode in node.childlist:
                self.pprint_tree(childnode,level)
        else:
            if printleaves:
                print prnstr

    def pprint_tree_balance(self,child,printleaves=False):
        childlist = child.childlist
        i=0
        middle=len(childlist)//2
        for c in childlist:
            if i==0 and printleaves:
                print
            if c.childcount == 0:
                if printleaves:
                    print self._pad(c.level,
                                    c.level,
                                    c.name,
                                    round(self.calc_pyramid(c),2),
                                    c.desccount)


            
            if i==middle:
                mid_node = self.get_node(child.name)

                print self._pad(mid_node.level,
                            mid_node.level,
                            mid_node.name,
                            round(self.calc_pyramid(mid_node),2),
                            mid_node.desccount)
            self.pprint_tree_balance(c)
            
            i+=1
            if i==len(childlist) and printleaves:
                print
        

    def pprint_widths(self):
        i=0
        for w in self.widths:
            if w>0:
                print i,w
                i+=1

    def populate_vals(self,node,level):
        node.level = level
        self.widths[level] += 1
        if node.childcount > 0:
            level+=1
            for childnode in node.childlist:
                self.populate_vals(childnode,level)

        
        
if __name__ == '__main__':

    l=Logger('/tmp/log.txt') # point stdout to logfile
    tb = TreeBuilder() # load the tree
    del l # set stdout back to screen

    #tb.tree.pprint_tree(tb.tree.head,0)
    #tb.tree.pprint_widths()

    tb.tree.pprint_tree_balance(tb.tree.head)
    print
    print


