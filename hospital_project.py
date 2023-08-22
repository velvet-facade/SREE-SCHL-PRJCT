from tkinter import *
from tkinter import ttk
from pillow import ImageTk, Image
import tkinter.messagebox
from datetime import datetime
import datetime
import tkcalendar as tc
import mysql.connector as sqlcon
import webbrowser

con = sqlcon.connect(
    host="localhost", user="root", password="Sree@19"
)  # connection to mysql
cur = con.cursor()
if con:
    # Carry out normal procedure
    print("Connection successful")
else:
    print("Connection unsuccessful")
cur.execute("create database if not exists Hospital")
cur.execute("use Hospital")
cur.execute(
    "create table if not exists appointment"
    "(idno int primary key,"
    "name char(50),"
    "age char(3),"
    "gender char(1),"
    "phone varchar(10),"
    "bg varchar(3),"
    "purpose int,"
    "udate varchar(20))"
)
cur.execute(
    "create table if not exists appointment_details"
    "(ano int primary key,"
    "idno int,"
    "dno int,"
    "date varchar(20),"
    "time varchar(20),"
    "remarks varchar(200),"
    "udate varchar(20))"
)
cur.execute(
    "create table if not exists doctor_details"
    "("
    "dno int primary key,"
    "doctor varchar(50),"
    "specialist varchar(50),"
    "room varchar(3),"
    "time varchar(20),"
    "phone varchar(10),"
    "amount varchar(20),"
    "category varchar(1),"
    "udate varchar(20))"
)


# Check for alphabet - This function is written to allow space
# and . in text fields additionally
def checkalpha(ca):
    if ca.isalpha() or " " in ca or "." in ca:
        return 0
    else:
        return 1


# Get Doctor / Service details from master table
def doctorservice(x):
    if x == 1:
        cur.execute(
            "select concat(dno,'. ',doctor) as Doctor from doctor_details where category = 'd'"
        )
    elif x == 2:
        cur.execute(
            "select concat(dno,'. ',doctor) as Service from doctor_details where category = 's'"
        )
    ar = cur.fetchall()
    data = []
    for row in ar:
        data.append(row[0])
    return data


# Patient Registration - GUI
def register():
    global e1, e2, e3, e4, e5, e6, e7
    root1 = Tk()
    root1.title("Hospital Management System")
    label = Label(root1, text="Patient Registration", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root1, height=350, width=350)
    frame.pack()
    l1 = Label(root1, text="Aadhar Card No.")
    l1.place(x=40, y=70)
    e1 = tkinter.Entry(root1)
    e1.place(x=160, y=70, width=140)
    l2 = Label(root1, text="Name")
    l2.place(x=40, y=110)
    e2 = tkinter.Entry(root1)
    e2.place(x=160, y=110, width=140)
    l3 = Label(root1, text="Age")
    l3.place(x=40, y=150)
    e3 = tkinter.Entry(root1)
    e3.place(x=160, y=150, width=140)
    l4 = Label(root1, text="Gender M/F")
    l4.place(x=40, y=190)
    e4 = ttk.Combobox(root1, values=["F", "M"], state="readonly")
    e4.place(x=160, y=190)
    l5 = Label(root1, text="Phone")
    l5.place(x=40, y=230)
    e5 = tkinter.Entry(root1)
    e5.place(x=160, y=230, width=140)
    l6 = Label(root1, text="Blood Group")
    l6.place(x=40, y=270)
    e6 = ttk.Combobox(
        root1,
        values=["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"],
        state="readonly",
    )
    e6.place(x=160, y=270)
    l7 = Label(root1, text="Purpose of visit")
    l7.place(x=40, y=310)
    e7 = ttk.Combobox(
        root1, values=["1.Doctor Appointment", "2.Other Services"], state="readonly"
    )
    e7.place(x=160, y=310)
    b1 = Button(
        root1, text="Submit", command=entry, bg="light blue", font="cambria 10 bold"
    )
    b1.place(x=120, y=350)
    b3 = Button(
        root1,
        text="Close",
        command=root1.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=200, y=350)
    root1.resizable(False, False)


# Patient registration - Save in Database
def entry():
    global e1, e2, e3, e4, e5, e6, e7, now1, cdate1
    reg1 = e1.get()
    reg2 = e2.get()
    reg3 = e3.get()
    reg4 = e4.get()
    reg5 = e5.get()
    reg6 = e6.get()
    reg7 = e7.get()
    if reg7 != "":
        reg8 = reg7[0]
    if (
        reg1 == ""
        or reg2 == ""
        or reg3 == ""
        or reg4 == ""
        or reg5 == ""
        or reg6 == ""
        or reg7 == ""
    ):
        tkinter.messagebox.showerror("Validation", "Please enter all the fields!")
        return
    if not reg1.isdigit():
        tkinter.messagebox.showerror(
            "Validation", "Please enter only numeric value for Aadhar number"
        )
        return
    if checkalpha(reg2) == 1:
        tkinter.messagebox.showerror(
            "Validation", "Please enter only alphabets for Name"
        )
        return
    if not reg3.isdigit() or int(reg3) > 125:
        tkinter.messagebox.showerror(
            "Validation", "Please enter only numeric value 1ess than 126 for Age"
        )
        return
    if not reg5.isdigit() or len(reg5) != 10:
        tkinter.messagebox.showerror(
            "Validation", "Please enter only 10 digit number for Phone number"
        )
        return
    now1 = datetime.datetime.today()
    cdate1 = now1.strftime("%d/%m/%Y")
    query1 = 'insert into appointment values("{}", "{}", "{}", "{}", "{}","{}","{}","{}")'.format(
        reg1, reg2, reg3, reg4, reg5, reg6, reg8, cdate1
    )
    cur.execute(query1)
    con.commit()
    tkinter.messagebox.showinfo("Information", "Registration completed successfully")


aadhar = None


