# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 08:51:06 2022

@author: parth
"""

file = open('meeting_saved_closed_caption_2.txt', 'r', encoding='utf-8')



lines = []
while (line := file.readline().rstrip()):
    if line[-1] != ".":
        line = line[9:] + ". "
    else: 
        line = line[9:] 
    #print(line)
    lines.append(line)
    
file.close()    
with open('clean_file.txt', 'w') as op:
    for line in lines:
        op.write(line);op.write('\n')
     
op.close()   