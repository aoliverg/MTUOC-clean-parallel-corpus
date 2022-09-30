#    MTUOC-clean-parallel-corpus-lite-GUI
#    Copyright (C) 2022  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import codecs
import re
import sys
from xml.sax.saxutils import unescape
import html
import argparse
from bs4 import BeautifulSoup
import re
import regex as rx
from ftfy import fix_encoding

from tkinter import *
from tkinter.ttk import *

import tkinter 
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tkinter import ttk


def remove_tags(segment):
    segmentnotags=re.sub('<[^>]+>',' ',segment).strip()
    segmentnotags=re.sub(' +', ' ', segmentnotags)
    return(segmentnotags)


def normalize_apos(segment):
    segmentnorm=segment.replace("’","'")
    segmentnorm=segmentnorm.replace("`","'")
    segmentnorm=segmentnorm.replace("‘","'")
    return(segmentnorm)
    
def remove_empty(SLsegment,TLsegment):
    remove=False
    if SLsegment.strip()=="": remove=True
    if TLsegment.strip()=="": remove=True
    return(remove)

def remove_short(segment,minimum):
    remove=False
    if len(segment)<int(minimum):
        remove=True
    return(remove)

def remove_equal(SLsegment,TLsegment):
    remove=False
    if SLsegment.strip()==TLsegment.strip(): remove=True
    return(remove)
    
def unescape_html(segment):
    segmentUN=html.unescape(segment)
    return(segmentUN)
    
def percentNUM(segment):
    nl=0
    nn=0
    for l in segment:
        if l.isdigit():
            nn+=1
        else:
            nl+=1
    if len(segment)>0:
        percent=100*nn/len(segment)
    else:
        percent=0
    return percent
def percentLET(segment):
    nl=0
    nn=0
    for l in segment:
        if l.isdigit():
            nn+=1
        else:
            nl+=1
    percent=100*nl/len(segment)
    return percent
    
def escapeforMoses(segment):
    segment=segment.replace("[","&lbrack;")
    segment=segment.replace("]","&rbrack;")    
    segment=segment.replace("|","&verbar;")
    segment=segment.replace("<","&lt;")
    segment=segment.replace(">","&gt;")
    return(segment)

def remove_control_characters(cadena):
    return rx.sub(r'\p{C}', '', cadena)
    
def select_file1():
    file1=askopenfilename(initialdir = ".",filetypes =(("All Files","*.*"),("text files", ["*.txt"])),
                           title = "Choose corpus file to clean.")
    E1.delete(0,END)
    E1.insert(0,file1)
    E1.xview_moveto(1)
   
def select_output_file():
    outfile = asksaveasfilename(initialdir = ".",filetypes =(("All Files","*.*"),("text files", ["*.txt"])),
                           title = "Choose a output file.")
    E2.delete(0,END)
    E2.insert(0,outfile)
    E2.xview_moveto(1)
    
def go():
    argremove_control_characters=True
    argnorm_apos=True
    argremove_tags=True
    argunescape_html=True
    argfixencoding=True
    argremove_empty=True
    argremove_short=5
    argremove_NUMPC=60
    argremove_equal=True
    argescapeforMoses=True
    argremove_NUMPC=60
    
    entrada=codecs.open(E1.get(),"r",encoding="utf-8")
    sortida=codecs.open(E2.get(),"w",encoding="utf-8")

    for linia in entrada:
        toWrite=True
        linia=linia.strip()
        camps=linia.split("\t")
        if len(camps)>=1:
            slsegment=camps[0]
            tlsegment=""
        if len(camps)>=2:
            tlsegment=camps[1]
        if argremove_control_characters:
            slsegment=remove_control_characters(slsegment)
            tlsegment=remove_control_characters(tlsegment)    
        if argunescape_html and toWrite:
            slsegment=unescape_html(slsegment)
            tlsegment=unescape_html(tlsegment)
        if argfixencoding:
            slsegment=fix_encoding(slsegment)
            tlsegment=fix_encoding(tlsegment)
        if argremove_tags and toWrite:
            slsegment=remove_tags(slsegment)
            tlsegment=remove_tags(tlsegment)
        if argnorm_apos and toWrite:
            slsegment=normalize_apos(slsegment)
            tlsegment=normalize_apos(tlsegment)
        if argremove_empty and toWrite:
            if remove_empty(slsegment,tlsegment): toWrite=False
        if argremove_short and toWrite:
            if remove_short(slsegment,argremove_short): toWrite=False
        if argremove_short and toWrite:
            if remove_short(slsegment,argremove_short): toWrite=False
            if remove_short(tlsegment,argremove_short): toWrite=False
        if argremove_equal and toWrite:
            if remove_equal(slsegment,tlsegment): toWrite=False
        if argremove_NUMPC and toWrite:
            if percentNUM(slsegment)>=float(argremove_NUMPC):
                toWrite=False
            elif percentNUM(tlsegment)>=float(argremove_NUMPC):
                toWrite=False
        if argescapeforMoses and toWrite:
            slsegment=escapeforMoses(slsegment)
            tlsegment=escapeforMoses(tlsegment)
        
        if toWrite:
            sortida.write(linia+"\n")