# Get Aadhar number - Common entry screen for appointment booking,
# appointment update and patient update
def get_aadhar(i):
    global adh, aadhar
    root2 = Tk()
    root2.title("Hospital Management System")
    label = Label(root2, text="Search Patient", font="cambria 20 bold")
    label.pack()
    frame = Frame(root2, height=140, width=250)
    frame.pack()
    l1 = Label(root2, text="Aadhar No.")
    l1.place(x=10, y=70)
    adh = tkinter.Entry(root2)
    adh.place(x=100, y=70)
    aadhar = adh.get()
    if i == 1:
        b1 = Button(
            root2, text="Submit", command=book, bg="light blue", font="cambria 10 bold"
        )
        b1.place(x=70, y=120)
    elif i == 2:
        b1 = Button(
            root2,
            text="Submit",
            command=updatepat,
            bg="light blue",
            font="cambria 10 bold",
        )
        b1.place(x=70, y=120)
    b3 = Button(
        root2,
        text="Close",
        command=root2.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=140, y=120)
    root2.resizable(False, False)


# Appointment booking - GUI
def book():
    global aadhar, bk1, bk2, bk3, bk4, bk5, bk6
    aadhar = adh.get()
    if aadhar == " ":
        tkinter.messagebox.showerror("Error", "No record found")
        return
    root3 = Tk()
    root3.title("Hospital Management System")
    label = Label(root3, text="Appointment Booking", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root3, height=290, width=350)
    frame.pack()
    i1 = Label(root3, text="Aadhar Card No.")
    i1.place(x=40, y=80)
    bk1 = Label(root3, text=aadhar)
    bk1.place(x=160, y=80, width=140)
    cur.execute("select * from appointment where idno =%s" % aadhar)
    ar = cur.fetchall()
    if len(ar) == 0:
        tkinter.messagebox.showerror("Error", "No record found")
        return
    for row in ar:
        bk5 = row[1]
        bk6 = row[6]
    l2 = Label(root3, text="Name")
    l2.place(x=40, y=120)
    bk2 = Label(root3, text=bk5)
    bk2.place(x=160, y=120, width=140)
    if bk6 == 1:
        i7 = Label(root3, text="Doctor")
        i7.place(x=40, y=160)
        bk3 = ttk.Combobox(root3, values=doctorservice(1), state="readonly")
        bk3.set("Select")
        bk3.place(x=160, y=160, width=140)
    elif bk6 == 2:
        i7 = Label(root3, text="Services")
        i7.place(x=40, y=160)
        bk3 = ttk.Combobox(root3, values=doctorservice(2), state="readonly")
        bk3.set("Select")
        bk3.place(x=160, y=160, width=140)
    i8 = Label(root3, text="Remarks")
    i8.place(x=40, y=200)
    bk4 = tkinter.Entry(root3)
    bk4.place(x=160, y=200, width=140, height=50)
    b1 = Button(
        root3, text="Submit", command=booking, bg="light blue", font="cambria 10 bold"
    )
    b1.place(x=120, y=280)
    b3 = Button(
        root3,
        text="Close",
        command=root3.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=200, y=280)
    i8 = Label(root3, text="*Appointment can be fixed only one day prior in advance!")
    i8.place(x=10, y=320)
    root3.resizable(False, False)


# Appointment booking - Save in Database
def booking():
    global aadhar, bk3, bk4, dcsv, dsp, dsn, bk7, bk8, bk9, bk11, bk12, bk13, now2, cdate2, msg1
    aadhar = adh.get()
    if aadhar == " ":
        tkinter.messagebox.showerror("Error", "No record found")
        return
    dcsv = bk3.get()
    dsp = dcsv.find(".", 1, 5)
    dsn = dcsv[0:dsp]
    bk7 = bk4.get()
    cur.execute("select * from doctor_details where dno =%s" % dsn)
    ar = cur.fetchall()
    for row in ar:
        bk8 = row[4]  # time
        bk9 = row[1]  # doctor
        bk12 = row[7]
    now = datetime.datetime.today() + datetime.timedelta(days=1)
    bk10 = now.strftime("%d/%m/%Y")
    cur.execute("select count(*) from appointment_details")
    arr = cur.fetchall()
    for row in arr:
        bk11 = row[0]
        bk11 = bk11 + 1
        now2 = datetime.datetime.today()
        cdate2 = now2.strftime("%d/%m/%Y")
        query10 = (
            "select count(*) from appointment_details a,doctor_details d where a.dno=d.dno and idno=%s and date='%s' and a.dno='%s'"
            % (aadhar, bk10, dsn)
        )
        cur.execute(query10)
        arr = cur.fetchall()
        print(arr)
        for row in arr:
            bk13 = row[0]
        if bk13 > 0:
            tkinter.messagebox.showerror(
                "Information", "You already have an appointment for tomorrow!"
            )
            return
        query2 = 'insert into appointment_details values("{}","{}", "{}", "{}","{}","{}","{}")'.format(
            bk11, aadhar, dsn, bk10, bk8, bk7, cdate2
        )
        cur.execute(query2)
        con.commit()
        if bk12 == "d":
            msg1 = (
                "Your appointment is fixed with Dr."
                + bk9
                + " on "
                + bk10
                + " between "
                + bk8
            )
        elif bk12 == "s":
            msg1 = (
                "Your appointment is fixed for "
                + bk9
                + " on "
                + bk10
                + ". You can visit the hospital anytime between "
                + bk8
                + "."
            )
        tkinter.messagebox.showinfo("Information", msg1)


