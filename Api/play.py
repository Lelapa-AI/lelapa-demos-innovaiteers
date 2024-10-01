import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def save_car_details(car_model: str, car_make: str, car_year: int, client_name: str, client_number: str, client_email: str) -> bool:
    
    """Save the details of a car and the associated client information.

    Args:
        car_model (str): The model of the car (e.g., 'Model S', 'Civic').
        car_make (str): The manufacturer of the car (e.g., 'Tesla', 'Honda').
        car_year (int): The year the car was manufactured (e.g., 2020).
        client_name (str): The name of the client (e.g., 'John Doe').
        client_number (str): The contact number of the client (e.g., '123-456-7890').
        client_email (str): The email address of the client (e.g., 'john.doe@example.com').

    Returns:
        bool: True if the details were saved successfully, otherwise False.
    """
    try:
        # Open the CSV file in append mode
        with open('car_details.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # Write the car details, client name, number, and email to the CSV file
            writer.writerow([car_model, car_make, car_year, client_name, client_number, client_email])
        return True
    except Exception as e:
        print(f"An error occurred while saving car details: {e}")
        return False




def connect_with_agent(client_email: str, client_name: str, client_number: str, car_make: str, car_model: str) -> bool:
    print("Connecting with agent...")
    print("Sending email to client...")
    """Connects client with an agent for further quotation.

    Args:
        client_email (str): The recipient's email address (e.g., 'recipient@example.com').
        client_name (str): The name of the client (e.g., 'John Doe').
        client_number (str): The contact number of the client (e.g., '123-456-7890').
        car_make (str): The manufacturer of the car (e.g., 'Tesla').
        car_model (str): The model of the car (e.g., 'Model S').
        

    Returns:
        bool: True if the email was sent successfully, otherwise False.
    """
    try:
        # Create a multipart email message
        msg = MIMEMultipart()
        sender_email = ''
        sender_password = ''
        msg['From'] = sender_email
        msg['To'] = client_email
        msg['Subject'] = f"Quotation for {client_name} - {car_make} {car_model}"

        # Create the message body
        message = f"Hello {client_name},\n\nThank you for your inquiry about the {car_make} {car_model}.\n\nPlease feel free to contact us at {client_number} for further assistance.\n\nBest regards,\nYour Company Name"

        # Attach the message body to the email
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to the SMTP server
        with smtplib.SMTP('smtp.example.com', 587) as server:  # Replace with your SMTP server
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(sender_email, sender_password)  # Log in to the sender's email account
            server.send_message(msg)  # Send the email
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        return False


def send_email(flights):
    flight_deals = ''
    for i in flights:
        flight_deals += f"{i['DEST']}:R{round(i['bestprice'],1)}\n"

    admin_email = "teamcodeclinics@gmail.com"
    password = "npfekqklfoafhexm"

    # starting server and connecting to gmail
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(admin_email,password)

        server.sendmail(from_addr=admin_email,to_addrs='kkndlovu9@gmail.com',msg=f"subject: Flight Deals!\n\n{flight_deals} some great deals right")

    print("email sent :)")
        