from reportlab.lib.units import mm
from reportlab.graphics.barcode import code39
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import sys
from reportlab.graphics.barcode import code39, code128, code93
from reportlab.graphics.barcode import eanbc, qr, usps
from reportlab.graphics.shapes import Drawing 
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF



class GenerateUHIDCard:
    
    
    def __init__(self,filename="Card.pdf", uhid="uhid",patient_name = "patient_name",gender ="gender"):
        """
        @param date: The date to use
        @param amount: The amount owed
        @param receiver: The person who received the amount owed
        """
        
        self.my_canvas = SimpleDocTemplate(filename, pagesize=(100*mm,54*mm),rightMargin=1, leftMargin=20,topMargin=45,bottomMargin=1)

        flowables = []
        
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Light", "BOOKOS.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Italic", "BBOOKOSI.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Bold Italic", "BOOKOSBI.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Bold", "BOOKOSB.TTF"))
        
        pdfmetrics.registerFontFamily("Bookman Old Style",normal="Bookman Old Style,",bold="Bookman Old Style Bold", italic="Bookman Old Style Italic", boldItalic="Bookman Old Style Bold Italic" )
        pdfmetrics.registerFont(TTFont('Bookman Old Style','BOOKOSB.TTF'))
        

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='card',
                                  fontName="Bookman Old Style Bold",
                                  fontSize=11,
                                  leading=8))
        styles.add(ParagraphStyle(name ="times",
                                  fontName="Bookman Old Style Bold",
                                  fontSize = 12,
                                  leading = 10))

       
        flowables.append(Paragraph(patient_name,styles["card"]))
        flowables.append(Spacer(1, 8))
        
        flowables.append(Paragraph(gender,styles["card"]))
        flowables.append(Spacer(1, 8))

        flowables.append(Paragraph(uhid,styles["card"]))
        flowables.append(Spacer(1, 8))

       
        self.my_canvas.build(flowables)

        #self.my_canvas.drawString(0, 10, data[0])
    
          
def createBarCodes():

        c = canvas.Canvas("barcodes.pdf", pagesize=letter)

        barcode_value = "1234567890"

        barcode39 = code39.Extended39(barcode_value)
        barcode39Std = code39.Standard39(barcode_value, barHeight=20, stop=1)

        # # code93 also has an Extended and MultiWidth version
        barcode93 = code93.Standard93(barcode_value)

        barcode128 = code128.Code128(barcode_value)
        # # the multiwidth barcode appears to be broken 
        barcode128Multi = code128.MultiWidthBarcode(barcode_value)

        barcode_usps = usps.POSTNET("50158-9999")

        codes = [barcode39, barcode39Std, barcode93, barcode128, barcode_usps]

        x = 1 * mm
        y = 285 * mm
        x1 = 6.4 * mm

        for code in codes:
            code.drawOn(c, x, y)
            y = y - 15 * mm


    


        c.save()
    
if __name__ == "__main__":
    createBarCodes()


if __name__ == '__main__':

    GenerateUHIDCard()

    
    # GenLabel('form.pdf', str(ct),
    # '$1,999', 'Mike')
