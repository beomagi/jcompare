#!/usr/bin/env python3

import json
import sys

def readf(fl):
    with open(fl) as f:
        js=json.load(f)
    return js

def jexpand(js):
    expansion=[]
    if type(js)==type([]):
        for j in js:
            addstr="[]."+json.dumps(jexpand(j))
            print(addstr)
            expansion.append(addstr)
    elif type(js)==type({}):
        for j in js.keys():
            addstr="{{{}}}.".format(j)+json.dumps(jexpand(js[j]))
            print(addstr)
            expansion.append(addstr)
    else:
        return "{}".format(js)
    return expansion
            
def jcompare(ja,jb):
    pass
    

if __name__=="__main__":
    fl1=sys.argv[1]
    #fl2=sys.argv[2]
    
    js1=readf(fl1)
    #js2=readf(fl2)
    
    #diffs=jcompare(js1, js2)
    for stuff in jexpand(js1):
        print(stuff)    