# Modify Patient details - GUI
def updatepat():
    global aadhar, pd1, pd2, pd3, pd4, pd5, pat1, pat2, pat3, pat4, pat5, pat6, pat7, pat8, pat9, pat10
    aadhar = adh.get()
    if aadhar == "":
        tkinter.messagebox.showerror("Error", "No record found")
        return
    cur.execute("select * from appointment where idno =%s" % aadhar)
    ar = cur.fetchall()
    if len(ar) == 0:
        tkinter.messagebox.showerror("Error", "No record found")
        return
    root4 = Tk()
    root4.title("Hospital Management System")
    label = Label(root4, text="Modify Patient details", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root4, height=300, width=480)
    frame.pack()
    i1 = Label(root4, text="Aadhar Card No.")
    i1.place(x=40, y=80)
    adh1 = Label(root4, text=aadhar)
    adh1.place(x=160, y=80, width=140)
    for row in ar:
        pd1 = row[1]
        pd2 = row[2]
        pd3 = row[3]
        pd4 = row[4]
        pd5 = row[5]
    l2 = Label(root4, text="Name")
    l2.place(x=40, y=120)
    pat1 = Label(root4, text=pd1)
    pat1.place(x=160, y=120, width=140)
    pat6 = tkinter.Entry(root4)
    pat6.place(x=300, y=120, width=140)
    l3 = Label(root4, text="Age")
    l3.place(x=40, y=160)
    pat2 = Label(root4, text=pd2)
    pat2.place(x=160, y=160, width=140)
    pat7 = tkinter.Entry(root4)
    pat7.place(x=300, y=160, width=140)
    l4 = Label(root4, text="Gender M/F")
    l4.place(x=40, y=200)
    pat3 = Label(root4, text=pd3)
    pat3.place(x=160, y=200, width=140)
    pat8 = ttk.Combobox(root4, values=["F", "M"], state="readonly")
    pat8.place(x=300, y=200)
    l5 = Label(root4, text="Phone")
    l5.place(x=40, y=240)
    pat4 = Label(root4, text=pd4)
    pat4.place(x=160, y=240, width=140)
    pat9 = tkinter.Entry(root4)
    pat9.place(x=300, y=240, width=140)
    l6 = Label(root4, text="Blood Group")
    l6.place(x=40, y=280)
    pat5 = Label(root4, text=pd5)
    pat5.place(x=160, y=280, width=140)
    pat10 = ttk.Combobox(
        root4,
        values=["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"],
        state="readonly",
    )
    pat10.place(x=300, y=280)
    b1 = Button(
        root4, text="Submit", command=savepat, bg="light blue", font="cambria 10 bold"
    )
    b1.place(x=180, y=320)
    b3 = Button(
        root4,
        text="Close",
        command=root4.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=260, y=320)
    root4.resizable(False, False)


# Modify Patient details - Save in Database
def savepat():
    global aadhar, pd1, pd2, pd3, pd4, pd5, pat1, pat2, pat3, pat4, pat5, pat6, pat7, pat8, pat9, pat10, now3, cdate3
    aadhar = adh.get()
    if aadhar == "":
        tkinter.messagebox.showerror("Error", "No record found")
        return
    pat6 = pat6.get()
    pat7 = pat7.get()
    pat8 = pat8.get()
    pat9 = pat9.get()
    pat10 = pat10.get()
    if pat6 != "":
        if checkalpha(pat6) == 1:
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only alphabets for Name"
            )
            return
    if pat7 != "":
        if not pat7.isdigit() or int(pat7) > 125:
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only 1ess than 126 for Age"
            )
            return
    if pat9 != "":
        if not pat9.isdigit() or len(pat9) != 10:
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only 10 digit number for Phone number"
            )
            return
    if pat6 == "":
        pat6 = pd1
    if pat7 == "":
        pat7 = pd2
    if pat8 == "":
        pat8 = pd3
    if pat9 == "":
        pat9 = pd4
    if pat10 == "":
        pat10 = pd5
    now3 = datetime.datetime.today()
    cdate3 = now3.strftime("%d/%m/%Y")
    query3 = "update appointment set name='{}', age={}, gender='{}', phone={},bg='{}', udate='{}' where idno={}".format(
        pat6, pat7, pat8, pat9, pat10, cdate3, aadhar
    )
    cur.execute(query3)
    con.commit()
    tkinter.messagebox.showinfo("Information", "Your record is updated!")


# To check if room is available for Doctor / Service
def roomexists(rn):
    cur.execute("select room from doctor_details where room=%s" % rn)
    ar = cur.fetchall()
    if len(ar) == 0:
        return 0
    else:
        return 1


# Add Doctor - GUI
def doctoradd():
    global da1, da2, da3, da4, da5, da6, da7, cnt
    root5 = Tk()
    root5.title("Hospital Management System")
    label = Label(root5, text="Add Doctor", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root5, height=380, width=350)
    frame.pack()
    cur.execute("select count(*) from doctor_details")
    ar = cur.fetchall()
    for row in ar:
        cnt = row[0]
    cnt = cnt + 1
    l1 = Label(root5, text="Doctor Id")
    l1.place(x=40, y=80)
    da1 = Label(root5, text=cnt)
    da1.place(x=160, y=80, width=140)
    l2 = Label(root5, text="Name")
    l2.place(x=40, y=120)
    da2 = tkinter.Entry(root5)
    da2.place(x=160, y=120, width=140)
    l3 = Label(root5, text="Specialization")
    l3.place(x=40, y=160)
    da3 = tkinter.Entry(root5)
    da3.place(x=160, y=160, width=140)
    l4 = Label(root5, text="Room No.")
    l4.place(x=40, y=200)
    da4 = tkinter.Entry(root5)
    da4.place(x=160, y=200, width=140)
    l5 = Label(root5, text="Time")
    l5.place(x=40, y=240)
    da5 = ttk.Combobox(
        root5,
        values=[
            "6.00 AM to 10.00 PM",
            "8.00 AM to 10.00 AM",
            "9.00 AM to 11.00AM",
            "10.00 PM to 12.00 PM",
            "6.00 PM to 8.00 PM",
            "7.00 PM to 9.00 PM",
            "8.00 PM to 10.00PM",
        ],
        state="readonly",
    )
    da5.place(x=160, y=240, width=140)
    l6 = Label(root5, text="Phone")
    l6.place(x=40, y=280)
    da6 = tkinter.Entry(root5)
    da6.place(x=160, y=280, width=140)
    l7 = Label(root5, text="Fees")
    l7.place(x=40, y=320)
    da7 = tkinter.Entry(root5)
    da7.place(x=160, y=320, width=140)
    b1 = Button(
        root5,
        text="Submit",
        command=doctorsave,
        bg="light blue",
        font="cambria 10 bold",
    )
    b1.place(x=120, y=370)
    b3 = Button(
        root5,
        text="Close",
        command=root5.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=200, y=370)
    root5.resizable(False, False)


