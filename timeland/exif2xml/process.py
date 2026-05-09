import os
from EXIF import *

if __name__ == '__main__':

	imageDirectory = "/Users/even/Sites/loc/"
	outputFile = "/Users/even/Sites/imageData.xml"
	
	files = os.listdir(imageDirectory)

	try:
		outfile = open(outputFile,'w')
	except: 
		print "could not open outfile",outputFile

	outfile.write("<exif>\n")

	for f in files:



		p = imageDirectory + f
		try:
			infile = open(p,'rb')

		except:
			print p, "unreadable"
			continue
				
		data = process_file(infile)

		if not data:
		    print 'No EXIF information found'
		    continue
		
		outfile.write("<image>\n")
		outfile.write("<file>"+f+"</file>\n")
		
		#2004-06-30T07:58:38Z
		outfile.write("<time>"+data["EXIF DateTimeOriginal"].printable+"</time>\n")
		print data["EXIF DateTimeOriginal"].printable

		if data.has_key('JPEGThumbnail'):
		    print 'File has JPEG thumbnail'
		print

		infile.close()

		outfile.write("</image>\n")
		
	outfile.write("</exif>\n")
	outfile.close()
