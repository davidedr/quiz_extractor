import aspose.words as aw

doc = aw.Document()
builder = aw.DocumentBuilder(doc)
builder.write("Hello world!")
doc.save("out.docx")