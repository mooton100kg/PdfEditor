from PyPDF2 import PdfWriter, PdfReader, PdfMerger
from PyPDF2.generic import RectangleObject, AnnotationBuilder
import io,json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from math import ceil

def openFile(fileName):
	global writer, reader

	writer = PdfWriter()
	reader = PdfReader(open(fileName,'rb'))
def getNewContent():
	allContent = dict()
	loop = True
	while loop:
		topic = input("Topic : ")
		if topic == "finish":
			loop = not loop
		elif topic == "del":
			delete = input("Topic to delete : ")
			try:	
				del allContent[delete]
			except:
				print("Topic not found")
		else:
			page = input("Page : ")
			try:
				allContent[topic] = int(page)
			except:
				print("Error page number")
		for i in allContent:
			print(allContent[i], " : ", i, "\n")

	allContent = dict(sorted(allContent.items(), key=lambda x:x[1]))
	return allContent

def writeFile(fileName, allContent, contentNum = 0):
	packet = io.BytesIO()
	can = canvas.Canvas(packet, pagesize=A4)
	can.setFont('Courier',15)
	
	x = 800

	for i in allContent:
		i = str(allContent[i]) + " : " + i
		can.drawString(30, x, i)
		x -= 20
		if x < 80:
			x = 800
			can.save()

			packet.seek(0)

			contentPage = PdfReader(packet)
			writer.add_page(contentPage.pages[0])
			can = canvas.Canvas(packet, pagesize=A4)
			can.setFont('Courier',15)
			
	can.save()

	packet.seek(0)

	contentPage = PdfReader(packet)
	writer.add_page(contentPage.pages[0])

	pn = 0
	x = 795
	for i in range(len(allContent)):
		annotation = AnnotationBuilder.link(
				rect = (0,x,525,x+15),
				target_page_index = list(allContent.values())[i] + ceil(len(allContent)/37) - 1
				)
		x -= 20 
		writer.add_annotation(page_number=pn, annotation=annotation)
		if i == 36:
			x = 795
			pn += 1

	if contentNum == 0:	
		writer.append_pages_from_reader(reader) 
	elif contentNum > 0:
		for i in range(contentNum,len(reader.pages)):
			writer.add_page(reader.pages[i])

def saveFile(saveF):
	newFileName = input("New file Name : ") or "new file.pdf"
	with open(newFileName, 'wb') as file:
		saveF.write(file)
	
def getContentPage(contentNum):
	allContent = dict()
	for p in range(contentNum):
		page = reader.pages[p]
		ac = page.extract_text().split("\n")
		ac.pop(-1)
		for i in ac:
			i = i.split(" : ")
			allContent[i[1]] = int(i[0])
		
	return allContent

def editContent(allContent):
	for i in allContent:
		print(f"{allContent[i]} : {i}")
	loop = True
	while loop:
		topic = input("topic : ")
		if topic == "finish":
			loop = not loop
		elif topic == "del":
			delete = input("Delete content page : ")
			try: 
				del allContent[delete]
			except:
				print("Page number not found")
		else:
			page = input("page : ")
			allContent[topic] = int(page)
	
		for i in allContent:
			print(f"{allContent[i]} : {i}")
	allContent = dict(sorted(allContent.items(), key=lambda x:x[1]))
	return allContent

def mergeFile():
	mergeList = []
	loop = True
	merger = PdfMerger()

	while loop:
		mergeName = input("Merge file name : ")
		if mergeName == "del":
			mergeList = []
		elif mergeName == "finish":
			loop = not loop
		for i in mergeList:
			print(i)

	for f in mergeList:
		try:
			merger.append(PdfReader(open(f,'rb')))
		except:
			print(f"{f} not found")

	return merger

def saveContentToFile(allContent):
	saveFileName = input("Save file name : ") or "Content list.txt"
	with open(saveFileName, 'w') as file:
		file.write(json.dumps(allContent))

def openContentFile(fn):
	with open(fn) as file:
		dataContent = json.loads(file.read())

	return dataContent

if __name__ == "__main__":
	func = input("1. Add content page\n2. Change content page\n3. Merge file\n4. Save content from file\n>> ")
	if func == "1":
		fileName = input("File name : ").strip()
		openFile(fileName)
		allContent = getNewContent()
		writeFile(fileName, allContent)
		saveFile(writer)
	elif func == "2":
		fileName = input("File name : ").strip()
		openFile(fileName)
		contentNum = int(input("Content page number : "))
		option = input("from (old content) / (txt) : ")
	
		if option == "old content":
			allContent = getContentPage(contentNum)
		elif option == "txt":
			fn = input("Content txt file name : ")
			allContent = openContentFile(fn)
			print(allContent)
		allContent = editContent(allContent)
		writeFile(fileName, allContent, contentNum)
		saveFile(writer)
	elif func == "3":
		merger = mergeFile()
		saveFile(merger)
	elif func == "4":
		fileName = input("File name : ").strip()
		openFile(fileName)
		contentNum = int(input("Content page number : "))
		allContent = getContentPage(contentNum)
		saveContentToFile(allContent)	
