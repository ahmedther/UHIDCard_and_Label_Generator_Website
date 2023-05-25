from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
from .support import Support as sup
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


@csrf_exempt
def index(request):
    context = {
        "header_text": "Welcome to UHID Printer ( Without Logo )",
        "button_text": "UHID",
    }

    if request.method == "GET":
        return render(request, "UHID_Printer_App/index.html", context)

    elif request.method == "POST":
        # Create a file-like buffer to receive PDF data.

        # assign uhid from user input
        uhid = (request.POST["uhid"]).upper()
        # Validate UHID
        sup.uhid_validate(uhid, request)

        # search and get data from the database
        patient_details = sup.search_uhid_in_database(uhid)
        if not patient_details:
            context["error"] = f"This UHID ({uhid}) doesn" "t exist in the database.\n"
            return render(request, "UHID_Printer_App/index.html", context)

        # change the value M to Male and F to Female
        patient_name, gender, uhid = sup.male_female_working(patient_details)

        # generate a pdf and get its path
        pdf_file_path = sup.generate_uhid_without_logo(patient_name, gender, uhid)

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")

        # Other Workings for Future Reference

        # file_location = "UHID_Printer_App\pdf\\" + patient_details[0] + ".pdf"
        # file_location = (
        #     "/home/ahmed/Desktop/AHMED/Django_Websites/UHID_Printer_Web/UHID_Printer_Web/pdf/"
        #     + patient_details[0]
        #     + ".pdf"
        # )
        # sys.stderr.write(file_location)
        # file_location = "sample.pdf"
        # file = "aa.pdf"

        # filepath = os.path.join('pdf', 'sample.pdf')
        # a = os.path.dirname(os.path.abspath(__file__))
        # b = os.path.abspath(os.getcwd())
        # sys.stderr.write(a)
        # sys.stderr.write(b)

        # return FileResponse(buffer, as_attachment=True, filename=file)

        # try:
        #         with codecs.open(file_location, 'r', encoding='utf-8',
        #         errors='ignore') as f:
        #                 file_data = f.read()

        #     # sending response
        #                 response = HttpResponse(file_data, content_type='application/pdf')
        #                 response['Content-Disposition'] = 'attachment; filename="UHID_Printer_App\pdf\\" + {patient_details[0]} + ".pdf"'

        # except IOError:
        #     # handle file not exist case here
        #         response = HttpResponseNotFound('<h1>File not exist</h1>')

        #         return response
        #         return render(request,'UHID_Printer_App/index.html',)


@csrf_exempt
def indore(request):
    context = {
        "header_text": "Welcome to UHID Printer With Logo (Indore)",
        "button_text": "UHID",
    }

    if request.method == "GET":
        return render(request, "UHID_Printer_App/index.html", context)

    elif request.method == "POST":
        # Create a file-like buffer to receive PDF data.

        # assign uhid from user input
        uhid = (request.POST["uhid"]).upper()

        # Show error if uhid is less the 12 characters
        sup.uhid_validate(uhid, request)

        # search and get data from the database
        patient_details = sup.search_uhid_in_database(uhid)
        if not patient_details:
            context["error"] = f"This UHID ({uhid}) doesn" "t exist in the database.\n"
            return render(request, "UHID_Printer_App/index.html", context)

        # change the value M to Male and F to Female
        patient_name, gender, uhid = sup.male_female_working(patient_details)

        # generate a pdf and get its path
        pdf_file_path = sup.generate_uhid_with_logo(
            patient_name, gender, uhid, "indore"
        )

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")


@csrf_exempt
def mumbai(request):
    context = {
        "header_text": "Welcome to UHID Printer With Logo (Mumbai)",
        "button_text": "UHID",
    }

    if request.method == "GET":
        return render(request, "UHID_Printer_App/index.html", context)

    elif request.method == "POST":
        # Create a file-like buffer to receive PDF data.

        # assign uhid from user input
        uhid = (request.POST["uhid"]).upper()

        # Show error if uhid is less the 12 characters
        sup.uhid_validate(uhid, request)

        # search and get data from the database
        patient_details = sup.search_uhid_in_database(uhid)
        if not patient_details:
            context["error"] = f"This UHID ({uhid}) doesn" "t exist in the database.\n"
            return render(request, "UHID_Printer_App/index.html", context)

        # change the value M to Male and F to Female
        patient_name, gender, uhid = sup.male_female_working(patient_details)

        # generate a pdf and get its path
        pdf_file_path = sup.generate_uhid_with_logo(
            patient_name, gender, uhid, "mumbai"
        )

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")


