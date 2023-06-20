from django.shortcuts import render
import csv
import datetime
import os
import random

import appointment_booking as apb
from Graph import Graph
import queueds as QueueDS
import send_email
from Stack import Stack
from DynamicArray import List
from HashMap import HashMap


QUEUE_DIA = QueueDS.Queue(5)
QUEUE_ENDO = QueueDS.Queue(5)
QUEUE_GASTRO = QueueDS.Queue(5)
QUEUE_GP = QueueDS.Queue(5)
QUEUE_IMMUNO = QueueDS.Queue(5)
QUEUE_NEURO = QueueDS.Queue(5)
QUEUE_ORTHO = QueueDS.Queue(5)
QUEUE_PSYCH = QueueDS.Queue(5)
QUEUE_PULMO = QueueDS.Queue(5)
QUEUE_URO = QueueDS.Queue(5)

QUEUES = [
    QUEUE_DIA,
    QUEUE_ENDO,
    QUEUE_GASTRO,
    QUEUE_GP,
    QUEUE_IMMUNO,
    QUEUE_NEURO,
    QUEUE_ORTHO,
    QUEUE_PSYCH,
    QUEUE_PULMO,
    QUEUE_URO,
]

slot_dict = HashMap()
slot_dict.put("slot1", "09:00-09:30")
slot_dict.put("slot2", "09:30-10:00")
slot_dict.put("slot3", "10:00-10:30")
slot_dict.put("slot4", "10:30-11:00")
slot_dict.put("slot5", "11:00-11:30")
slot_dict.put("slot6", "13:30-14:00")
slot_dict.put("slot7", "14:00-14:30")
slot_dict.put("slot8", "14:30-15:00")
slot_dict.put("slot9", "15:00-15:30")
slot_dict.put("slot10", "15:30-16:00")
slot_dict.put("slot11", "16:00-16:30")
slot_dict.put("slot12", "16:30-17:00")

lbl_slot_dict = HashMap()

lbl_slot_dict.put("09:00-09:30", "lblslot1")
lbl_slot_dict.put("09:30-10:00", "lblslot2")
lbl_slot_dict.put("10:00-10:30", "lblslot3")
lbl_slot_dict.put("10:30-11:00", "lblslot4")
lbl_slot_dict.put("11:00-11:30", "lblslot5")
lbl_slot_dict.put("13:30-14:00", "lblslot6")
lbl_slot_dict.put("14:00-14:30", "lblslot7")
lbl_slot_dict.put("14:30-15:00", "lblslot8")
lbl_slot_dict.put("15:00-15:30", "lblslot9")
lbl_slot_dict.put("15:30-16:00", "lblslot10")
lbl_slot_dict.put("16:00-16:30", "lblslot11")
lbl_slot_dict.put("16:30-17:00", "lblslot12")


def home(request):
    return render(request, "index.html")


def new_page_view(request):
    return render(request, "register.html")


def login(request):
    with open("doctors.csv", "a") as f:
        pass
    f.close()

    with open("patients.csv", "a") as f:
        pass
    f.close()

    with open("receptionists.csv", "a") as f:
        pass
    f.close()

    with open("register.csv", "a") as f:
        pass
    f.close()

    with open("transactions.csv", "a") as f:
        pass
    f.close()

    with open("Confirmedappointments.csv", "a") as f:
        pass
    f.close()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        print(username, password)

        # Read the register.csv file
        with open("register.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                print(row)
                stored_username = row[3]
                stored_password = row[4]

                if username == stored_username:
                    if password == stored_password:
                        with open("logs.csv", "a") as logs:
                            write = csv.writer(logs)
                            date_time = datetime.datetime.now()

                            current_time = date_time.time()
                            current_date = date_time.date()

                            write.writerow([username, current_date, current_time])

                        request.session["CURRENT_USER"] = username

                        if row[-2] == "admin":
                            request.session["CURRENT_PRIV"] = "admin"
                            return render(request, "admin_homepage.html")
                        elif row[-2] == "rec":
                            request.session["CURRENT_PRIV"] = "rec"
                            return render(request, "homepage.html")
                        elif row[-2] == "pat":
                            request.session["CURRENT_PRIV"] = "pat"
                            return render(request, "patient_homepage.html")
                        elif row[-2] == "doc":
                            request.session["CURRENT_PRIV"] = "doc"
                            return render(
                                request, "doctor_homepage.html"
                            )  # Redirect to success page after successful login
                    else:
                        return render(
                            request, "index.html", {"alertmessage": "Wrong password"}
                        )  # Display wrong password message

            return render(
                request, "index.html", {"alertmessage": "Username not found"}
            )  # Display username not found message

    return render(request, "index.html")


def newregister(request):
    if request.method == "POST":
        name = request.POST["name"]
        mobile = request.POST["mobile"]
        dob = request.POST["dob"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        address = request.POST["address"].replace(",", "-").replace("\r\n", ";")
        age = request.POST["age"]
        gender = request.POST["gender"]
        blood_group = request.POST["blood-group"]

        if password != confirm_password:
            return render(
                request, "register.html", {"alertmessage": "Passwords do not match."}
            )

        with open("register.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if email == row[3]:
                    return render(
                        request,
                        "register.html",
                        {"alertmessage": "E-mail already exists."},
                    )

            uniqueid_random = str(random.randint(100000, 999999))
            while uniqueid_random in [row[-1] for row in reader]:
                uniqueid_random = str(random.randint(100000, 999999))

        with open("register.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    name,
                    mobile,
                    dob,
                    email,
                    password,
                    address,
                    age,
                    gender,
                    blood_group,
                    "pat",
                    uniqueid_random,
                ]
            )

        with open("patients.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    name,
                    mobile,
                    dob,
                    email,
                    password,
                    address,
                    age,
                    gender,
                    blood_group,
                    "pat",
                    uniqueid_random,
                ]
            )

        with open(f"{uniqueid_random}.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    name,
                    mobile,
                    dob,
                    email,
                    password,
                    address,
                    age,
                    gender,
                    blood_group,
                    "pat",
                    uniqueid_random,
                    "None",
                    "None",
                    "None",
                ]
            )

        return render(
            request,
            "index.html",
            {"alertmessage": "New user registration information stored successfully."},
        )

    return render(request, "register.html")


