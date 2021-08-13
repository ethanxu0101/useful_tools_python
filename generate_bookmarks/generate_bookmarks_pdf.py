from PyPDF2 import PdfFileWriter, PdfFileReader




output = PdfFileWriter() # open output
input = PdfFileReader(open('./generate_bookmarks/input/target_original.pdf', 'rb')) # open input
toc = open('./generate_bookmarks/output/cleaned_toc_all.txt', 'r')
toc_lines = toc.readlines()

n = input.getNumPages()

for i in range(n):
   output.addPage(input.getPage(i)) # insert page

for toc_line in toc_lines:
    toc_item = toc_line.split()
    try:
         int(toc_item[-1])
    except:
        print(toc_item)
    output.addBookmark(' '.join(toc_item[:-1]), int(toc_item[-1])+14, parent=None) # add a bookmark 


outputStream = open('./output/target_toc.pdf','wb') #creating result pdf JCT
output.write(outputStream) #writing to result pdf JCT
outputStream.close() #closing result JCT