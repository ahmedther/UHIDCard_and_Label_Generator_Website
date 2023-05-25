from reportlab.lib.units import mm
from reportlab.graphics.barcode import code39, code128
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import platform
import sys
from pathlib import Path
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib import fonts

def name_capitalization_and_limiting(patient_name):
    # limit Name and Capitalize Each words
    split_pat_name = patient_name.replace(".", " ").split()
    new_name = ""
    for name in split_pat_name:
        new_name = new_name + name.capitalize() + " "
    if len(new_name) > 40:
        new_name = new_name[0:40]

    if len(new_name) < 20:
        new_name = new_name + "      "

    return new_name


def shorten_dr_name(dr_name):
    if len(dr_name) > 20:
        dr_name = dr_name[0:20]
    return dr_name


class GenerateUHIDCard:
    def __init__(
        self,
        filename="Card.pdf",
        uhid="uhid",
        patient_name="patient_name",
        gender="gender",
    ):
        self.filename = filename
        self.uhid = uhid
        self.patient_name = patient_name
        self.gender = gender
        """
        @param date: The date to use
        @param amount: The amount owed
        @param receiver: The person who received the amount owed
        """

        # Variable to add in cavanas after collecting data from different source
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Light", "BOOKOS.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Italic", "BBOOKOSI.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Bold Italic", "BOOKOSBI.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Bold", "BOOKOSB.TTF"))

        # Defining Fonts
        pdfmetrics.registerFontFamily(
            "Bookman Old Style",
            normal="Bookman Old Style,",
            bold="Bookman Old Style Bold",
            italic="Bookman Old Style Italic",
            boldItalic="Bookman Old Style Bold Italic",
        )
        pdfmetrics.registerFont(TTFont("Bookman Old Style", "BOOKOSB.TTF"))

        # Defining Styles
        self.styles = getSampleStyleSheet()
        self.styles.add(
            ParagraphStyle(
                name="card", fontName="Bookman Old Style Bold", fontSize=11, leading=8
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="times", fontName="Bookman Old Style Bold", fontSize=12, leading=10
            )
        )

        # Defining barcode
        self.bar_code = code128.Code128(uhid, barWidth=1, barHeight=20)

    def without_logo(self):
        # Define Canvas
        my_canvas = SimpleDocTemplate(
            self.filename,
            pagesize=(100 * mm, 54 * mm),
            rightMargin=1,
            leftMargin=20,
            topMargin=45,
            bottomMargin=1,
        )

        # List of Items to Display
        flowables = []

        # Adding it all Together
        flowables.append(Paragraph(self.patient_name, self.styles["card"]))
        flowables.append(Spacer(1, 8))

        flowables.append(Paragraph(self.gender, self.styles["card"]))
        flowables.append(Spacer(1, 8))

        flowables.append(Paragraph(self.uhid, self.styles["card"]))
        flowables.append(Spacer(1, 18))

        flowables.append(self.bar_code)
        flowables.append(Spacer(1, 8))
        flowables.append(PageBreak())
        my_canvas.build(flowables)

        # self.my_canvas.drawString(0, 10, data[0])

    def with_logo(self, location):
        wl_canvas = SimpleDocTemplate(
            self.filename,
            pagesize=(100 * mm, 54 * mm),
            rightMargin=-6,
            leftMargin=20,
            topMargin=0,
            bottomMargin=-6,
        )

        self.styles.add(
            ParagraphStyle(
                name="footer",
                fontName="Bookman Old Style Bold",
                fontSize=12,
                leading=22,
                backColor="#1A237E",
                textColor="#FAFAFA",
                leftIndent=-26,
                rightIndent=-6,
                alignment=1,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="spacer",
                fontName="Bookman Old Style Bold",
                fontSize=2,
                leading=4,
                backColor="#1A237E",
                textColor="#FAFAFA",
                leftIndent=-26,
                rightIndent=-6,
                alignment=1,
            )
        )
        # List of Items to Display
        flowables = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        curret_path = Path(current_dir)
        if location.lower() == "mumbai":
            system_os = platform.system()
            if system_os == "Linux":
                logo_path = f"{curret_path}/static/UHID_Printer_App/logo.jpg"
            else:
                logo_path = f"{curret_path}\\static\\UHID_Printer_App\\logo.jpg"

        if location.lower() == "indore":
            system_os = platform.system()
            if system_os == "Linux":
                logo_path = f"{curret_path}/static/UHID_Printer_App/logo_indore.png"
            else:
                logo_path = f"{curret_path}\\static\\UHID_Printer_App\\logo_indore.png"

        # logo = f"""

        #         <img src="{logo_path}" style="width: 30px; height: 30px;"></img>

        #         """

        flowables.append(Image(logo_path, width=150, height=40, hAlign="LEFT"))
        flowables.append(Spacer(1, 8))

        flowables.append(Paragraph(self.patient_name, self.styles["card"]))
        flowables.append(Spacer(1, 8))

        flowables.append(Paragraph(self.gender, self.styles["card"]))
        flowables.append(Spacer(1, 8))

        flowables.append(Paragraph(self.uhid, self.styles["card"]))
        flowables.append(Spacer(1, 10))

        flowables.append(self.bar_code)
        flowables.append(Spacer(1, 3))
        flowables.append(Paragraph(f" ", self.styles["spacer"]))
        flowables.append(Paragraph(f"Patient Registration Card", self.styles["footer"]))
        flowables.append(PageBreak())
        wl_canvas.build(flowables)
        