@csrf_exempt
def ip_label(request):
    context = {
        "header_text": "Welcome to IP Label Printer",
        "button_text": "IP Label",
    }

    if request.method == "GET":
        return render(request, "UHID_Printer_App/index.html", context)

    elif request.method == "POST":
        # Create a file-like buffer to receive PDF data.

        # assign uhid from user input
        uhid = (request.POST["uhid"]).upper()

        # Show error if uhid is less the 12 characters
        sup.uhid_validate(uhid, request)

        # search and get data from the database
        patient_details = sup.search_uhid_for_label(uhid, "IP")
        if not patient_details:
            context[
                "error"
            ] = f"This Patient with UHID ({uhid}) might not be admitted currently.\n"
            return render(request, "UHID_Printer_App/index.html", context)

        # generate a pdf and get its path
        pdf_file_path = sup.generate_label(patient_details)

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")


@csrf_exempt
def op_label(request):
    context = {
        "header_text": "Welcome to OP Label Printer",
        "button_text": "OP Label",
    }

    if request.method == "GET":
        return render(request, "UHID_Printer_App/index.html", context)

    elif request.method == "POST":
        # Create a file-like buffer to receive PDF data.

        # assign uhid from user input
        uhid = (request.POST["uhid"]).upper()

        # Show error if uhid is less the 12 characters
        sup.uhid_validate(uhid, request)

        # search and get data from the database
        patient_details = sup.search_uhid_for_label(uhid, "OP")
        if not patient_details:
            context[
                "error"
            ] = f"This Patient with UHID ({uhid}) doesn't have an open encounter.\n"
            return render(request, "UHID_Printer_App/index.html", context)

        # generate a pdf and get its path
        pdf_file_path = sup.generate_label(patient_details)

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")


@csrf_exempt
def both_label(request):
    context = {
        "header_text": "Welcome to All Encounter Label Printer",
        "button_text": "ALL Labels",
    }

    if request.method == "GET":
        return render(request, "UHID_Printer_App/index.html", context)

    elif request.method == "POST":
        # Create a file-like buffer to receive PDF data.

        # assign uhid from user input
        uhid = (request.POST["uhid"]).upper()

        # Show error if uhid is less the 12 characters
        sup.uhid_validate(uhid, request)

        # search and get data from the database
        patient_details = sup.search_uhid_for_label(uhid, "BOTH")
        if not patient_details:
            context[
                "error"
            ] = f"This Patient with UHID ({uhid}) did'nt avail our services.\n"
            return render(request, "UHID_Printer_App/index.html", context)

        # generate a pdf and get its path
        pdf_file_path = sup.generate_label(patient_details)

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")


@csrf_exempt
def lebel_with_spec(request):
    context = {
        "header_text": "Welcome to Label With Specimen Printer ",
        "button_text": "Labels",
    }

    if request.method == "GET":
        return render(request, "UHID_Printer_App/index.html", context)

    elif request.method == "POST":
        # Create a file-like buffer to receive PDF data.

        # assign uhid from user input
        uhid = (request.POST["uhid"]).upper()

        # Show error if uhid is less the 12 characters
        sup.uhid_validate(uhid, request)

        # search and get data from the database
        patient_details = sup.search_uhid_for_label(uhid)
        if not patient_details:
            context[
                "error"
            ] = f"This Patient with UHID ({uhid}) did'nt avail our services.\n"
            return render(request, "UHID_Printer_App/index.html", context)

        # generate a pdf and get its path
        pdf_file_path = sup.generate_label_with_specimen(patient_details)

        return FileResponse(open(pdf_file_path, "rb"), content_type="application/pdf")
