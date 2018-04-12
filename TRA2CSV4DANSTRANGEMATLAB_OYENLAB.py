# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 16:14:28 2018

@author: john3
"""

#modules necessary to run program
import pandas as pd
import os
import fileinput
import pathlib
import shutil

#populates a list of all .TRA files that exists in the same directory as this python program
tralist=[]
for stuff in os.listdir():
    if stuff.endswith(".TRA"):
        tralist.append(stuff)
        
#The rest of the program is one gigantic "for" loop  which runs through for each .TRA file in tralist      
for eachtrafile in tralist:
    mytra=eachtrafile
#This block makes a junk directory that intermediary files are saved to. it can/will be deleted after conversion run for each .TRA
    junkdirectory="junkdirectory"
    pathlib.Path(junkdirectory).mkdir(parents=True, exist_ok=True)
    ignore1="durp1.csv"
    ignore2="durp2.csv"

#this block opens the .tra as a .csv and eliminates the top 4 lines
    FIRST_ROW_NUM=0
    ROWS_TO_DELETE={0,1,2,3}
    with open(mytra, "rt") as infile, open(ignore1, "wt") as outfile:
        outfile.writelines(row for row_num, row in enumerate(infile, FIRST_ROW_NUM)
                            if row_num not in ROWS_TO_DELETE)
        outfile.close(), infile.close()

#Takes first intermediary file and changes the labels and generates 2nd intermediary file
    inputFileName=ignore1
    outputFileName=ignore2 
    with open(outputFileName, "w") as outfile:
        for line in fileinput.input(
                [inputFileName],
                inplace=False):
                if fileinput.isfirstline():
                    outfile.write("Load,Time,Extension\n(N),(sec),(mm)\n")
                else:
                    outfile.write(line)
        outfile.close(), infile.close()

#This provides the final reordering of columns then feeds the MATLAB .csvs into a new subdirectory
    df=pd.read_csv(ignore2)
    df_reorder=df[["Extension", "Load", "Time"]]
    df_reorder.to_csv(mytra[:-4]+"_MATLABready.csv", index=False)

#moves intermediate .csvs to junk directory and delete it
    shutil.move(ignore1, junkdirectory+"/"+ignore1)
    shutil.move(ignore2, junkdirectory+"/"+ignore2)
    shutil.rmtree(junkdirectory)

#this makes a new subdirectory where all the 
    MATLABformattedSubdirectory="MATLABreadyfiles"
    pathlib.Path(MATLABformattedSubdirectory).mkdir(parents=True, exist_ok=True)
    for item in os.listdir():
        if item.endswith("MATLABready.csv"):
            shutil.move(item, MATLABformattedSubdirectory+"/"+item)

