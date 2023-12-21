from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.generic import RectangleObject, AnnotationBuilder
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
			allContent.pop(-1)
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

	x = 795
	pn = 0
	for i in allContent.values():
		if x < 75:
			x = 795
			pn += 1

		annotation = AnnotationBuilder.link(
			rect = (0,x,525,x+15),
			target_page_index = i
		)
		x -= 20 
		writer.add_annotation(page_number=pn, annotation=annotation)
	if contentNum == 0:	
		writer.append_pages_from_reader(reader) 
	elif contentNum > 0:
		for i in range(contentNum,len(reader.pages)):
			writer.add_page(reader.pages[i])

def saveFile():
	newFileName = input("New file Name : ").strip() + '.pdf'
	with open(newFileName, 'wb') as file:
		writer.write(file)
	
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

if __name__ == "__main__":
	fileName = input("File name : ").strip()
	openFile(fileName)
	func = input("1. Add content page\n2.Change content page\n>> ")
	if func == "1":
		allContent = getNewContent()
		writeFile(fileName, allContent)
		saveFile()
	elif func == "2":
		contentNum = int(input("Content page number : "))
		allContent = getContentPage(contentNum)
		allContent = editContent(allContent)
		writeFile(fileName, allContent, contentNum)
		saveFile()
