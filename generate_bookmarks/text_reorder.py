import re
import random
from PyPDF2 import PdfFileWriter, PdfFileReader


"""
read original pdf and extract its table of content pages; 
save it into output folder 
"""
input = PdfFileReader(open('./generate_bookmarks/input/target_original.pdf', 'rb')) # open input

# depending on where are the actual toc pages 
for toc_page_num in range(1, 5):
    page = input.getPage(toc_page_num)
    page_content = page.extractText()

    extract_text = open(f'./generate_bookmarks/output/TOC.txt', "w")
    extract_text.writelines(page_content)




"""
Read extracted toc pages; clean it and reorder them into the template as below

Note: The last element of each line is the page number. 

Chapter 1: Getting Started Using SAS Software 1 
1.1 The SAS Language 1 
1.2 SAS Data Sets 4 

xxx

Chapter 2: Getting Your Data into SAS 38 
2.1 Methods for Getting Your Data into SAS 38 
2.2 Enterin g Data with the Viewtable Window 41 


"""            

combined_newlines = []
for toc_page_num in range(1, 5):
    fin = open(f"./generate_bookmarks/output/TOC{toc_page_num}.txt", "r")
    lines = fin.readlines()

    new_lines = []

    for each_line in lines:
        list = each_line.split()
        if list:
            if not list[0].startswith('.'):
                new_lines.append(' '.join(list))
    
    if toc_page_num == 1:
        starts = [new_lines.index(l) for l in new_lines if l.startswith('Chapter 1')]
        i = starts[0]
        print(i)
    else:
        i = 0
    
    while i < len(new_lines):
        # print(i)
        if new_lines[i].startswith('Chapter'):
            new_item = ' '.join(new_lines[i: i+3])
            combined_newlines.append(new_item)
            i += 3
    
        if re.match("\d+\.\d", new_lines[i]):
            end_point = 2

            if i + end_point >= len(new_lines):
                new_item = ' '.join(new_lines[i, :])
            else:           
                while not new_lines[i + end_point][0].isdigit() or (i + end_point >= len(new_lines)):
                    end_point += 1
                new_item = ' '.join(new_lines[i: i+end_point + 1])

            # print('new item:', new_item)
            combined_newlines.append(new_item)
            i += end_point + 1

        elif re.match("\d", new_lines[i]):
            i+= 1

        else:
            new_item = ' '.join(new_lines[i: i+2])
            combined_newlines.append(new_item)
            i += 1


"""
double check if the last number is the page number;
If not, we may split the item into two lines. In that case, we should re-combine them together

"""
for i in range(len(combined_newlines)):
    if not combined_newlines[i][-1].isdigit():
        combined_newlines[i] = ''.join(combined_newlines[i:i+2])


"""
Save the cleaned TOC into output folder
"""
# print(combined_newlines)
with open('./generate_bookmarks/output/cleaned_toc_all.txt', 'w') as f:
    for element in combined_newlines:
        f.write(f"{element} \n")