# Add Doctor - Save in Database
def doctorsave():
    global da1, da2, da3, da4, da5, da6, da7, da8, cnt, now4, cdate4
    ds2 = da2.get()
    ds3 = da3.get()
    ds4 = da4.get()
    ds5 = da5.get()
    ds6 = da6.get()
    ds7 = da7.get()
    da8 = "d"
    if ds2 == "" or ds3 == "" or ds4 == "" or ds5 == "" or ds6 == "" or ds7 == "":
        tkinter.messagebox.showinfo("Validation", "Please enter all the fields")
        return
    if checkalpha(ds2) == 1:
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only alphabets for Name"
        )
        return
    if checkalpha(ds3) == 1:
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only alphabets for Specialist"
        )
        return
    if not ds4.isdigit():
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only numeric value for Room No."
        )
        return
    if roomexists(ds4) == 1:
        tkinter.messagebox.showinfo(
            "Validation",
            "Room is already occupied. Please allot a different Room between 100 and 199",
        )
        return
    if ds4.isdigit():
        if int(ds4) < 100 or int(ds4) > 199:
            tkinter.messagebox.showinfo(
                "Validation", " Please allot a Room between 100 and 199"
            )
            return
    if not ds6.isdigit() or len(ds6) != 10:
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only 10 digit number for Phone number"
        )
        return
    if not ds7.isdigit():
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only numeric value for Fees"
        )
        return
    now4 = datetime.datetime.today()
    cdate4 = now4.strftime("%d/%m/%Y")
    query4 = 'insert into doctor_details values("{}","{}", "{}", "{}","{}","{}","{}","{}","{}")'.format(
        cnt, ds2, ds3, ds4, ds5, ds6, ds7, da8, cdate4
    )
    cur.execute(query4)
    con.commit()
    tkinter.messagebox.showinfo("Information", "Details are added!")


# Add Service - GUI
def serviceadd():
    global sa1, sa2, sa3, sa4, sa5, sa6, sa7, cnt
    root6 = Tk()
    root6.title("Hospital Management System")
    label = Label(root6, text="Add Service", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root6, height=380, width=350)
    frame.pack()
    cur.execute("select count(*) from doctor_details")
    ar = cur.fetchall()
    for row in ar:
        cnt = row[0]
    cnt = cnt + 1
    l1 = Label(root6, text="Service Id")
    l1.place(x=40, y=80)
    sa1 = Label(root6, text=cnt)
    sa1.place(x=160, y=80, width=140)
    l2 = Label(root6, text="Service Name")
    l2.place(x=40, y=120)
    sa2 = tkinter.Entry(root6)
    sa2.place(x=160, y=120, width=140)
    l3 = Label(root6, text="Sub Level")
    l3.place(x=40, y=160)
    sa3 = tkinter.Entry(root6)
    sa3.place(x=160, y=160, width=140)
    l4 = Label(root6, text="Room No.")
    l4.place(x=40, y=200)
    sa4 = tkinter.Entry(root6)
    sa4.place(x=160, y=200, width=140)
    l5 = Label(root6, text="Time")
    l5.place(x=40, y=240)
    sa5 = ttk.Combobox(
        root6,
        values=[
            "6.00 AM to 10.00 PM",
            "8.00 AM to 10.00 AM",
            "9.00 AM to 11.00 AM",
            "10.00 PM to 12.00 PM",
            "6.00 PM to 8.00 PM",
            "7.00 PM to 9.00 PM",
            "8.00 PM to 10.00 PM",
        ],
        state="readonly",
    )
    sa5.place(x=160, y=240, width=140)
    l6 = Label(root6, text="Phone")
    l6.place(x=40, y=280)
    sa6 = tkinter.Entry(root6)
    sa6.place(x=160, y=280, width=140)
    l7 = Label(root6, text="Charge")
    l7.place(x=40, y=320)
    sa7 = tkinter.Entry(root6)
    sa7.place(x=160, y=320, width=140)
    b1 = Button(
        root6,
        text="Submit",
        command=servicesave,
        bg="light blue",
        font="cambria 10 bold",
    )
    b1.place(x=120, y=370)
    b3 = Button(
        root6,
        text="Close",
        command=root6.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=200, y=370)
    root6.resizable(False, False)


# Add Service - Save in Database
def servicesave():
    global sa1, sa2, sa3, sa4, sa5, sa6, sa7, sa8, cnt, now5, cdate5
    ss2 = sa2.get()
    ss3 = sa3.get()
    ss4 = sa4.get()
    ss5 = sa5.get()
    ss6 = sa6.get()
    ss7 = sa7.get()
    sa8 = "s"
    if ss2 == "" or ss3 == "" or ss4 == "" or ss5 == "" or ss6 == "" or ss7 == "":
        tkinter.messagebox.showinfo("Validation", "Please enter all the fields")
        return
    if checkalpha(ss2) == 1:
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only alphabets for Name"
        )
        return
    if checkalpha(ss3) == 1:
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only alphabets for Specialist"
        )
        return
    if not ss4.isdigit():
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only numeric value for Room No."
        )
        return
    if roomexists(ss4) == 1:
        tkinter.messagebox.showinfo(
            "Validation",
            "Room is already occupied. Please allot a different Room between 200 and 299",
        )
        return
    if ss4.isdigit():
        if int(ss4) < 200 or int(ss4) > 299:
            tkinter.messagebox.showinfo(
                "Validation", " Please allot a Room between 200 and 299"
            )
            return
    if not ss6.isdigit() or len(ss6) != 10:
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only 10 digit number for Phone number"
        )
        return
    if not ss7.isdigit():
        tkinter.messagebox.showinfo(
            "Validation", "Please enter only numeric value for Fees"
        )
        return

    now5 = datetime.datetime.today()
    cdate5 = now5.strftime("%d/%m/%Y")
    query5 = 'insert into doctor_details values("{}","{}", "{}", "{}","{}","{}","{}","{}","{}")'.format(
        cnt, ss2, ss3, ss4, ss5, ss6, ss7, sa8, cdate5
    )
    cur.execute(query5)
    con.commit()
    tkinter.messagebox.showinfo("Information", "Details are added!")


# Modify Doctor - GUI 1
def doctorupdate():
    global ddd1, cnt
    root8 = Tk()
    root8.title("Hospital Management System")
    label = Label(root8, text="Modify Doctor", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root8, height=120, width=300)
    frame.pack()
    s1 = Label(root8, text="Doctor")
    s1.place(x=40, y=80)
    ddd1 = ttk.Combobox(root8, values=doctorservice(1), state="readonly")
    ddd1.place(x=120, y=80, width=140)
    b1 = Button(
        root8,
        text="Submit",
        command=doctordata,
        bg="light blue",
        font="cambria 10 bold",
    )
    b1.place(x=90, y=120)
    b3 = Button(
        root8,
        text="Close",
        command=root8.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=170, y=120)


