from tkinter import *
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import messagebox
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tkinter import ttk

root = tk.Tk()
root.geometry("1200x700")
root.resizable(0, 0)
root.title("Registration Form")


reg = Frame(root)
# Create form input fields
name_var = tk.StringVar()
email_var = tk.StringVar()
phone_var = tk.StringVar()
event_name_var = tk.StringVar()
teammate_name_var = tk.StringVar()
college_name_var= tk.StringVar()
amount_pay_var = tk.StringVar()
payment_status_var= tk.StringVar()

conn = sqlite3.connect('comman.db')
with conn:
    cursor = conn.cursor()
def database():
    name = name_var.get()
    email = email_var.get()
    phone = phone_var.get()
    event_name = event_name_var.get()
    teammate_name = teammate_name_var.get()
    college_name = college_name_var.get()
    amount_pay = amount_pay_var.get()
    payment_status = payment_status_var.get()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Student (
        name TEXT,
        email TEXT,
        phone TEXT,
        event_name TEXT,
        teammate_name TEXT,
        college_name TEXT,
        amount_pay TEXT,
        payment_status TEXT

    )
    """)
    cursor.execute('INSERT INTO Student (name,email,phone,event_name,teammate_name,college_name,amount_pay,payment_status) VALUES(?,?,?,?,?,?,?,?)',
                   (name,email,phone,event_name,teammate_name,college_name,amount_pay,payment_status))
    conn.commit()
    showinfo(title="Student Reacord", message="Data inserted sucessfully")
    # Add registration to database

    # Generate PDF file
    generate_pdf(name, email, phone, event_name, teammate_name, college_name, amount_pay, payment_status)

    # Send email with PDF attachment
    send_email(email, f"{name}.pdf")

    # Show success message
    messagebox.showinfo("Registration Form", "Registration submitted successfully!")
def generate_pdf(name, email, phone,event_name,teammate_name,college_name,amount_pay,payment_status):
    # Create a new PDF file
    pdf_file = canvas.Canvas(f"{name}.pdf", pagesize=letter)

    # Add text to the PDF file
    pdf_file.drawString(100, 750, "Registration Form")
    pdf_file.drawString(100, 700, f"Name: {name}")
    pdf_file.drawString(100, 650, f"Email: {email}")
    pdf_file.drawString(100, 600, f"Phone: {phone}")
    pdf_file.drawString(100, 550, f"event_name: {event_name}")
    pdf_file.drawString(100, 500, f"teammate_name: {teammate_name}")
    pdf_file.drawString(100, 450, f"college_name: {college_name}")
    pdf_file.drawString(100, 400, f"amount_pay: {amount_pay}")
    pdf_file.drawString(100, 350, f"payment_status: {payment_status}")
    pdf_file.drawString(100, 300, f"THANKS FOR REGESTRARION FOR MCA EVENT AT SONA COLLEGE OF TECHNOLOGY")

    # Save the PDF file
    pdf_file.save()
# Define function to send email with PDF attachment
def send_email(to, pdf_file):
    # Set up email details
    subject = "Registration Form"
    body = "Please find attached the registration form."

    # Create a new email message
    message = MIMEMultipart()
    message["Subject"] = subject
    message["To"] = to

    # Add email body
    text = MIMEText(body)
    message.attach(text)

    # Add PDF attachment
    with open(pdf_file, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="pdf")
        attachment.add_header(
            "Content-Disposition", "attachment", filename=pdf_file
        )
        message.attach(attachment)

    # Send email
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "cyberking023@gmail.com"
    smtp_password = "pdxylmzoesbatnes"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to, message.as_string())

def display():
    cursor.execute('SELECT * FROM Student')
    data = cursor.fetchall()
    print(data)
    output = ''
    for x in data:
        output = output + x[0] + '  ' + x[1] + '  ' + x[2] + '  ' + x[3] + '  ' + x[4] + '\n'
    print(output)
    return output
def delete(conn, task):
    sql = 'DELETE FROM Student WHERE name =?'
    cursor = conn.cursor()
    cursor.execute(sql, task)
    conn.commit()
    showinfo(title="Student Reacord", message="Data deleted sucessfully")
def update(task):
    sql = 'UPDATE Student SET email=?, phone=?, event_name=?, college_name=?  teammate_name=?, amount_pay=?, payment_status=?WHERE name = ?'
    cursor.execute(sql, task)
    conn.commit()
    showinfo(title="Student Reacord", message="Data updated sucessfully")

def main():
    name = name_var.get()
    email = email_var.get()
    phone = phone_var.get()
    event_name = event_name_var.get()
    teammate_name = teammate_name_var.get()
    college_name = college_name_var.get()
    amount_pay = amount_pay_var.get()
    payment_status = payment_status_var.get()
    update(name,email,phone,event_name,teammate_name,college_name,amount_pay,payment_status)
def delete_task():
    database = r"Form.db"
    conn = sqlite3.connect(database)
    name = name_var.get()
    with conn:
        delete_task(conn, name,)
canvas1 = tk.Canvas(root, width=1000, height=500, relief='raised', bg="white")
canvas1.pack()
label1 = tk.Label(root, text='Registration Form')
label1.config(font=("bold", 18), bg="white")
canvas1.create_window(250, 30, window=label1)

label2 = tk.Label(root, text='name :')
label2.config(font=('helvetica', 14), bg="white")
canvas1.create_window(65, 90, window=label2)
entry1 = tk.Entry(root, textvar=name_var, font=(14), borderwidth=2, width=30)
canvas1.create_window(320, 90, window=entry1)

label3 = tk.Label(root, text='E-mail :')
label3.config(font=('helvetica', 14), bg="white")
canvas1.create_window(65, 140, window=label3)
entry2 = tk.Entry(root, textvar=email_var, font=(14), borderwidth=2, width=30)
canvas1.create_window(320, 140, window=entry2)

label3 = tk.Label(root, text='number :')
label3.config(font=('helvetica', 14), bg="white")
canvas1.create_window(65, 190, window=label3)
entry2 = tk.Entry(root, textvar=phone_var, font=(14), borderwidth=2, width=30)
canvas1.create_window(320, 190, window=entry2)

label3 = tk.Label(root, text='event name:')
label3.config(font=('helvetica', 14), bg="white")
canvas1.create_window(65, 240, window=label3)
entry2 = tk.Entry(root, textvar=event_name_var, font=(14), borderwidth=2, width=30)
canvas1.create_window(320, 240, window=entry2)

label3 = tk.Label(root, text='temmate  name:')
label3.config(font=('helvetica', 14), bg="white")
canvas1.create_window(65, 290, window=label3)
entry2 = tk.Entry(root, textvar=teammate_name_var, font=(14), borderwidth=2, width=30)
canvas1.create_window(320, 290, window=entry2)

label3 = tk.Label(root, text='college  name:')
label3.config(font=('helvetica', 14), bg="white")
canvas1.create_window(65, 340, window=label3)
entry2 = tk.Entry(root, textvar=college_name_var, font=(14), borderwidth=2, width=30)
canvas1.create_window(320, 340, window=entry2)

label3 = tk.Label(root, text='amount pay  :')
label3.config(font=('helvetica', 14), bg="white")
canvas1.create_window(65, 390, window=label3)
entry2 = tk.Entry(root, textvar=amount_pay_var, font=(14), borderwidth=2, width=30)
canvas1.create_window(320, 390, window=entry2)

label3 = tk.Label(root, text='amount status  :')
label3.config(font=('helvetica', 14), bg="white")
canvas1.create_window(65, 440, window=label3)
entry2 = tk.Entry(root, textvar=payment_status_var, font=(14), borderwidth=2, width=30)
canvas1.create_window(320, 440, window=entry2)





button1 = tk.Button(text='   Submit   ', command=database, bg='black', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(230, 490, window=button1)

button2 = tk.Button(text='   Display   ', command=lambda: (text.delete(1.0, END), text.insert(END, display())),
                    bg='black', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(330, 490, window=button2)

button3 = tk.Button(text='   Update   ', command=main, bg='black', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(130, 490, window=button3)

button4 = tk.Button(text='   Delete   ', command=delete_task, bg='black', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(430, 490, window=button4)

text = tk.Text(root, height=25, width=50)
text.config(font=('helvetica', 12), bg="white")
canvas1.create_window(750, 270, window=text)

lblDisplay = tk.Label(root, text="Student Data")
lblDisplay.config(font=('Helvetica', 18, 'bold'), fg='black', justify=CENTER, bg="white")
canvas1.create_window(750, 25, window=lblDisplay)


def iExit():
    iExit = tkinter.messagebox.askyesno("Scientific Calculator", "Do you want to exit ?")
    if iExit > 0:
        root.destroy()
        return


def Data():
    root.resizable(width=True, height=True)
    root.geometry("1100x700+0+0")


def Form():
    root.resizable(width=True, height=True)
    root.geometry("1200x800+0+0")


menubar = Menu(reg)

filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label="Form", command=Form)
filemenu.add_command(label="Data", command=Data)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=iExit)
root.config(menu=menubar)



mainloop()