def get_email(request):
    if request.method == "POST":
        email = request.POST["email"]
        with open("register.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            if email not in [row[3] for row in reader]:
                return render(
                    request, "forgot_password.html", {"message": "Email not found!"}
                )
            else:
                name = ""
                for row in reader:
                    if row[3] == email:
                        name = row[0]
                        break
                request.session["RESET_EMAIL"] = email
                request.session["RANDOM_OTP"] = random.randint(100000, 999999)
                subject = "OTP Verification for Resetting your Password"
                to = email
                content = (
                        """Hello """
                        + str(name)
                        + """, This mail is in response to your request of resetting your clinic account password. 

                                    Please enter or provide the following OTP: """
                        + str(request.session["RANDOM_OTP"])
                        + """

                                    Note that this OTP is valid only for this instance. Requesting another OTP will 
                                    make this OTP invalid. Incase you haven't requested to reset your password, 
                                    contact your xyz. Thank You """
                )

                send_email.send_email(to, subject, content)
                

                return render(request, "validate_otp.html")
    return render(request, "forgot_password.html")


def validate_otp(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        if password != confirm_password:
            return render(
                request,
                "validate_otp.html",
                {"alertmessage": "Passwords do not match!"},
            )
        elif int(otp) != request.session["RANDOM_OTP"]:
            return render(
                request, "validate_otp.html", {"alertmessage": "Incorrect OTP!"}
            )
        else:
            with open("register.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                for idx, row in enumerate(rows):
                    if row[3] == request.session["RESET_EMAIL"]:
                        request.session["RESET_EMAIL"] = ""
                        rows[idx][4] = password
                        break
            csvfile.close()
            with open("register.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
            csvfile.close()
            return render(
                request, "index.html", {"alertmessage": "Reset Password Successful!"}
            )
    else:
        return render(request, "validate_otp.html")


def personal_details(request):
    print(request.session)
    with open("register.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3] == request.session.get("CURRENT_USER"):
                priv = ""
                if row[-2] == "admin":
                    priv = "Administrator"
                    userhome = "admin"
                elif row[-2] == "rec":
                    priv = "Receptionist"
                    userhome = "receptionist"
                elif row[-2] == "pat":
                    priv = "Patient"
                    userhome = "patient"
                elif row[-2] == "doc":
                    priv = "Doctor"
                    userhome = "doctor"

                data = {
                    "uniqueid": row[-1],
                    "name": row[0],
                    "username": row[3],
                    "phone": row[1],
                    "gender": row[7],
                    "bloodgroup": row[8],
                    "dob": row[2],
                    "address": row[5].replace("-", ",").replace(";", "\\n"),
                    "age": row[6],
                    "priv": priv,
                    "userhome": userhome,
                }
                return render(request, "personal_details.html", data)
        return render(request, "personal_details.html")


def admin_home(request):
    return render(request, "admin_homepage.html")


def patient_home(request):
    return render(request, "patient_homepage.html")


def receptionist_home(request):
    return render(request, "homepage.html")


def doctor_home(request):
    return render(request, "doctor_homepage.html")


def receptionist_search_patient(request):
    if request.method == "POST":
        patient_id = request.POST.get("patientid")
        patient_name = request.POST.get("patientname")
        doctor_name = None
        if patient_id:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[-1].strip() == patient_id.strip():
                        current_name = row[0]
                        break
                else:
                    return render(
                        request,
                        "receptionist_search_patient.html",
                        {"alertmessage": "Patient not found!"},
                    )

            temp1 = {}
            temp2 = {}
            with open("Confirmedappointments.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == patient_id:
                        doctor_id = row[1]
                        with open("doctors.csv") as anothercsvfile:
                            anotherreader = csv.reader(anothercsvfile)
                            for anotherrow in anotherreader:
                                if anotherrow[-1] == doctor_id:
                                    doctor_name = anotherrow[0]

                        today = datetime.datetime.today()
                        appointment = row[2]
                        date, month, year = appointment.split("-")
                        appointment_date = datetime.datetime(
                            int(year), int(month), int(date)
                        )
                        if appointment_date > today:
                            temp2[appointment_date - today] = appointment
                        else:
                            temp1[today - appointment_date] = appointment

            last_appointment = temp1.get(min(temp1.keys(), default="EMPTY"))
            upcoming_appointment = temp2.get(min(temp2.keys(), default="EMPTY"))

            with open(f"{patient_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data = {
                        "uniqueid": row[-4],
                        "name": row[0],
                        "phone": row[1],
                        "gender": row[7],
                        "last_appointment": str(last_appointment),
                        "address": row[5].replace("-", ",").replace(";", "\\n"),
                        "upcoming_appointment": str(upcoming_appointment),
                        "doctor_name": str(doctor_name),
                        "blood_group": row[8],
                    }
                    break

            return render(request, "receptionist_view_patient_details.html", data)
        elif patient_name:
            with open("patients.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == patient_name:
                        patient_id = row[-1]
                        break
                else:
                    return render(
                        request,
                        "receptionist_search_patient.html",
                        {"alertmessage": "Patient not found!"},
                    )

            current_name = patient_name

            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[-1].strip() == patient_id.strip():
                        current_name = row[0]

            temp1 = {}
            temp2 = {}
            with open("Confirmedappointments.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == patient_id:
                        doctor_id = row[1]
                        with open("doctors.csv") as anothercsvfile:
                            anotherreader = csv.reader(anothercsvfile)
                            for anotherrow in anotherreader:
                                if anotherrow[-1] == doctor_id:
                                    doctor_name = anotherrow[0]

                        today = datetime.datetime.today()
                        appointment = row[2]
                        date, month, year = appointment.split("-")
                        appointment_date = datetime.datetime(
                            int(year), int(month), int(date)
                        )
                        if appointment_date > today:
                            temp2[appointment_date - today] = appointment
                        else:
                            temp1[today - appointment_date] = appointment
            last_appointment = temp1.get(min(temp1.keys(), default="EMPTY"))
            upcoming_appointment = temp2.get(min(temp2.keys(), default="EMPTY"))

            with open(f"{patient_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data = {
                        "uniqueid": row[-4],
                        "name": row[0],
                        "phone": row[1],
                        "gender": row[7],
                        "last_appointment": str(last_appointment),
                        "address": row[5].replace("-", ",").replace(";", "\\n"),
                        "upcoming_appointment": str(upcoming_appointment),
                        "doctor_name": str(doctor_name),
                        "blood_group": row[8],
                    }
                    break

            return render(request, "receptionist_view_patient_details.html", data)
        else:
            return render(
                request,
                "receptionist_search_patient.html",
                {"alertmessage": "Patient not found!"},
            )

    return render(request, "receptionist_search_patient.html")


def doctor_search_patient(request):
    if request.method == "POST":
        patientid = ""
        patientname = ""
        phonenumber = ""
        gender = ""
        bloodgroup = ""
        address = ""
        dob = ""
        age = ""
        username = ""
        lastappointment = ""
        upcomingappointment = ""
        dentalcarries = ""
        missingtooth = ""
        allergy = ""
        abrasions = ""
        medicaldatas = ""
        appointmentdatas = ""
        lastappointment = None
        upcomingappointment = None

        patientid = request.POST.get("patientid")
        patientname = request.POST.get("patientname")

        with open("patients.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if patientid:
                    if row[-1] == patientid:
                        patientname = row[0]
                        username = row[3]
                        break
                elif patientname:
                    if row[0] == patientname:
                        patientid = row[-1]
                        username = row[3]
                        break
                else:
                    return render(
                        request,
                        "receptionist_book_appointment_search_patient.html",
                        {"alertmessage": "Fill any one field!"},
                    )
            else:
                return render(
                    request,
                    "doctor_search_patient.html",
                    {"alertmessage": "Patient not found!"},
                )

        class MedicalData:
            def __init__(self, examination, prescription, treatment, treatmentadvice):
                self.examination = examination
                self.prescription = prescription
                self.treatment = treatment
                self.treatmentadvice = treatmentadvice

        class AppointmentData:
            def __init__(self, pname, dname, date, timeslot):
                self.patientname = pname
                self.doctorname = dname
                self.date = date
                self.timeslot = timeslot

        temp1 = {}
        temp2 = {}
        with open("Confirmedappointments.csv") as acsvfile:
            areader = csv.reader(acsvfile)
            for arow in areader:
                if arow[0] == patientid:
                    doctor_id = arow[1]
                    with open("doctors.csv") as anothercsvfile:
                        anotherreader = csv.reader(anothercsvfile)
                        for anotherrow in anotherreader:
                            if anotherrow[-1] == doctor_id:
                                doctorname = anotherrow[0]

                    today = datetime.datetime.today()
                    appointment = arow[2]
                    date, month, year = appointment.split("-")
                    appointment_date = datetime.datetime(
                        int(year), int(month), int(date)
                    )
                    if appointment_date > today:
                        temp2[appointment_date - today] = appointment
                    else:
                        temp1[today - appointment_date] = appointment

        lastappointment = temp1.get(min(temp1.keys(), default="EMPTY"))
        upcomingappointment = temp2.get(min(temp2.keys(), default="EMPTY"))

        medicaldatas = []
        appointmentdatas = []

        with open("Confirmedappointments.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == patientid:
                    doctorname = ""
                    with open("doctors.csv") as anothercsvfile:
                        anotherreader = csv.reader(anothercsvfile)
                        for anotherrow in anotherreader:
                            if anotherrow[-1] == row[1]:
                                doctorname = anotherrow[0]
                    appointmentdata = AppointmentData(
                        patientname, doctorname, row[2], row[3]
                    )
                    appointmentdatas.append(appointmentdata)


        with open(f"{patientid}.csv") as csvfile:
            reader = csv.reader(csvfile)
            firstrow = next(reader)

            phonenumber = firstrow[1]
            dob = firstrow[2]
            address = firstrow[5].replace("-", ",").replace(";", "\\n")
            age = firstrow[6]
            gender = firstrow[7]
            bloodgroup = firstrow[8]

            try:
                secondrow = next(reader)
            except StopIteration:
                data = {
                    "uniqueid": patientid,
                    "patientname": patientname,
                    "phonenumber": phonenumber,
                    "gender": gender,
                    "bloodgroup": bloodgroup,
                    "address": address,
                    "dob": dob,
                    "age": age,
                    "username": username,
                    "lastappointment": lastappointment,
                    "upcomingappointment": upcomingappointment,
                    "dentalcarries": dentalcarries,
                    "missingteeth": missingtooth,
                    "allergy": allergy,
                    "abrasions": abrasions,
                    "medicaldatas": medicaldatas,
                    "appointmentdatas": appointmentdatas,
                }

                return render(request, "doctor_view_patient_details.html", data)

            dentalcarries = secondrow[7].replace("-", ",").replace(";", "\\n")
            missingtooth = secondrow[8].replace("-", ",").replace(";", "\\n")
            allergy = secondrow[9].replace("-", ",").replace(";", "\\n")
            abrasions = secondrow[11].replace("-", ",").replace(";", "\\n")


            for row in reader:
                medicaldata = MedicalData(row[0], row[1], row[2], row[3])
                medicaldatas.append(medicaldata)


        data = {
            "uniqueid": patientid,
            "patientname": patientname,
            "phonenumber": phonenumber,
            "gender": gender,
            "bloodgroup": bloodgroup,
            "address": address,
            "dob": dob,
            "age": age,
            "username": username,
            "lastappointment": lastappointment,
            "upcomingappointment": upcomingappointment,
            "dentalcarries": dentalcarries,
            "missingteeth": missingtooth,
            "allergy": allergy,
            "abrasions": abrasions,
            "medicaldatas": medicaldatas,
            "appointmentdatas": appointmentdatas,
        }

        return render(request, "doctor_view_patient_details.html", data)

    return render(request, "doctor_search_patient.html")


def add_patient_details(request):
    if request.method == "POST":
        uniqueid = request.POST.get("unique-id")
        name = request.POST.get("full-name")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        phone = request.POST.get("phone-number")
        address = request.POST.get("address")
        # prescription = request.POST.get("prescription").replace(",", "-").replace(",", "-").replace("\r\n", ";")
        dental_carries = (
            request.POST.get("dental-carries").replace(",", "-").replace("\r\n", ";")
        )
        missing_teeth = (
            request.POST.get("missing-teeth").replace(",", "-").replace("\r\n", ";")
        )
        allergy = request.POST.get("allergy").replace(",", "-").replace("\r\n", ";")
        abrasions = request.POST.get("abrasions").replace(",", "-").replace("\r\n", ";")
        with open(f"{uniqueid}.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    uniqueid,
                    name,
                    age,
                    sex,
                    phone,
                    address,
                    "None",
                    dental_carries,
                    missing_teeth,
                    allergy,
                    "None",
                    abrasions,
                    "None",
                    "None",
                    "None",
                ]
            )
        return render(
            request,
            "doctor_prescription_search_patient.html",
            {"alertmessage": "Details saved successfully!"},
        )

    return render(request, "doctor_add_patient_details.html")


def doctor_prescription_search_patient(request):
    if request.method == "POST":
        patient_id = request.POST.get("patientid")
        patient_name = request.POST.get("patientname")
        current_name = ""
        if patient_id:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[-1].strip() == patient_id.strip():
                        current_name = row[0]
                        break
                else:
                    return render(
                        request,
                        "doctor_prescription_search_patient.html",
                        {"alertmessage": "Patient not found!"},
                    )
            with open(f"{patient_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                basic_details = next(reader)
                uniqueid = basic_details[-4]
                name = basic_details[0]
                age = basic_details[6]
                sex = basic_details[7]
                phone = basic_details[1]
                address = basic_details[5].replace("-", ",").replace(";", "\\n")
                data = {
                    "uniqueid": uniqueid,
                    "name": name,
                    "age": age,
                    "sex": sex,
                    "phone": phone,
                    "address": address,
                }

            with open(f"{patient_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                if len([row for row in reader]) < 2:
                    data[
                        "alertmessage"
                    ] = "Patient details are not entered! Please enter them now!"
                    return render(request, "doctor_add_patient_details.html", data)

            return render(request, "enter_prescription.html", data)

        elif patient_name:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0].strip() == patient_name.strip():
                        current_name = row[0]
                        patient_id = row[-1]
                        break
                else:
                    return render(
                        request,
                        "doctor_search_patient.html",
                        {"alertmessage": "Patient not found!"},
                    )
            current_name = patient_name
            with open(f"{patient_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                basic_details = next(reader)
                uniqueid = basic_details[-4]
                name = basic_details[0]
                age = basic_details[6]
                sex = basic_details[7]
                phone = basic_details[1]
                address = basic_details[5].replace("-", ",").replace(";", "\\n")
                data = {
                    "uniqueid": uniqueid,
                    "name": name,
                    "age": age,
                    "sex": sex,
                    "phone": phone,
                    "address": address,
                }

            with open(f"{patient_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                if len([row for row in reader]) < 2:
                    data[
                        "alertmessage"
                    ] = "Patient details are not entered! Please enter them now!"
                    return render(request, "doctor_add_patient_details.html", data)

            return render(request, "enter_prescription.html", data)

        else:
            return render(
                request,
                "doctor_prescription_search_patient.html",
                {"alertmessage": "Please fill any one field!"},
            )

    return render(request, "doctor_prescription_search_patient.html")


def add_prescription_details(request):
    if request.method == "POST":
        current_name = request.POST.get("name")
        medical_prescription = (
            request.POST.get("prescription").replace(",", "-").replace("\r\n", ";")
        )
        examination = (
            request.POST.get("examination").replace(",", "-").replace("\r\n", ";")
        )
        treatment = request.POST.get("treatment").replace(",", "-").replace("\r\n", ";")
        advice = request.POST.get("advice").replace(",", "-").replace("\r\n", ";")

        with open("patients.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == current_name:
                    patient_id = row[-1]
                    break
        with open(f"{patient_id}.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([examination, medical_prescription, treatment, advice])

        with open(f"{patient_id}.csv", "r") as oldfile, open(
                f"{patient_id}.tmp", "w", newline=""
        ) as newfile:
            reader = csv.reader(oldfile)
            writer = csv.writer(newfile, quoting=csv.QUOTE_NONE, escapechar="\\")

            myrow = [row for row in reader]

            myrow[1][6] = medical_prescription
            myrow[1][10] = examination
            myrow[1][12] = treatment
            myrow[1][13] = advice

            for row in myrow:
                writer.writerow(row)

        os.replace(f"{patient_id}.tmp",
                   f"{patient_id}.csv")
        return render(
            request,
            "doctor_prescription_search_patient.html",
            {"alertmessage": "Prescription added successfully!"},
        )
    return render(request, "enter_prescription.html")


def display_registered_patients(request):
    class Patient:
        def __init__(self, row):
            self.uniqueid = row[10]
            self.name = row[0]
            self.phonenumber = row[1]
            self.dob = row[2]
            self.email = row[3]
            self.address = row[5].replace("-", ",").replace(";", "\\n")
            self.age = row[6]
            self.gender = row[7]
            self.blood = row[8]
            self.privilege = "Patient" if row[9] == "pat" else ""

    with open("patients.csv") as csvfile:
        reader = csv.reader(csvfile)
        patient_data = []
        for i in reader:
            patient_data.append(Patient(i))
        data = {"patients": patient_data}
    return render(request, "display_registered_patients.html", data)


def display_registered_receptionists(request):
    class Receptionist:
        def __init__(self, row):
            self.uniqueid = row[10]
            self.name = row[0]
            self.phonenumber = row[1]
            self.dob = row[2]
            self.email = row[3]
            self.address = row[5].replace("-", ",").replace(";", "\\n")
            self.age = row[6]
            self.gender = row[7]
            self.blood = row[8]
            self.privilege = "Receptionist" if row[9] == "rec" else ""

    with open("receptionists.csv") as csvfile:
        reader = csv.reader(csvfile)
        receptionist_data = []
        for i in reader:
            receptionist_data.append(Receptionist(i))
        data = {"receptionists": receptionist_data}
    return render(request, "display_registered_receptionists.html", data)


def display_registered_doctors(request):
    class Doctor:
        def __init__(self, row):
            self.uniqueid = row[10]
            self.name = row[0]
            self.phonenumber = row[1]
            self.dob = row[2]
            self.email = row[3]
            self.address = row[5].replace("-", ",").replace(";", "\\n")
            self.age = row[6]
            self.gender = row[7]
            self.blood = row[8]
            self.privilege = "Doctor" if row[9] == "doc" else ""

    with open("doctors.csv") as csvfile:
        reader = csv.reader(csvfile)
        doctor_data = []
        for i in reader:
            doctor_data.append(Doctor(i))
        data = {"doctors": doctor_data}

    return render(request, "display_registered_doctors.html", data)


def receptionist_appointment_homepage(request):
    return render(request, "receptionist_appointment_homepage.html")


def testing(request):
    return render(request, "receptionist_transaction_search_patient.html")


def receptionist_transaction_search_patient(request):
    if request.method == "POST":
        patient_id = request.POST.get("patientid")
        patient_name = request.POST.get("patientname")
        current_name = ""
        if patient_id:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[-1].strip() == patient_id.strip():
                        current_name = row[0]
                        break
                else:
                    return render(
                        request,
                        "receptionist_transaction_search_patient.html",
                        {"alertmessage": "Patient not found!"},
                    )

            with open(f"{patient_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data = {
                        "uniqueid": row[-4],
                        "name": row[0],
                        "email": row[3],
                    }
                    break

            return render(request, "payment_form.html", data)

        elif patient_name:
            current_name = patient_name
            with open("patients.csv") as csvfile:
                reader = csv.reader(csvfile)
                if current_name not in [name[0] for name in reader]:
                    return render(
                        request,
                        "receptionist_transaction_search_patient.html",
                        {"alertmessage": "Patient not found!"},
                    )
            
            with open("patients.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == current_name:
                        patient_id = row[-1]
                        break

            with open(f"{patient_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data = {
                        "uniqueid": row[-4],
                        "name": row[0],
                        "email": row[3],
                    }
                    break

            return render(request, "payment_form.html", data)
        else:
            return render(
                request,
                "receptionist_transaction_search_patient.html",
                {"alertmessage": "Fill any one field!"},
            )

    return render(request, "receptionist_transaction_search_patient.html")


def payment_form(request):
    if request.method == "POST":
        email = request.POST.get("email")
        name = request.POST.get("name")
        uniqueid = request.POST.get("unique-id")
        charges = request.POST.get("treatment-charges")
        charge_type = request.POST.get("charge-type")

        date_time = datetime.datetime.now()

        contents_to_write = []
        with open(f"{uniqueid}.csv", "r") as oldfile:
            reader = csv.reader(oldfile)
            contents_to_write.append(next(reader))

            try:
                temp = next(reader)
            except StopIteration:
                return render(
                    request,
                    "homepage.html",
                    {
                        "alertmessage": "Cannot add charges until doctor adds required data!"
                    },
                )

            temp[-1] = charges

            contents_to_write.append(temp)

            for row in reader:
                contents_to_write.append(row)

        with open(f"{uniqueid}.csv", "w", newline="") as newfile:
            writer = csv.writer(newfile)
            writer.writerows(contents_to_write)
        
        with open("transactions.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, uniqueid, email, charges, charge_type, date_time])

        subject = "Payment Status"

        body = (
            f"Hello {name},\n"
            f"\tThis email is your invoice regarding your last payment at the clinic.\n"
            f"The payment details are as follows:\n"
            f"Name of the patient: {name}\n"
            f"Patient ID: {uniqueid}\n"
            f"Email: {email}\n"
            f"Amount charged: ₹{charges}\n"
            f"Charge Type: {charge_type}\n"
            f"Charging Date and Time: {date_time}\n"
            f"Wishing you a speedy recovery.\n"
            f"Thank You.\n"
        )

        send_email.send_email(email, subject, body)

        return render(
            request,
            "homepage.html",
            {"alertmessage": "Transaction saved successfully!"},
        )

    return render(request, "payment_form.html")


def receptionist_time_slot(request):
    if request.method == "POST":
        if not os.path.exists("Confirmedappointments.csv"):
            with open("Confirmedappointments.csv", mode="w", newline="") as file:
                pass
            file.close()
        if not os.path.exists("appointments.json"):
            apb.writejson()

        doctor = request.POST.get("doctor")
        doctorid = None
        with open("doctors.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == doctor:
                    doctorid = row[-1]
                    break

        olddate = request.POST.get("date").split("-")
        olddate.reverse()
        date = ""
        for d in olddate:
            date += d + "-"
        date = date[:-1]
        oldtimeslot = request.POST.getlist("slots")

        timeslot = List(5)
        for t in oldtimeslot:
            timeslot.append(slot_dict.get(t))

        apb.timeslotgenerator(doctorid, date, timeslot)

        return render(
            request, "homepage.html", {"alertmessage": "Time slot edited successfully!"}
        )
    else:

        class Doctor:
            def __init__(self, name):
                self.name = name

        doctors = []
        with open("doctors.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                doctors.append(Doctor(row[0]))
        data = {"doctors": doctors}
        return render(request, "edit_timeslots.html", data)


def receptionist_book_appointment(request):
    if request.method == "POST":
        patient_id = request.POST.get("patientid")
        patient_name = request.POST.get("patientname")
        current_name = ""
        if patient_id:
            with open("register.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[-1].strip() == patient_id.strip():
                        current_name = row[0]
                        break
                else:
                    return render(
                        request,
                        "receptionist_book_appointment_search_patient.html",
                        {"alertmessage": "Patient not found!"},
                    )

            with open(f"{patient_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data = {
                        "uniqueid": row[-4],
                        "name": row[0],
                        "age": row[6],
                        "gender": row[7],
                        "address": row[5].replace("-", ",").replace(";", "\\n"),
                    }
                    break

            return render(request, "receptionist_book_appointment.html", data)
        elif patient_name:
            unique_id = ''
            current_name = patient_name
            with open("patients.csv") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == current_name:
                        unique_id = row[-1]
                        break
                else:
                    return render(
                        request,
                        "receptionist_book_appointment_search_patient.html",
                        {"alertmessage": "Patient not found!"},
                    )
            

            with open(f"{unique_id}.csv", "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data = {
                        "uniqueid": row[-4],
                        "name": row[0],
                        "age": row[6],
                        "gender": row[7],
                        "address": row[5].replace("-", ",").replace(";", "\\n"),
                    }
                    break

            return render(request, "receptionist_book_appointment.html", data)
        else:
            return render(
                request,
                "receptionist_book_appointment_search_patient.html",
                {"alertmessage": "Fill any one field!"},
            )

    return render(request, "receptionist_book_appointment_search_patient.html")


def patient_appointment_homepage(request):
    return render(request, "patient_appointments.html")


def patient_book_appointment(request):
    print(request.session)
    if request.method == "POST":
        olddate = request.POST.get("date").split("-")
        olddate.reverse()
        date = ""
        for d in olddate:
            date += d + "-"
        date = date[:-1]
        doctor = request.POST.get("doctor")
        pid = request.POST.get("uniqueid")
        with open("doctors.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == doctor:
                    d_uniqueid = row[-1]
                    data = {"d_uniqueid": d_uniqueid, "p_uniqueid": pid, "date": date}
                    break
        return view_timeslots(request, data)
        # return render(request, "select_timeslot.html", data)

    class Doctor:
        def __init__(self, name):
            self.name = name

    doctors = []
    with open("doctors.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            doctors.append(Doctor(row[0]))
    data = {"doctors": doctors}

    with open("patients.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3] == request.session.get("CURRENT_USER"):
                data.update({
                    "name": row[0],
                    "uniqueid": row[-1],
                    "age": row[6],
                    "sex": row[7],
                    "address": row[5].replace("-", ",").replace(";", "\\n"),
                })
                # data.update(temp)
                break

    return render(request, "patient_book_appointment.html", data)


def view_timeslots(request, data=None):
    if not os.path.exists("Confirmedappointments.csv"):
        with open("Confirmedappointments.csv", mode="w", newline="") as file:
            pass
        file.close()
    if not os.path.exists("appointments.json"):
        apb.writejson()
    if data is None:
        timeslot = request.POST.get("rdvalue")
        doctorid = request.POST.get("docid")
        patientid = request.POST.get("patid")
        date = request.POST.get("dt")
        doctorname = ""
        apb.bookappointment(patientid, doctorid, date, timeslot)
        with open("doctors.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[-1] == doctorid:
                    doctorname = row[0]
                    break

        name = ""
        with open("patients.csv") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[3] == request.session.get("CURRENT_USER"):
                    name = row[0]
                    break
        subject = "Appointment confirmation"

        content = (
            f"Hello {name},\n"
            f"\t This email is a confirmation that we have received your appointment request."
            f"Your appointment details:\n"
            f"\t\tPatient Name: {name}\n"
            f"\t\tPatient ID: {patientid}\n"
            f"\t\tDoctor Name: {doctorname}\n"
            f"\t\tDate: {date}\n"
            f"\t\tTime Slot: {timeslot}\n"
            f"Thank you."
        )

        send_email.send_email(request.session["CURRENT_USER"], subject, content)

        return render(
            request,
            "patient_homepage.html",
            {"alertmessage": "Appointment booking successfull!"},
        )
    if request.method == "POST":

        class WhatColor:
            def __init__(self, boolean, timeslot):
                self.color = None
                if boolean:
                    self.color = "#37d766"
                else:
                    self.color = "#ff6661"
                self.lblname = lbl_slot_dict.get(timeslot)
                self.rdname = lbl_slot_dict.get(timeslot).replace("lbl", "")

        doctorid = data.get("d_uniqueid")
        patientid = data.get("p_uniqueid")
        date = data.get("date")
        timeslots = [
            "09:00-09:30",
            "09:30-10:00",
            "10:00-10:30",
            "10:30-11:00",
            "11:00-11:30",
            "13:30-14:00",
            "14:00-14:30",
            "14:30-15:00",
            "15:00-15:30",
            "15:30-16:00",
            "16:00-16:30",
            "16:30-17:00",
        ]
        colors = []

        for time in timeslots:
            try:
                isAvailable = apb.checkavailability(doctorid, date, time)
            except AttributeError:
                return render(
                    request,
                    "patient_homepage.html",
                    {
                        "alertmessage": "The selected date is not ready for booking! Please try with another date!"
                    },
                )
            colors.append(WhatColor(isAvailable, time))

        data = {"colors": colors, "docid": doctorid, "patid": patientid, "dt": date}

        return render(request, "select_timeslot.html", data)


def patient_appointment_history(request):
    class PatientAppointmentData:
        def __init__(self, patient_id, doctor_id, date, timeslot, booking_date_time):
            self.patientid = patient_id
            self.doctorid = doctor_id
            self.date = date
            self.timeslot = timeslot
            self.bookingdatetime = booking_date_time

    patient_id = ""
    patient_name = ""
    with open("patients.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3] == request.session.get("CURRENT_USER"):
                patient_id = row[-1]
                patient_name = row[0]

    appointmentdata = []
    with open("Confirmedappointments.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == patient_id:
                doctorname = ""
                with open("doctors.csv") as anothercsvfile:
                    anothereader = csv.reader(anothercsvfile)
                    for anotherow in anothereader:
                        if anotherow[-1] == row[1]:
                            doctorname = anotherow[0]
                appointmentdata.append(
                    PatientAppointmentData(
                        patient_name, doctorname, row[2], row[3], row[4]
                    )
                )

    data = {"appointmentdata": appointmentdata}

    return render(request, "patient_appointment_history.html", data)


def receptionist_view_appointments(request):
    class AppointmentData:
        def __init__(self, patient_id, doctor_id, date, timeslot, booking_date_time):
            self.patientid = patient_id
            self.doctorid = doctor_id
            self.date = date
            self.timeslot = timeslot
            self.bookingdatetime = booking_date_time

    patient_id = ""
    patient_name = ""

    appointmentdata = []
    with open("Confirmedappointments.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            doctorname = ""
            with open("doctors.csv") as anothercsvfile:
                anothereader = csv.reader(anothercsvfile)
                for anotherow in anothereader:
                    if anotherow[-1] == row[1]:
                        doctorname = anotherow[0]
            with open("patients.csv") as acsvfile:
                areader = csv.reader(acsvfile)
                for arow in areader:
                    if arow[-1] == row[0]:
                        patient_id = arow[-1]
                        patient_name = arow[0]
            appointmentdata.append(
                AppointmentData(patient_name, doctorname, row[2], row[3], row[4])
            )

    appointmentdata.sort(
        reverse=True, key=lambda x: (x.date, [-ord(ch) for ch in x.timeslot])
    )

    data = {"appointmentdata": appointmentdata}

    return render(request, "appointment_history.html", data)


def doctor_appointment_history(request):
    class DoctorAppointmentData:
        def __init__(self, patient_id, doctor_id, date, timeslot, booking_date_time):
            self.patientid = patient_id
            self.doctorid = doctor_id
            self.date = date
            self.timeslot = timeslot
            self.bookingdatetime = booking_date_time

    doctor_id = ""
    doctor_name = ""
    with open("doctors.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3] == request.session.get("CURRENT_USER"):
                doctor_id = row[-1]
                doctor_name = row[0]

    appointmentdata = []
    with open("Confirmedappointments.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[1] == doctor_id:
                patient_name = ""
                with open("patients.csv") as anothercsvfile:
                    anothereader = csv.reader(anothercsvfile)
                    for anotherow in anothereader:
                        if anotherow[-1] == row[0]:
                            patient_name = anotherow[0]
                appointmentdata.append(
                    DoctorAppointmentData(
                        patient_name, doctor_name, row[2], row[3], row[4]
                    )
                )

    data = {"appointmentdata": appointmentdata}

    return render(request, "doctor_appointment_history.html", data)


def logout(request):
    request.session["CURRENT_USER"] = None
    request.session["CURRENT_PRIV"] = None
    return render(request, "index.html")


def book_local_appointment(request):
    if request.method == "POST":
        graph = Graph()

        for file in os.listdir("./GraphResources/Diseases/"):
            graph.add_node(file.strip().lower().replace(".txt", ""), "disease")
            with open("./GraphResources/Diseases/" + file) as f:
                lines = f.readlines()
                for line in lines:
                    graph.add_node(line.strip().lower().replace(".txt", ""), "symptom")
                    graph.add_edge_disease(
                        file.strip().lower().replace(".txt", ""),
                        line.strip().lower().replace(".txt", ""),
                    )

        graph.add_node((0, 15), "agegroup")
        graph.add_node((16, 80), "agegroup")
        graph.add_node((81, 100), "agegroup")

        for file in os.listdir("./GraphResources/Doctors/"):
            graph.add_node(file.strip().lower().replace(".txt", ""), "doctor")
            with open("./GraphResources/Doctors/" + file) as f:
                lines = f.readlines()
                for line in lines:
                    graph.add_edge_doctor(
                        line.strip().lower().replace(".txt", ""),
                        (0, 15),
                        file.strip().lower().replace(".txt", ""),
                    )
                    graph.add_edge_doctor(
                        line.strip().lower().replace(".txt", ""),
                        (16, 80),
                        file.strip().lower().replace(".txt", ""),
                    )
                    graph.add_edge_doctor(
                        line.strip().lower().replace(".txt", ""),
                        (81, 100),
                        file.strip().lower().replace(".txt", ""),
                    )

        class QueueDetails:
            def __init__(self, p_name, p_age, p_uniqueid, p_symptom, p_doctor, p_disease):
                self.name = p_name
                self.age = p_age
                self.uniqueid = p_uniqueid
                self.symptom = p_symptom
                self.doctor = p_doctor
                self.disease = p_disease

        name = request.POST.get("name")
        age = request.POST.get("age")
        uniqueid = request.POST.get("uniqueid")
        symptom = list(request.POST.get("symptoms").lower().split(","))

        matched_disease = graph.find_disease(symptom)

        matched_doctor = graph.get_matching_doctors(matched_disease, int(age))[0]

        queuename = f"QUEUE_{matched_doctor.upper()}"

        command = f"{queuename}.enqueue(QueueDetails(name, age, uniqueid, symptom, matched_doctor, matched_disease))"

        eval(command)

        return render(
            request,
            "homepage.html",
            {"alertmessage": f"Appointment booked for doctor {matched_doctor}"},
        )


def receptionist_view_local_appointments(request):
    results = []
    for queue in QUEUES:
        temp = queue
        templist = []
        while True:
            try:
                d = temp.dequeue()
                results.append(d)
                templist.append(d)
            except QueueDS.EmptyQueueError:
                for elt in templist:
                    queue.enqueue(elt)
                templist = []
                break

    data = {"appointmentdata": results}

    return render(request, "local_appointments.html", data)


def patient_view_history(request):
    print(request.session)
    patientid = ""
    patientname = ""
    phonenumber = ""
    gender = ""
    bloodgroup = ""
    address = ""
    dob = ""
    age = ""
    username = ""
    lastappointment = ""
    upcomingappointment = ""
    dentalcarries = ""
    missingtooth = ""
    allergy = ""
    abrasions = ""
    medicaldatas = []
    appointmentdatas = []
    lastappointment = None
    upcomingappointment = None

    class MedicalData:
        def __init__(self, examination, prescription, treatment, treatmentadvice):
            self.examination = examination
            self.prescription = prescription
            self.treatment = treatment
            self.treatmentadvice = treatmentadvice

    class AppointmentData:
        def __init__(self, patientname, doctorname, date, timeslot):
            self.patientname = patientname
            self.doctorname = doctorname
            self.date = date
            self.timeslot = timeslot

    patientid = ""
    patientname = ""
    username = request.session.get("CURRENT_USER")

    with open("patients.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3] == request.session.get("CURRENT_USER"):
                patientid = row[-1]
                patientname = row[0]
    
    medicaldatas = []
    appointmentdatas = []

    with open("Confirmedappointments.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == patientid:
                doctorname = ""
                with open("doctors.csv") as anothercsvfile:
                    anotherreader = csv.reader(anothercsvfile)
                    for anotherrow in anotherreader:
                        if anotherrow[-1] == row[1]:
                            doctorname = anotherrow[0]
                appointmentdata = AppointmentData(
                    patientname, doctorname, row[2], row[3]
                )
                appointmentdatas.append(appointmentdata)

    temp1 = {}
    temp2 = {}
    with open("Confirmedappointments.csv") as acsvfile:
        areader = csv.reader(acsvfile)
        for arow in areader:
            if arow[0] == patientid:
                doctor_id = arow[1]
                with open("doctors.csv") as anothercsvfile:
                    anotherreader = csv.reader(anothercsvfile)
                    for anotherrow in anotherreader:
                        if anotherrow[-1] == doctor_id:
                            doctorname = anotherrow[0]

                today = datetime.datetime.today()
                appointment = arow[2]
                date, month, year = appointment.split("-")
                appointment_date = datetime.datetime(
                    int(year), int(month), int(date)
                )
                if appointment_date > today:
                    temp2[appointment_date - today] = appointment
                else:
                    temp1[today - appointment_date] = appointment

    lastappointment = temp1.get(min(temp1.keys(), default="EMPTY"))
    upcomingappointment = temp2.get(min(temp2.keys(), default="EMPTY"))


    with open(f"{patientid}.csv") as csvfile:
        reader = csv.reader(csvfile)
        firstrow = next(reader)

        phonenumber = firstrow[1]
        dob = firstrow[2]
        address = firstrow[5].replace("-", ",").replace(";", "\\n")
        age = firstrow[6]
        gender = firstrow[7]
        bloodgroup = firstrow[8]

        try:
            secondrow = next(reader)
        except StopIteration:
            data = {
                "uniqueid": patientid,
                "patientname": patientname,
                "phonenumber": phonenumber,
                "gender": gender,
                "bloodgroup": bloodgroup,
                "address": address,
                "dob": dob,
                "age": age,
                "username": username,
                "lastappointment": lastappointment,
                "upcomingappointment": upcomingappointment,
                "dentalcarries": dentalcarries,
                "missingteeth": missingtooth,
                "allergy": allergy,
                "abrasions": abrasions,
                "medicaldatas": medicaldatas,
                "appointmentdatas": appointmentdatas,
            }

            request.session["CURRENT_USER"] = username

            return render(request, "view_patient_history.html", data)

        dentalcarries = secondrow[7].replace("-", ",").replace(";", "\\n")
        missingtooth = secondrow[8].replace("-", ",").replace(";", "\\n")
        allergy = secondrow[9].replace("-", ",").replace(";", "\\n")
        abrasions = secondrow[11].replace("-", ",").replace(";", "\\n")


        for row in reader:
            medicaldata = MedicalData(row[0], row[1], row[2], row[3])
            medicaldatas.append(medicaldata)


    data = {
        "uniqueid": patientid,
        "patientname": patientname,
        "phonenumber": phonenumber,
        "gender": gender,
        "bloodgroup": bloodgroup,
        "address": address,
        "dob": dob,
        "age": age,
        "username": username,
        "lastappointment": lastappointment,
        "upcomingappointment": upcomingappointment,
        "dentalcarries": dentalcarries,
        "missingteeth": missingtooth,
        "allergy": allergy,
        "abrasions": abrasions,
        "medicaldatas": medicaldatas,
        "appointmentdatas": appointmentdatas,
    }

    request.session["CURRENT_USER"] = username

    return render(request, "view_patient_history.html", data)


def patient_view_payments(request):
    
    class TransactionData:
        def __init__(self, name, t_id, email, amount, chargetype, date_time):
            self.name = name
            self.id = t_id
            self.email = email
            self.amount = amount
            self.chargetype = chargetype
            self.date_time = date_time

    transactiondatas = []

    with open("transactions.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[2] == request.session.get("CURRENT_USER"):
                transactiondatas.append(
                    TransactionData(row[0], row[1], row[2], row[3], row[4], row[5])
                )

    return render(
        request, "patient_payments.html", {"transactiondatas": transactiondatas}
    )


def receptionist_view_payments(request):
    class TransactionData:
        def __init__(self, name, t_id, email, amount, chargetype, date_time):
            self.name = name
            self.id = t_id
            self.email = email
            self.amount = amount
            self.chargetype = chargetype
            self.date_time = date_time

    transactionstack = Stack(5)

    with open("transactions.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            transactionstack.push(
                TransactionData(row[0], row[1], row[2], row[3], row[4], row[5])
            )
    
    transactiondatas = []
    for idx in range(len(transactionstack)):
        transactiondatas.append(transactionstack.pop())


    return render(
        request, "receptionist_payments.html", {"transactiondatas": transactiondatas}
    )


def doctor_register(request):
    if request.method == "POST":
        name = request.POST["name"]
        mobile = request.POST["mobile"]
        dob = request.POST["dob"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        address = request.POST["address"].replace(",", "-").replace("\r\n", ";")
        age = request.POST["age"]
        gender = request.POST["gender"]
        blood_group = request.POST["blood-group"]

        if password != confirm_password:
            return render(
                request,
                "doctor_register.html",
                {"alertmessage": "Passwords do not match."},
            )

        with open("register.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if email == row[3]:
                    return render(
                        request,
                        "doctor_register.html",
                        {"alertmessage": "E-mail already exists."},
                    )

            uniqueid_random = str(random.randint(100000, 999999))
            while uniqueid_random in [row[-1] for row in reader]:
                uniqueid_random = str(random.randint(100000, 999999))

        with open("register.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    name,
                    mobile,
                    dob,
                    email,
                    password,
                    address,
                    age,
                    gender,
                    blood_group,
                    "doc",
                    uniqueid_random,
                ]
            )

        with open("doctors.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    name,
                    mobile,
                    dob,
                    email,
                    password,
                    address,
                    age,
                    gender,
                    blood_group,
                    "doc",
                    uniqueid_random,
                ]
            )

        return render(
            request,
            "admin_homepage.html",
            {"alertmessage": "New user registration information stored successfully."},
        )

    return render(request, "doctor_register.html")


def receptionist_register(request):
    if request.method == "POST":
        name = request.POST["name"]
        mobile = request.POST["mobile"]
        dob = request.POST["dob"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]
        address = request.POST["address"].replace(",", "-").replace("\r\n", ";")
        age = request.POST["age"]
        gender = request.POST["gender"]
        blood_group = request.POST["blood-group"]

        if password != confirm_password:
            return render(
                request,
                "receptionist_register.html",
                {"alertmessage": "Passwords do not match."},
            )

        with open("register.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if email == row[3]:
                    return render(
                        request,
                        "receptionist_register.html",
                        {"alertmessage": "E-mail already exists."},
                    )

            uniqueid_random = str(random.randint(100000, 999999))
            while uniqueid_random in [row[-1] for row in reader]:
                uniqueid_random = str(random.randint(100000, 999999))

        with open("register.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    name,
                    mobile,
                    dob,
                    email,
                    password,
                    address,
                    age,
                    gender,
                    blood_group,
                    "rec",
                    uniqueid_random,
                ]
            )

        with open("receptionists.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    name,
                    mobile,
                    dob,
                    email,
                    password,
                    address,
                    age,
                    gender,
                    blood_group,
                    "rec",
                    uniqueid_random,
                ]
            )

        return render(
            request,
            "admin_homepage.html",
            {"alertmessage": "New user registration information stored successfully."},
        )

    return render(request, "receptionist_register.html")