# Modify Doctor / Service - GUI 2
def doctordata():
    global cnt, ddd1, dnm, dnp, ddn, dd1, dd2, dd3, dd4, dd5, du1, du3, du4, du5, du6, dd6, dd7, du7
    root8 = Tk()
    root8.title("Hospital Management System")
    label = Label(root8, text="Modify Doctor", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root8, height=350, width=480)
    frame.pack()
    dnm = ddd1.get()
    dnp = dnm.find(".", 1, 5)
    ddn = dnm[0:dnp]
    cur.execute("select * from doctor_details where dno=%s" % ddn)
    ar = cur.fetchall()
    for row in ar:
        dd1 = row[1]
        dd2 = row[2]
        dd3 = row[3]
        dd4 = row[4]
        dd5 = row[5]
        dd6 = row[6]
        dd7 = row[7]
    l2 = Label(root8, text="Doctor Id")
    l2.place(x=40, y=80)
    g1 = Label(root8, text=ddn)
    g1.place(x=160, y=80, width=140)
    l1 = Label(root8, text="Name")
    l1.place(x=40, y=120)
    g1 = Label(root8, text=dd1)
    g1.place(x=160, y=120, width=140)
    du1 = tkinter.Entry(root8)
    du1.place(x=300, y=120, width=140)
    l3 = Label(root8, text="Specialization")
    l3.place(x=40, y=160)
    g2 = Label(root8, text=dd2)
    g2.place(x=160, y=160, width=140)
    du3 = tkinter.Entry(root8)
    du3.place(x=300, y=160, width=140)
    l4 = Label(root8, text="Room No.")
    l4.place(x=40, y=200)
    g3 = Label(root8, text=dd3)
    g3.place(x=160, y=200, width=140)
    du4 = tkinter.Entry(root8)
    du4.place(x=300, y=200, width=140)
    l5 = Label(root8, text="Time")
    l5.place(x=40, y=240)
    g4 = Label(root8, text=dd4)
    g4.place(x=160, y=240, width=140)
    du5 = ttk.Combobox(
        root8,
        values=[
            "8.00 AM to 10.00 AM",
            "9.00 AM to 11.00 AM",
            "10.00 PM to 12.00 PM",
            "6.00 PM to 8.00 PM",
            "7.00 PM to 9.00 PM",
            "8.00 PM to 10.00 PM",
        ],
        state="readonly",
    )
    du5.place(x=300, y=240, width=140)
    l6 = Label(root8, text="Phone")
    l6.place(x=40, y=280)
    g5 = Label(root8, text=dd5)
    g5.place(x=160, y=280, width=140)
    du6 = tkinter.Entry(root8)
    du6.place(x=300, y=280, width=140)
    l7 = Label(root8, text="Fees")
    l7.place(x=40, y=320)
    g6 = Label(root8, text=dd6)
    g6.place(x=160, y=320, width=140)
    du7 = tkinter.Entry(root8)
    du7.place(x=300, y=320, width=140)
    b1 = Button(
        root8,
        text="Submit",
        command=savedoctor,
        bg="light blue",
        font="cambria 10 bold",
    )
    b1.place(x=160, y=360)
    b3 = Button(
        root8,
        text="Close",
        command=root8.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=240, y=360)


# Modify Doctor - Save in Database
def savedoctor():
    global du1, du3, du4, du5, du6, du7, cnt, now6, cdate6, dd1, dd2, dd3, dd4, dd5, dd6, dd7
    sd2 = du1.get()
    sd3 = du3.get()
    sd4 = du4.get()
    sd5 = du5.get()
    sd6 = du6.get()
    sd7 = du7.get()
    if sd2 != "":
        if checkalpha(sd2) == 1:
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only alphabets for Name"
            )
            return
    if sd3 != "":
        if checkalpha(sd3) == 1:
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only alphabets for Specialist"
            )
            return
    if sd4 != "":
        if not sd4.isdigit():
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only numeric value for Room No."
            )
            return
        if roomexists(sd4) == 1:
            tkinter.messagebox.showinfo(
                "Validation",
                "Room is already occupied. Please allot a different Room between 100 and 199",
            )
            return
        if sd4.isdigit():
            if int(sd4) < 100 or int(sd4) > 199:
                tkinter.messagebox.showinfo(
                    "Validation", " Please allot a Room between 100 and 199"
                )
                return
    if sd6 != "":
        if not sd6.isdigit() or len(sd6) != 10:
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only 10 digit number for Phone number"
            )
            return
    if sd7 != "":
        if not sd7.isdigit():
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only numeric value for Fees"
            )
            return
    if sd2 == "":
        sd2 = dd1
    if sd3 == "":
        sd3 = dd2
    if sd4 == "":
        sd4 = dd3
    if sd5 == "":
        sd5 = dd4
    if sd6 == "":
        sd6 = dd5
    if sd7 == "":
        sd7 = dd6
    now6 = datetime.datetime.today()
    cdate6 = now6.strftime("%d/%m/%Y")
    query6 = "update doctor_details set doctor='{}', specialist='{}', room='{}', time='{}',phone={}, amount={},udate='{}' where dno={}".format(
        sd2, sd3, sd4, sd5, sd6, sd7, cdate6, ddn
    )
    cur.execute(query6)
    con.commit()
    tkinter.messagebox.showinfo("Information", "Details are updated!")


# Modify Service - GUI 1
def serviceupdate():
    global cnt, sv1
    root9 = Tk()
    root9.title("Hospital Management System")
    label = Label(root9, text="Modify Service", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root9, height=120, width=300)
    frame.pack()
    s1 = Label(root9, text="Service")
    s1.place(x=40, y=80)
    sv1 = ttk.Combobox(root9, values=doctorservice(2), state="readonly")
    sv1.place(x=120, y=80, width=140)
    b1 = Button(
        root9,
        text="Submit",
        command=servicedata,
        bg="light blue",
        font="cambria 10 bold",
    )
    b1.place(x=90, y=120)
    b3 = Button(
        root9,
        text="Close",
        command=root9.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=170, y=120)