class GenerateLabel:
    def __init__(self, filename, patient_details):
        """
        @param date: The date to use
        @param amount: The amount owed
        @param receiver: The person who received the amount owed
        """

        # Variable to add in cavanas after collecting data from different source
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Light", "BOOKOS.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Italic", "BBOOKOSI.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Bold Italic", "BOOKOSBI.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Bold", "BOOKOSB.TTF"))

        # Defining Fonts
        pdfmetrics.registerFontFamily(
            "Bookman Old Style",
            normal="Bookman Old Style,",
            bold="Bookman Old Style Bold",
            italic="Bookman Old Style Italic",
            boldItalic="Bookman Old Style Bold Italic",
        )
        pdfmetrics.registerFont(TTFont("Bookman Old Style", "BOOKOSB.TTF"))

        # Defining Styles
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="label", fontName="Bookman Old Style Bold", fontSize=11, leading=5
            )
        )
        styles.add(
            ParagraphStyle(
                name="name",
                fontName="Bookman Old Style Bold",
                fontSize=11,
                leading=11,
            )
        )

        label_canvas = SimpleDocTemplate(
            filename,
            pagesize=(50 * mm, 30 * mm),
            rightMargin=0,
            leftMargin=1,
            topMargin=-5,
            bottomMargin=0,
        )

        # List of Items to Display
        flowables = []

        for pat in patient_details:
            patient_name = name_capitalization_and_limiting(pat[1])
            dr_name = name_capitalization_and_limiting(pat[4])
            dr_name = shorten_dr_name(dr_name)
            # Defining barcode
            bar_code = code128.Code128(pat[0], barWidth=0.9, barHeight=10)

            flowables.append(Paragraph(pat[0], styles["label"]))
            flowables.append(Spacer(1, 7))

            flowables.append(Paragraph(patient_name, styles["name"]))
            flowables.append(Spacer(1, 7))

            flowables.append(Paragraph(pat[2] + "       " + pat[3], styles["label"]))
            flowables.append(Spacer(1, 7))

            flowables.append(Paragraph(dr_name, styles["label"]))
            flowables.append(Spacer(1, 9))

            flowables.append(bar_code)
            flowables.append(PageBreak())
        label_canvas.build(flowables)


class GenerateLabelWithSpecimen:
    def __init__(self, filename, patient_details):
        """
        @param date: The date to use
        @param amount: The amount owed
        @param receiver: The person who received the amount owed
        """

        # Variable to add in cavanas after collecting data from different source
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Light", "BOOKOS.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Italic", "BBOOKOSI.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Bold Italic", "BOOKOSBI.TTF"))
        # pdfmetrics.registerFont(TTFont("Bookman Old Style Bold", "BOOKOSB.TTF"))

        # Defining Fonts
        # pdfmetrics.registerFontFamily(
        #     "Bookman Old Style",
        #     normal="Bookman Old Style,",
        #     bold="Bookman Old Style Bold",
        #     italic="Bookman Old Style Italic",
        #     boldItalic="Bookman Old Style Bold Italic",
        # )
        # pdfmetrics.registerFont(TTFont("Bookman Old Style", "BOOKOSB.TTF"))

        # # Defining Styles
        # styles = getSampleStyleSheet()
        # styles.add(
        #     ParagraphStyle(
        #         name="label", fontName="Bookman Old Style Bold", fontSize=8, leading=0
        #     )
        # )
        # styles.add(
        #     ParagraphStyle(
        #         name="name",
        #         fontName="Bookman Old Style Bold",
        #         fontSize=11,
        #         leading=11,
        #     )
        # )
        styles = getSampleStyleSheet()
        styles['Normal'].fontSize = 8
        label_canvas = SimpleDocTemplate(
            filename,
            pagesize=(50 * mm, 30 * mm),
            rightMargin=0,
            leftMargin=1,
            topMargin=-5,
            bottomMargin=-5,
        )

        # List of Items to Display
        flowables = []

        for pat in patient_details:
            patient_name = name_capitalization_and_limiting(pat[1])
            dr_name = name_capitalization_and_limiting(pat[4])
            dr_name = shorten_dr_name(dr_name)
            # Defining barcode
            bar_code = code128.Code128(pat[7], barWidth=1.2, barHeight=20)

            flowables.append(Paragraph(f"KDAH Ro   {pat[0]}",styles['Normal']))
            flowables.append(Spacer(0, -2))

            flowables.append(bar_code)
            flowables.append(Spacer(0, 0))
            flowables.append(Paragraph(str(pat[7]),styles['Normal']))
            flowables.append(Spacer(0, -3))

            flowables.append(Paragraph(f"<b>{patient_name}</b>",styles['Normal']))
            flowables.append(Spacer(0, -3))

            flowables.append(Paragraph(pat[2] + "    " + pat[3] + f"    {pat[6].strftime('%d-%b-%Y')}",styles['Normal']))
            flowables.append(Spacer(0, -3))

            flowables.append(Paragraph(f"{pat[8]}",styles['Normal']))
            flowables.append(Spacer(0, -3))
            flowables.append(Paragraph(f"{pat[5]}",styles['Normal']))
            flowables.append(Spacer(0, -3))
            flowables.append(PageBreak())

        label_canvas.build(flowables)


if __name__ == "__main__":
    GenerateUHIDCard()

    # GenLabel('form.pdf', str(ct),
    # '$1,999', 'Mike')
