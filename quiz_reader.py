import PyPDF2
pdfFileObj = open("J:\\temp\\LISTA CP QUIZ BASE (Patenti entro-oltre 12 miglia) - Aggiornamento 14.04.2016.pdf", "rb")
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
print(pdfReader.numPages)
page=pdfReader.getPage(0)
pdfReader.getPage(0).extractText()