# Modify Service - GUI 2
def servicedata():
    global cnt, sv1, snm, svp, d1, sd1, sd2, sd3, sd4, sd5, su1, su3, su4, su5, su6, sno, sd6, sd7, su7
    root10 = Tk()
    root10.title("Hospital Management System")
    label = Label(root10, text="Modify Service", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root10, height=350, width=500)
    frame.pack()
    snm = sv1.get()
    svp = snm.find(".", 1, 5)
    sno = snm[0:svp]
    cur.execute("select * from doctor_details where dno=%s" % sno)
    ar = cur.fetchall()
    for row in ar:
        sd1 = row[1]
        sd2 = row[2]
        sd3 = row[3]
        sd4 = row[4]
        sd5 = row[5]
        sd6 = row[6]
        sd7 = row[7]
    l2 = Label(root10, text="Service Id")
    l2.place(x=40, y=80)
    g1 = Label(root10, text=sno)
    g1.place(x=160, y=80, width=140)
    l1 = Label(root10, text="Service Name")
    l1.place(x=40, y=120)
    g1 = Label(root10, text=sd1)
    g1.place(x=160, y=120, width=140)
    su1 = tkinter.Entry(root10)
    su1.place(x=300, y=120, width=140)
    l3 = Label(root10, text="Sub Level")
    l3.place(x=40, y=160)
    g2 = Label(root10, text=sd2)
    g2.place(x=160, y=160, width=140)
    su3 = tkinter.Entry(root10)
    su3.place(x=300, y=160, width=140)
    l4 = Label(root10, text="Room No.")
    l4.place(x=40, y=200)
    g3 = Label(root10, text=sd3)
    g3.place(x=160, y=200, width=140)
    su4 = tkinter.Entry(root10)
    su4.place(x=300, y=200, width=140)
    l5 = Label(root10, text="Time")
    l5.place(x=40, y=240)
    g4 = Label(root10, text=sd4)
    g4.place(x=160, y=240, width=140)
    su5 = ttk.Combobox(
        root10,
        values=[
            "8.00 AM to 10.00 AM",
            "9.00 AM to 11.00 AM",
            "10.00 PM to 12.00 PM",
            "6.00 PM to 8.00 PM",
            "7.00 PM to 9.00 PM",
            "8.00 PM to 10.00 PM",
        ],
        state="readonly",
    )
    su5.place(x=300, y=240, width=140)
    l6 = Label(root10, text="Phone")
    l6.place(x=40, y=280)
    g5 = Label(root10, text=sd5)
    g5.place(x=160, y=280, width=140)
    su6 = tkinter.Entry(root10)
    su6.place(x=300, y=280, width=140)
    l7 = Label(root10, text="Charge")
    l7.place(x=40, y=320)
    g6 = Label(root10, text=sd6)
    g6.place(x=160, y=320, width=140)
    su7 = tkinter.Entry(root10)
    su7.place(x=300, y=320, width=140)
    b1 = Button(
        root10,
        text="Submit",
        command=saveservice,
        bg="light blue",
        font="cambria 10 bold",
    )
    b1.place(x=180, y=360)
    b3 = Button(
        root10,
        text="Close",
        command=root10.destroy,
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=260, y=360)


# Modify Service - Save in Database
def saveservice():
    global su1, e2, su3, su4, su5, su6, su7, cnt, now7, cdate7, sd1, sd2, sd3, sd4, sd5, sd6, sd7
    sv2 = su1.get()
    sv3 = su3.get()
    sv4 = su4.get()
    sv5 = su5.get()
    sv6 = su6.get()
    sv7 = su7.get()
    if sv2 != "":
        if checkalpha(sv2) == 1:
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only alphabets for Name"
            )
            return
    if sv3 != "":
        if checkalpha(sv3) == 1:
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only alphabets for Specialist"
            )
            return
    if sv4 != "":
        if not sv4.isdigit():
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only numeric value for Room No."
            )
            return
        if roomexists(sv4) == 1:
            tkinter.messagebox.showinfo(
                "Validation",
                "Room is already occupied. Please allot a different Room between 200 and 299",
            )
            return
        if sv4.isdigit():
            if int(sv4) < 200 or int(sv4) > 299:
                tkinter.messagebox.showinfo(
                    "Validation", " Please allot a Room between 200 and 299"
                )
                return
    if sv6 != "":
        if not sv6.isdigit() or len(sv6) != 10:
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only 10 digit number for Phone number"
            )
            return
    if sv7 != "":
        if not sv7.isdigit():
            tkinter.messagebox.showinfo(
                "Validation", "Please enter only numeric value for Charge"
            )
            return
    if sv2 == "":
        sv2 = sd1
    if sv3 == "":
        sv3 = sd2
    if sv4 == "":
        sv4 = sd3
    if sv5 == "":
        sv5 = sd4
    if sv6 == "":
        sv6 = sd5
    if sv7 == "":
        sv7 = sd6
    now7 = datetime.datetime.today()
    cdate7 = now7.strftime("%d/%m/%Y")
    query7 = "update doctor_details set doctor='{}', specialist='{}', room='{}', time='{}',phone={},amount={},udate='{}' where dno={}".format(
        sv2, sv3, sv4, sv5, sv6, sv7, cdate7, sno
    )
    cur.execute(query7)
    con.commit()
    tkinter.messagebox.showinfo("Information", "Details are updated!")


def report1():
    global rp2, rp6, rpc0, rpc1, rpc2, rpc3, rpc4, rpc5
    if rp2 != "":
        rp6 = rp2.get()
    if rp6 == "":
        tkinter.messagebox.showerror("Error", "Please enter a valid Aadhar no.")
        return
    fileout = open(r"C:\Users\ssankari\Desktop\PatientDetailsReport.txt", "w+")
    head = "\t\t\t\t\t\tPatient details for Aadhar card no. " + rp6 + "\n"
    desn = "\t\t\t\t\t\t***************************************** " + "\n"
    fileout.write(head)
    fileout.write(desn)
    query9 = (
        "select distinct a.idno,name,age,gender,a.phone,bg from appointment a,appointment_details b where a.idno=b.idno and a.idno=%s"
        % rp6
    )
    cur.execute(query9)
    ar = cur.fetchall()
    if len(ar) == 0:
        tkinter.messagebox.showerror("Error", "No record found")
        return
    for row in ar:
        rpc0 = "\t\t\t\t\t\t\tAadhar No. - " + str(row[0]) + "\n"
        rpc1 = "\t\t\t\t\t\t\tName - " + str(row[1]) + "\n"
        rpc2 = "\t\t\t\t\t\t\tAge - " + str(row[2]) + "\n"
        rpc3 = "\t\t\t\t\t\t\tGender - " + str(row[3]) + "\n"
        rpc4 = "\t\t\t\t\t\t\tPhone - " + str(row[4]) + "\n"
        rpc5 = "\t\t\t\t\t\t\tBlood Group - " + str(row[5])
        fileout.write(rpc0)
        fileout.write(rpc1)
        fileout.write(rpc2)
        fileout.write(rpc3)
        fileout.write(rpc4)
        fileout.write(rpc5)
    fileout.close()
    tkinter.messagebox.showinfo(
        "Information",
        "PatientDetailsReport.txt is generated and is available in Desktop",
    )


