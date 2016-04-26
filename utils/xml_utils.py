#!/usr/bin/python
import xml.etree.ElementTree as xmltree

def get_xml_root(filen, ns=None):
    ''' return the root node '''
    return(xmltree.parse(filen))

def get_xml_elements(filen, tag, root=None,ns=None):
    ''' starting at the root, search for any elements where tag=tag
    and return a list of those xmlelement objects. root will default
    to the top of the tree unless a lower level node is provided '''
    
    if root==None: #assume we search from actual tree root
        search_root = xmltree.parse(filen)
    else:
        search_root = root
        
    return(search_root.findall(tag,ns))

def get_xml_element(filen, tag, root=None,ns=None):
    ''' starting at the root, search for the element where tag=tag
    and return the xml element object or throw error if more than one hit'''
    
    if root==None: #assume we search from actual tree root
        search_root = xmltree.parse(filen)
    else:
        search_root = root
        
    elements = search_root.findall(tag,ns)
    
    if len(elements)>1:
        raise Exception
    
    return(elements[0])
           
def get_xml_child_elements(parent):
    ''' for a given xml element, return all children as a list of tuples of the form
    (name,value)'''
    
    d={}
    for child in parent._children:
        d[child.tag]=child.text
    return(d)
