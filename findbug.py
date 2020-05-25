"""
findbug.py <bug.txt> <landscape.txt>

Trayport VisoTech GmbH 
Test for applicants for the role of Software Developer
Daniel Burnier de Castro
21.05.2020

STEPS:
1) extract scructure from 'bug.txt'. In the file we  have following structure, 
    where Line is the text line and Pos is the column position in that line
 
+------+-------+-------------+
| Line |  Pos  |  Bug Part   |
+------+-------+-------------+
|  0   |   0   | '| |'       |
|  1   |   0   | '###O'      |
|  2   |   0   | '| |'       |
+------+-------+-------------+

2) scan the 'landscape.txt' file and list all 'bug parts' found.

+------+-------+-------------+
| Line |  Pos  |  Bug Part   |
+------+-------+-------------+
|  1   |   4   | '| |'       |
|  2   |   4   | '###O'      |
|  3   |   4   | '| |'       |
|  3   |  18   | '| |'       |
|  4   |  18   | '###O'      |
|  5   |  18   | '| |'       |
|  5   |  35   | '| |'       |
|  6   |  35   | '###O'      |
|  7   |  35   | '| |'       |
+------+-------+-------------+

3) Look for matching from bug in landscape. We start with the first line,
    if it is a match, we increase the Line by 1 and keep the same Pos 
    (the starting position of all bug parts is 0 - therefore, all matches need
    to have equal starting Pos)


"""

import sys
import re

# used to remove duplicates - e.g. one "pair of wings" shared by two bugs
def remove_duplicate_list_of_lists(input_list):
    new_list = []
    for elem in input_list:
        if elem not in new_list:
            new_list.append(elem)
    return new_list

# for the regix functions we need to add an escape signal to the pipe symbol (or any other especial symbol)
def escape_especial_char(string):
    escaped_string = string.translate(str.maketrans({"-":  r"\-", 
                                                     "]":  r"\]",
                                                     "\\": r"\\",
                                                     "^":  r"\^",
                                                     "$":  r"\$",
                                                     "*":  r"\*",
                                                     "|":  r"\|",
                                                     ">":  r"\>",
                                                     "<":  r"\<",                                                     
                                                     ".":  r"\."}))
    return escaped_string


# read bug.txt
bug = []
with open(sys.argv[1], 'r') as f:                                              #uncomment to read file from command line
#with open('bug.txt') as f:
    for i, line in enumerate(f):
        if re.search(r'\S', line):                                              #read only lines with any char except whitespaces
            index_bug_part = len(line) - len(line.lstrip())                     #index of first non whitespace (begin of bug part)
            line = line.strip('\n')                                             #remove '\n' from string
            bug.append([i, index_bug_part, line])
    
bug_n_lines = len(bug)                                                          #number of lines of the bug pattern
    

bug_parts_list = []
with open(sys.argv[2], 'r') as f:                                              #uncomment to read file from command line
#with open('landscape.txt') as f:
    for i, line in enumerate(f):
        if re.search(r'\S', line):                                              #read only lines with any char except whitespaces
            for j in range(bug_n_lines):
                escaped_bug_part = escape_especial_char(bug[j][2])              #for each line: search all occurences of bug parts
                flex_bug = escaped_bug_part.replace(' ','.')                    #to account for any char within the "wings" of the bug (regex considers "." = any char)
                for m in re.finditer(flex_bug, line):
                    bug_parts_list.append([i, m.start(), bug[j][2]])
            
bug_parts_list = remove_duplicate_list_of_lists(bug_parts_list)

#for element in bug_parts_list:
#    print(element)


#find bug pattern in bug list
bug_parts_found = 0                                                             # [1..3] - if 3, all bug parts were found
bug_checked = []                                                                # if bug checked, it is moved to an aux. list
bug_counter = 0                                                                 # number of bugs found
for bug_part in bug_parts_list:
    bug_parts_found = 0                                                         #reset the counter for parts found
    if bug_part not in bug_checked:                                             #first line of bug used as reference
        if (bug_part[2] == bug[0][2]):
            bug_parts_found += 1
        
        # if first part of bug present, check if the following lines match
        for shift in range(1,bug_n_lines):
            if [bug_part[0]+shift, bug_part[1], bug[shift][2]] in bug_parts_list:  #bug_part[1] as all bug parts start in the same position
                bug_parts_found += 1      

        if bug_parts_found == bug_n_lines:                                      # if all bug parts found
            bug_counter += 1
            bug_checked.append(bug_part)                                        #add to the reference part to bug_checked
            for shift in range(1,bug_n_lines):                                  #add other parts to bug_checked
                bug_checked.append([bug_part[0]+shift, bug_part[1], 
                                    bug[shift][2]])         


print('Bugs found: ', bug_counter)
for ln in bug_checked:
    print(ln)