# Admin Reports - GUI
def reportoptions():
    global rp2, rp3, rp4, rp5
    root12 = Tk()
    root12.title("Hospital Management System")
    label = Label(root12, text="Reports", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root12, height=250, width=510)
    frame.pack()
    k2 = Label(root12, text="Patient details for Aadhar Card No.")
    k2.place(x=40, y=80)
    rp2 = tkinter.Entry(root12)
    rp2.place(x=250, y=80, width=140, height=25)
    b1 = Button(
        root12,
        text="Report 1",
        command=report1,
        bg="light blue",
        font="cambria 10 bold",
    )
    b1.place(x=410, y=80)
    k3 = Label(root12, text="Patients visited Hospital on ")
    k3.place(x=40, y=120)
    rp3 = tc.DateEntry(root12, date_pattern="dd/mm/yyyy", year=2022, month=8, day=1)
    rp3.place(x=250, y=120, width=140, height=25)
    b2 = Button(
        root12,
        text="Report 2",
        command=lambda: reports(1),
        bg="light blue",
        font="cambria 10 bold",
    )
    b2.place(x=410, y=120)
    k4 = Label(root12, text="Patients visited Doctor ")
    k4.place(x=40, y=160)
    rp4 = ttk.Combobox(root12, values=doctorservice(1), state="readonly")
    rp4.place(x=250, y=160, width=140, height=25)
    rp4.set("Select")
    b3 = Button(
        root12,
        text="Report 3",
        command=lambda: reports(2),
        bg="light blue",
        font="cambria 10 bold",
    )
    b3.place(x=410, y=160)
    rdfn = Label(root12, text="Services availed")
    rdfn.place(x=40, y=200)
    rp5 = ttk.Combobox(root12, values=doctorservice(2), state="readonly")
    rp5.place(x=250, y=200, width=140, height=25)
    rp5.set("Select")
    b4 = Button(
        root12,
        text="Report 4",
        command=lambda: reports(3),
        bg="light blue",
        font="cambria 10 bold",
    )
    b4.place(x=410, y=200)
    k2 = Label(
        root12,
        text="* If Date remains 01/08/2022, it will not be considered for filtering",
        font="cambria 8",
    )
    k2.place(x=40, y=260)


# Admin Reports - Save in Desktop
def reports(r):
    global rp6, rp7, rdn, rd1, rp2, rp3, rp4, rpc0, rpc1, rpc2, rpc3, rpc4, rpc5, rpc6, rpc7, head, rp5, rsn, rs1, rsfn, rdp, rdno, rsp, rsno
    fileout = open(r"C:\Users\ssankari\Desktop\Report2.txt", "w+")
    query = "select a.idno,name,age,gender,a.phone,bg,b.date,doctor from appointment a,appointment_details b, doctor_details c where a.idno=b.idno and b.dno=c.dno"
    if r == 1:
        rp7 = rp3.get()
        query = query + " and b.date='%s'" % rp7
        head = "\t\t\t\t\t\tList of Patients visited on " + rp7 + "\n"
        des = "*" * (len(head) - 7)
        desn = "\t\t\t\t\t\t" + des + "\n"
        chead = "Aadhar Name Age Gender Phone BloodGroup Appointment Doctor\n"
    elif r == 2:
        rdn = rp4.get()
        rd1 = rdn[0]
        rdp = rdn.find(".", 1, 5)
        rdno = rdn[0:rdp]
        rdfn = rdn[2::]
        query = query + " and b.dno='%s'" % rdno
        head = "\t\t\t\t\t\tList of Patients visited Dr." + rdfn + "\n"
        des = "*" * (len(head) - 7)
        desn = "\t\t\t\t\t\t" + des + "\n"
        chead = "Aadhar Name Age Gender Phone BloodGroup Appointment Doctor\n"
    elif r == 3:
        rsn = rp5.get()
        rs1 = rsn[0]
        rsp = rsn.find(".", 1, 5)
        rsno = rsn[0:rsp]
        rsfn = rsn[2::]
        query = query + " and b.dno='%s'" % rsno
        head = "\t\t\t\t\t\tList of Patients availed " + rsfn + "\n"
        des = "*" * (len(head) - 7)
        desn = "\t\t\t\t\t\t" + des + "\n"
        chead = "Aadhar Name Age Gender Phone BloodGroup Appointment Service\n"
    fileout.write(head)
    fileout.write(desn)
    fileout.write(chead)
    cur.execute(query)
    ar = cur.fetchall()
    if len(ar) == 0:
        tkinter.messagebox.showerror("Error", "No record found")
        return
    for row in ar:
        rpc0 = row[0]
        rpc1 = row[1]
        rpc2 = row[2]
        rpc3 = row[3]
        rpc4 = row[4]
        rpc5 = row[5]
        rpc6 = row[6]
        rpc7 = row[7]
        rec = (
            str(rpc0)
            + "\t"
            + str(rpc1)
            + "\t\t"
            + str(rpc2)
            + "\t"
            + str(rpc3)
            + "\t"
            + str(rpc4)
            + "\t"
            + str(rpc5)
            + "\t\t"
            + str(rpc6)
            + "\t\t"
            + str(rpc7)
            + "\n"
        )
        fileout.write(rec)
        fileout.close()
        fileout = open(r"C:\Users\ssankari\Desktop\Report2.txt", "r+")
        fileout1 = open(r"C:\Users\ssankari\Desktop\Report.txt", "w+")
        fileout1.write(fileout.readline())
        fileout1.write(fileout.readline())
        fileout1.write("\n")
        lengths = [10, 20, 5, 8, 15, 13, 20, 20]
        for line in fileout:
            line = line.split()
        for field, fieldlength in zip(line, lengths):
            fileout1.write(field.ljust(fieldlength))
        fileout1.write("\n")
        fileout1.close
        fileout.close
        tkinter.messagebox.showinfo(
            "Information", "Report.txt is generated and is available in Desktop"
        )