top = Tk()
top.title("MTUOC clean parallel corpus lite")

B1=tkinter.Button(top, text = str("Input file"), borderwidth = 1, command=select_file1,width=14).grid(row=0,column=0)
E1 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E1.grid(row=0,column=1)

B2=tkinter.Button(top, text = str("Output file"), borderwidth = 1, command=select_output_file,width=14).grid(row=1,column=0)
E2 = tkinter.Entry(top, bd = 5, width=50, justify="right")
E2.grid(row=1,column=1)

B5=tkinter.Button(top, text = str("Go!"), borderwidth = 1, command=go,width=14).grid(sticky="W",row=2,column=0)

top.mainloop()


'''

if all:
    remove_control_characters=True
    norm_apos=True
    remove_tags=True
    unescape_html=True
    fixencoding=True
    remove_empty=True
    remove_short=10
    remove_NUMPC=60
    remove_equal=True
    escapeforMoses=True
    if not remove_NUMPC: remove_NUMPC=60
    if not remove_short: remove_short=5
entrada=codecs.open(inputfile,"r",encoding="utf-8")
sortida=codecs.open(outputfile,"w",encoding="utf-8")

if stringFromFile:
    sfile=codecs.open(stringFromFile,"r",encoding="utf-8")
    remlist=[]
    for lsfile in sfile:
        lsfile=lsfile.rstrip()
        remlist.append(lsfile)
        
if regexFromFile:
    regfile=codecs.open(regexFromFile,"r",encoding="utf-8")
    reglist=[]
    for lsfile in regfile:
        lsfile=lsfile.rstrip()
        reglist.append(lsfile)

if vSetLanguages:
    toset=[]
    for l in vSetLanguages.split(","):
        toset.append(l)
    langid.set_languages(toset)

for linia in entrada:
    toWrite=True
    linia=linia.strip()
    camps=linia.split("\t")
    if len(camps)>=1:
        slsegment=camps[0]
        tlsegment=""
    if len(camps)>=2:
        tlsegment=camps[1]
    if remove_control_characters:
        slsegment=remove_control_characters(slsegment)
        tlsegment=remove_control_characters(tlsegment)    
    if unescape_html and toWrite:
        slsegment=unescape_html(slsegment)
        tlsegment=unescape_html(tlsegment)
    if fixencoding:
        slsegment=fix_encoding(slsegment)
        tlsegment=fix_encoding(tlsegment)
    if remove_tags and toWrite:
        slsegment=remove_tags(slsegment)
        tlsegment=remove_tags(tlsegment)
    if norm_apos and toWrite:
        slsegment=normalize_apos(slsegment)
        tlsegment=normalize_apos(tlsegment)
    if remove_empty and toWrite:
        if remove_empty(slsegment,tlsegment): toWrite=False
    if remove_short and toWrite:
        if remove_short(slsegment,remove_short): toWrite=False
    if remove_short and toWrite:
        if remove_short(slsegment,remove_short): toWrite=False
        if remove_short(tlsegment,remove_short): toWrite=False
    if remove_equal and toWrite:
        if remove_equal(slsegment,tlsegment): toWrite=False
    if remove_NUMPC and toWrite:
        if percentNUM(slsegment)>=float(remove_NUMPC):
            toWrite=False
        elif percentNUM(tlsegment)>=float(remove_NUMPC):
            toWrite=False
    if escapeforMoses and toWrite:
        slsegment=escapeforMoses(slsegment)
        tlsegment=escapeforMoses(tlsegment)
    if vSL and toWrite:
        (lang,logpercent)=langid.classify(slsegment)
        if not vSL==lang:
                toWrite=False
                if verbose: print("SOURCE NOT MATCHING:",vSL,lang,slsegment)

    if vTL and toWrite:
        (lang,logpercent)=langid.classify(tlsegment)
        if not vTL==lang:
                toWrite=False
                if verbose: print("TARGET NOT MATCHING:",vTL,lang,tlsegment)
            
    if vTNOTL and toWrite:
        (lang,logpercent)=langid.classify(tlsegment)
        if vTNOTL==lang:
                toWrite=False
                if verbose: print("TARGET MATCHING:",vTNOTL,lang,tlsegment)
        

    if noUPPER and toWrite:
        if slsegment==slsegment.upper():
            toWrite=False
            if verbose: print("DELETE UPPER:",slsegment)
        if tlsegment==tlsegment.upper():
            toWrite=False
            if verbose: print("DELETE UPPER:",tlsegment)
                
    if stringFromFile and toWrite:
        for rmstring in remlist:
            if slsegment.find(rmstring)>-1:
                toWrite=False
                break
            if tlsegment.find(rmstring)>-1:
                toWrite=False
                break
                
    if regexFromFile and toWrite:
        for regex in reglist:
            pattern = re.compile(regex)
            if pattern.search(slsegment):
                toWrite=False
                break
            if pattern.search(tlsegment):
                toWrite=False
    if toWrite:
        sortida.write(linia+"\n")
        
'''