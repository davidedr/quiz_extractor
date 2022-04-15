from fpdf import FPDF

IMAGES_SUBFOLDER = "images"

class PDF(FPDF):

    def plot(self):
      filename = f'{IMAGES_SUBFOLDER}/{str(13)}.jpeg'
      question_image = open(filename, 'rb').read()

      self.set_xy(40.0,25.0)
      self.image(filename,  link = '', type = '', w = 150/5, h = 130/5)
 
pdf = PDF(orientation = 'P', unit = 'mm', format = 'A4')
pdf.add_page()

pdf_w = 210
pdf_h = 297

pdf.plot()
pdf.output('test.pdf','F')