# Reference data for Admin staff
def reference(ref):
    root13 = Tk()
    root13.title("Hospital Management System")
    label = Label(root13, text="Reference", font="cambria 25 bold", pady=10)
    label.pack()
    frame = Frame(root13, height=300, width=510)
    frame.pack()
    if ref == 1:
        l1 = Label(root13, text="Doctors list")
        l1.place(x=40, y=60)
        cur.execute("select * from doctor_details where category='d'")
    elif ref == 2:
        l1 = Label(root13, text="Services available")
        l1.place(x=40, y=60)
        cur.execute("select * from doctor_details where category='s'")
    ar = cur.fetchall()
    l2 = Label(root13, text="Name")
    l2.place(x=40, y=90)
    l3 = Label(root13, text="Specialization")
    l3.place(x=140, y=90)
    l2 = Label(root13, text="Room No.")
    l2.place(x=240, y=90)
    l3 = Label(root13, text="Available Time")
    l3.place(x=300, y=90)
    cntx = 40
    cnty = 120
    for row in ar:
        l2 = Label(root13, text=row[1])
        l2.place(x=cntx, y=cnty)
        l3 = Label(root13, text=row[2])
        l3.place(x=cntx + 100, y=cnty)
        l2 = Label(root13, text=row[3])
        l2.place(x=cntx + 200, y=cnty)
        l3 = Label(root13, text=row[4])
        l3.place(x=cntx + 260, y=cnty)
        cnty = cnty + 40


root = Tk()
root.title("Hospital Management System")
img = Image.open("hospital_image.png")
bg = ImageTk.PhotoImage(img)
root.geometry("1920x1080")
hospital_frame = Frame(root)
hospital_frame.pack(side=TOP)
ref = Button(
    root,
    text="Doctors",
    font="cambria 10 underline",
    bd=0,
    command=lambda: reference(1),
    fg="blue",
)
ref.place(x=1450, y=20)
ref = Button(
    root,
    text="Services",
    font="cambria 10 underline",
    bd=0,
    command=lambda: reference(2),
    fg="blue",
)
ref.place(x=1450, y=40)
title = Label(
    hospital_frame,
    text="Vivekananda Hospital",
    font="cambria 30 bold",
    fg="black",
    padx=600,
    pady=100,
)
title.grid(row=5, columnspan=2)
label1 = Label(root, image=bg)
label1.place(x=1030, y=100)
label_frame = Label(hospital_frame)
label_frame.grid(row=7, column=0, rowspan=1, columnspan=3, padx=10, pady=10)
title1 = Label(
    label_frame,
    text="Patient",
    font="cambria 18 bold",
    width=14,
    fg="black",
    padx=10,
    pady=10,
)
title1.grid(row=0, column=0, padx=10, pady=10)
title1 = Label(
    label_frame,
    text="Doctor",
    font="cambria 18 bold",
    width=14,
    fg="black",
    padx=7,
    pady=10,
)
title1.grid(row=0, column=1, padx=10, pady=10)
title1 = Label(
    label_frame,
    text="Service",
    font="cambria 18 bold",
    width=14,
    fg="black",
    padx=7,
    pady=10,
)
title1.grid(row=0, column=2, padx=10, pady=10)
btn_frame = Frame(hospital_frame)
btn_frame.grid(row=7, column=0, rowspan=2, columnspan=3, padx=10, pady=10)
btnRegister = Button(
    btn_frame,
    command=register,
    text="Registration",
    width=18,
    font="cambria 16 bold",
    fg="black",
    bg="light blue",
    bd=0,
).grid(row=1, column=0, padx=10, pady=10)
btnModPat = Button(
    btn_frame,
    command=lambda: get_aadhar(3),
    text="Modify Patient",
    width=18,
    font="cambria 16 bold",
    fg="black",
    bg="light blue",
    bd=0,
).grid(row=2, column=0, padx=10, pady=10)
btnAddDoc = Button(
    btn_frame,
    command=doctoradd,
    text="Add Doctor",
    width=18,
    font="cambria 16 bold",
    fg="black",
    bg="light blue",
    bd=0,
).grid(row=1, column=1, padx=10, pady=10)
btnModDoc = Button(
    btn_frame,
    command=doctorupdate,
    text="Modify Doctor",
    width=18,
    font="cambria 16 bold",
    fg="black",
    bg="light blue",
    bd=0,
).grid(row=2, column=1, padx=10, pady=10)
btnAddSer = Button(
    btn_frame,
    command=serviceadd,
    text="Add Service",
    width=18,
    font="cambria 16 bold",
    fg="black",
    bg="light blue",
    bd=0,
).grid(row=1, column=2, padx=10, pady=10)
btnModSer = Button(
    btn_frame,
    command=serviceupdate,
    text="Modify Service",
    width=18,
    font="cambria 16 bold",
    fg="black",
    bg="light blue",
    bd=0,
).grid(row=2, column=2, padx=10, pady=10)
btn_frame1 = Frame(hospital_frame)
btn_frame1.grid(row=11, column=0, rowspan=1, columnspan=2, padx=10, pady=10)
btnBkApp = Button(
    btn_frame1,
    command=lambda: get_aadhar(1),
    text="Book Appointment",
    width=18,
    font="cambria 16 bold",
    fg="black",
    bg="light blue",
    bd=0,
).grid(row=1, column=0, padx=10, pady=10)
btnBook = Button(
    btn_frame1,
    command=reportoptions,
    text="Admin Reports",
    width=18,
    font="cambria 16 bold",
    fg="black",
    bg="light blue",
    bd=0,
).grid(row=1, column=1, padx=10, pady=10)
btn_frame2 = Frame(hospital_frame)
btn_frame2.grid(row=12, rowspan=1, columnspan=3, padx=10, pady=10)
btnView = Button(
    btn_frame2,
    command=root.destroy,
    text="Exit",
    width=18,
    font="cambria 16 bold",
    fg="black",
    bg="light blue",
    bd=0,
).grid(row=1, column=2, padx=10, pady=10)
