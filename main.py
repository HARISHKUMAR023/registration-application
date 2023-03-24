import tkinter as tk
from tkinter import messagebox
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tkinter import ttk



# Set up database connection
conn = sqlite3.connect("registration.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY,
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
conn.commit()

# Define function to add new registration
def add_registration(name, email, phone,event_name,teammate_name,college_name,amount_pay,payment_status):
    cursor.execute("""
    INSERT INTO registrations (name, email, phone,event_name,teammate_name,college_name,amount_pay,payment_status) VALUES (?, ?, ?,?, ?, ?,?, ?)
    """, (name, email, phone,event_name,teammate_name,college_name,amount_pay,payment_status))
    conn.commit()

# Define function to generate PDF file
def generate_pdf(name, email, phone,event_name,teammate_name,college_name,amount_pay,payment_status):
    # Create a new PDF file
    pdf_file = canvas.Canvas(f"{name}.pdf", pagesize=letter)

    # Add text to the PDF file
    pdf_file.drawString(100, 750, "Registration Form")
    pdf_file.drawString(100, 700, f"Name: {name}")
    pdf_file.drawString(100, 650, f"Email: {email}")
    pdf_file.drawString(100, 600, f"Phone: {phone}")
    pdf_file.drawString(100, 600, f"event_name: {event_name}")
    pdf_file.drawString(100, 600, f"teammate_name: {teammate_name}")
    pdf_file.drawString(100, 600, f"college_name: {college_name}")
    pdf_file.drawString(100, 600, f"amount_pay: {amount_pay}")
    pdf_file.drawString(100, 600, f"payment_status: {payment_status}")
    pdf_file.drawString(100, 600, f"THANKS FOR REGESTRARION FOR MCA EVENT AT SONA COLLEGE OF TECHNOLOGY")

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
#display data
# def display():
#     cursor.execute('SELECT * FROM registrations')
#     data = cursor.fetchall()
#     print(data)
#     output = ''
#     for x in data:
#         output = output + x[0] + '  ' + x[1] + '  ' + x[2] + '  ' + x[3] + '  ' + x[4] + '\n'
#     print(output)
#     return output

# Define function to handle form submission
def submit_form():
    # Get user input
    name = name_var.get()
    email = email_var.get()
    phone = phone_var.get()
    event_name = event_name_var.get()
    teammate_name = teammate_name_var.get()
    college_name = college_name_var.get()
    amount_pay = amount_pay_var.get()
    payment_status= payment_status_var.get()

    # Add registration to database
    add_registration(name, email, phone,event_name,teammate_name,college_name,amount_pay,payment_status)

    # Generate PDF file
    generate_pdf(name, email, phone,event_name,teammate_name,college_name,amount_pay,payment_status)

    # Send email with PDF attachment
    send_email(email, f"{name}.pdf")

    # Show success message
    messagebox.showinfo("Registration Form", "Registration submitted successfully!")
#display box
# lblDisplay = tk.Label(root, text="Student Data")
# lblDisplay.config(font=('Helvetica', 18, 'bold'), fg='black', justify=CENTER, bg="white")
# canvas1.create_window(750, 25, window=lblDisplay)
# Set up GUI
root = tk.Tk()
root.geometry("240x100")
root.title("Registration Form")

# configure the grid

#display
def display_registrations():
    # Create a new tkinter window
    display_window = tk.Toplevel(root)
    display_window.title("Registrations")

    # Create table to display registrations
    tree = ttk.Treeview(display_window)
    tree["columns"] = ("Name", "Email", "Phone","event_name","teammate_name","college_name","amount_pay","payment_status")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Name", width=150)
    tree.column("Email", width=200)
    tree.column("Phone", width=150)
    tree.column("event_name", width=200)
    tree.column("teammate_name", width=200)
    tree.column("college_name", width=200)
    tree.column("amount_pay", width=200)
    tree.column("payment_status", width=200)
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Phone", text="Phone")
    tree.heading("event_name",text="event_name" )
    tree.heading("teammate_name",text="teammate_name" )
    tree.heading("college_name",text="college_name")
    tree.heading("amount_pay",text="amount_pay" )
    tree.heading("payment_status",text="payment_status" )

    # Retrieve data from database
    cursor.execute("SELECT * FROM registrations")
    rows = cursor.fetchall()

    # Populate table with data
    for row in rows:
        tree.insert("", tk.END, text="", values=(row[1], row[2], row[3],row[4], row[5], row[6],row[7], row[8]))

    # Pack the tree view
    tree.pack()
display_button = tk.Button(root, text="Display Registrations", command=display_registrations)
display_button.grid(row=3, column=0)


# Create form labels
name_label = tk.Label(root, text="Name:")
email_label = tk.Label(root, text="Email:")
phone_label = tk.Label(root, text="Phone:")
event_name_label = tk.Label(root, text="event_name:")
teammate_name_label = tk.Label(root, text="teammate_name")
college_name_label= tk.Label(root, text="college_name")
amount_pay_label = tk.Label(root, text="amount_pay")
payment_status_label= tk.Label(root, text="payment_status")

# Create form input fields
name_var = tk.StringVar()
email_var = tk.StringVar()
phone_var = tk.StringVar()
event_name_var = tk.StringVar()
teammate_name_var = tk.StringVar()
college_name_var= tk.StringVar()
amount_pay_var = tk.StringVar()
payment_status_var= tk.StringVar()

name_entry = tk.Entry(root, textvariable=name_var)
email_entry = tk.Entry(email_label, textvariable=email_var)
phone_entry = tk.Entry(phone_label, textvariable=phone_var)
event_name_entry = tk.Entry(event_name_label, textvariable=event_name_var)
teammate_name_entry = tk.Entry(teammate_name_label, textvariable=teammate_name_var )
college_name_entry = tk.Entry(college_name_label, textvariable=college_name_var)
amount_pay_entry = tk.Entry(amount_pay_label, textvariable=amount_pay_var)
payment_status_entry = tk.Entry(payment_status_label, textvariable=payment_status_var)

submit_button = tk.Button(root, text="Submit", command=submit_form)
# name_label.grid(row=0, column=0)
# name_entry.grid(row=0, column=1)
# email_label.grid(row=0, column=1)
# email_entry.grid(row=1, column=1)
# phone_label.grid(row=0, column=2)
# phone_entry.grid(row=2, column=1)
# submit_button.grid(row=3, column=1)
# Display registration details

root.mainloop()