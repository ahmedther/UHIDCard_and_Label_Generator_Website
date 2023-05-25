from django.shortcuts import render
from .oracle_config import Ora
from .card_generator import GenerateUHIDCard, GenerateLabel, GenerateLabelWithSpecimen
import os
from pathlib import Path


class Support:
    def uhid_validate(uhid, request):
        # Show error if uhid is less the 12 characters
        if len(uhid) < 12:
            return render(
                request, "UHID_Printer_App/index.html", {"error": "UHID Incomplete."}
            )

    def search_uhid_in_database(uhid):
        # search and get data from the database
        patient_details = []
        db = Ora()
        patient_details = db.get_patient_details(uhid)
        # Data to send on website
        if patient_details:
            return patient_details

    def search_uhid_for_label(uhid, encounter_type):
        db = Ora()
        if encounter_type == "IP":
            patient_details = db.get_patient_details_for_label_ip(uhid)

        if encounter_type == "OP":
            patient_details = db.get_patient_details_for_label_op(uhid)

        if encounter_type == "BOTH":
            patient_details = db.get_patient_details_for_label_both(uhid)

        # Data to send on website
        if patient_details:
            return patient_details

    def male_female_working(patient_details):
        # get the first element fro the recived query
        patient_details = list(patient_details[0])

        # limit Name and Capitalize Each words
        split_pat_name = patient_details[1].split()
        new_name = ""
        for name in split_pat_name:
            new_name = new_name + name.capitalize() + " "

        if len(new_name) > 31:
            new_name = new_name[0:31]

        # Filter data as per Printing Requirements for MAle and Female
        patient_name = "Name    :  " + new_name
        gender = ""
        if patient_details[2] == "M":
            gender = "Sex       :  Male"

        elif patient_details[2] == "F":
            gender = "Sex       :  Female"

        uhid = "UHID    :  " + patient_details[0]
        return patient_name, gender, uhid

    def generate_uhid_without_logo(patient_name, gender, uhid):
        # Generate PDF file with barcode
        current_dir = os.path.dirname(os.path.abspath(__file__))
        curret_path = Path(current_dir)
        parent_path = curret_path.parent

        pdf_file_path = f"{parent_path}/pdf/without_logo.pdf"

        guc = GenerateUHIDCard(
            filename=pdf_file_path, patient_name=patient_name, gender=gender, uhid=uhid
        )
        guc.without_logo()
        return pdf_file_path

    def generate_uhid_with_logo(patient_name, gender, uhid, location):
        # Generate PDF file with barcode
        current_dir = os.path.dirname(os.path.abspath(__file__))
        curret_path = Path(current_dir)
        parent_path = curret_path.parent

        pdf_file_path = f"{parent_path}/pdf/with_logo.pdf"

        guc = GenerateUHIDCard(
            filename=pdf_file_path, patient_name=patient_name, gender=gender, uhid=uhid
        )
        guc.with_logo(location)

        return pdf_file_path

    def name_capitalization_and_limiting(patient_name):
        # limit Name and Capitalize Each words
        split_pat_name = patient_name.split()
        new_name = ""
        for name in split_pat_name:
            new_name = new_name + name.capitalize() + " "
            # if len(new_name) > 31:
        #     new_name = new_name[0:31]

        return new_name

    def generate_label(patient_details):
        # Generate PDF file with barcode
        current_dir = os.path.dirname(os.path.abspath(__file__))
        curret_path = Path(current_dir)
        parent_path = curret_path.parent

        pdf_file_path = f"{parent_path}/pdf/ip_labl.pdf"

        GenerateLabel(pdf_file_path, patient_details)
        return pdf_file_path

    def generate_label_with_specimen(patient_details):
        # Generate PDF file with barcode
        current_dir = os.path.dirname(os.path.abspath(__file__))
        curret_path = Path(current_dir)
        parent_path = curret_path.parent

        pdf_file_path = f"{parent_path}/pdf/label_with_specimen.pdf"

        GenerateLabelWithSpecimen(pdf_file_path, patient_details)
        return pdf_file_path

    def search_uhid_for_label(uhid):
        db = Ora()
        patient_details = db.get_patient_details_for_label_with_specimen(uhid)
        # Data to send on website
        if patient_details:
            return patient_details

    # def uhid_card_print_response(request):
    #     # Create a file-like buffer to receive PDF data.

    #     # assign uhid from user input
    #     uhid = (request.POST["uhid"]).upper()
    #     # Show error if uhid is less the 12 characters

    #     # search and get data from the database
    #     patient_details = []
    #     db = Ora()
    #     patient_details = db.get_patient_details(uhid)
    #     # Data to send on website
    #     if not patient_details:
    #         return render(
    #             request,
    #             "UHID_Printer_App/index.html",
    #             {"error": f"This UHID ({uhid}) doesn" "t exist in the database.\n"},
    #         )

    #     patient_details = list(patient_details[0])

    #     # Filter data as per Printing Requirements for MAle and Female
    #     patient_name = "Name    :  " + patient_details[1]
    #     gender = ""
    #     if patient_details[2] == "M":
    #         gender = "Sex       :  Male"

    #     elif patient_details[2] == "F":
    #         gender = "Sex       :  Female"

    #     uhid = "UHID    :  " + patient_details[0]

    #     # file_location = "UHID_Printer_App\pdf\\" + patient_details[0] + ".pdf"
    #     # file_location = (
    #     #     "/home/ahmed/Desktop/AHMED/Django_Websites/UHID_Printer_Web/UHID_Printer_Web/pdf/"
    #     #     + patient_details[0]
    #     #     + ".pdf"
    #     # )
    #     # sys.stderr.write(file_location)
    #     # file_location = "sample.pdf"
    #     # file = "aa.pdf"

    #     # Generate PDF file with barcode
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     curret_path = Path(current_dir)
    #     parent_path = curret_path.parent

    #     pdf_file_path = f"{parent_path}/pdf/sample.pdf"

    #     GenerateUHIDCard(
    #         filename=pdf_file_path, patient_name=patient_name, gender=gender, uhid=uhid
    #     )
    #     # filepath = os.path.join('pdf', 'sample.pdf')
    #     # a = os.path.dirname(os.path.abspath(__file__))
    #     # b = os.path.abspath(os.getcwd())
    #     # sys.stderr.write(a)
    #     # sys.stderr.write(b)

    #     return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")

    #     # return FileResponse(buffer, as_attachment=True, filename=file)

    #     # try:
    #     #         with codecs.open(file_location, 'r', encoding='utf-8',
    #     #         errors='ignore') as f:
    #     #                 file_data = f.read()

    #     #     # sending response
    #     #                 response = HttpResponse(file_data, content_type='application/pdf')
    #     #                 response['Content-Disposition'] = 'attachment; filename="UHID_Printer_App\pdf\\" + {patient_details[0]} + ".pdf"'

    #     # except IOError:
    #     #     # handle file not exist case here
    #     #         response = HttpResponseNotFound('<h1>File not exist</h1>')

    #     #         return response
    #     #         return render(request,'UHID_Printer_App/index.html',)
