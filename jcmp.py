#!/usr/bin/env python3

import json
import sys

def readf(fl):
    with open(fl) as f:
        js=json.load(f)
    return js

    
def jexpand(js,prepend="",postpend="",idkeys="",level=0):
    #print("jexpand called {} {} {}--{}".format(js,type(js),prepend,postpend))
    expansion=[]
    if type(js)==type([]):
        cnt=0
        for j in js:
            result=jexpand(j,prepend=prepend+"[]",postpend=""+postpend,idkeys=idkeys,level=level+1)
            expansion.extend(result)
            cnt+=1
    elif type(js)==type({}):
        idkey=None
        for j in js.keys():
            if j in idkeys:
                idkey=js[j]+"("+str(level)+")"
        for j in js.keys():
            if idkey:
                postpendadd=""+postpend +"-MId {}-".format(idkey)
            else:
                postpendadd=""+postpend
            result=jexpand(js[j],prepend=prepend+".{}".format(j),postpend=postpendadd,idkeys=idkeys,level=level+1)
            expansion.extend(result)
    else:
        #print("{}{}{}".format(prepend,js,postpend))
        expansion.append("{}={}{}".format(prepend,js,postpend))
    return expansion
            
def jcompare(ja,jb,mks=[]):
    result1=jexpand(ja,idkeys=mks)
    result2=jexpand(jb,idkeys=mks)

    diffs1=[]
    for elem in result1:
        if elem not in result2:
            diffs1.append(elem)

    diffs2=[]
    for elem in result2:
        if elem not in result1:
            diffs2.append(elem)

    return {"a":diffs1,"b":diffs2}


if __name__=="__main__":
    if len(sys.argv)<3:
        print("Usage: {} file1 file2".format(sys.argv[0]))
        exit(1)

    args=sys.argv
    majorkeys=[]
    while "-m" in args:
        idx=args.index("-m")
        args.pop(idx) # remove -m
        majorkeys.append(args.pop(idx)) # remove -m value and add to list


    fl1=args[1]
    fl2=args[2]
    
    js1=readf(fl1)
    js2=readf(fl2)
    
    diffs=jcompare(js1, js2, majorkeys)
    print(json.dumps(diffs,indent=4))
