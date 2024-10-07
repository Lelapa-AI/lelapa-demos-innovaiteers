import os
import csv
import smtplib
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders


# not used
def save_car_details(
    car_model: str,
    car_make: str,
    car_year: int,
    client_name: str,
    client_number: str,
    client_email: str,
) -> bool:
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
        with open("car_details.csv", "a", newline="") as file:
            writer = csv.writer(file)
            # Write the car details, client name, number, and email to the CSV file
            writer.writerow(
                [
                    car_model,
                    car_make,
                    car_year,
                    client_name,
                    client_number,
                    client_email,
                ]
            )
        return True
    except Exception as e:
        print(f"An error occurred while saving car details: {e}")
        return False


def connect_with_agent(
    client_email: str,
    client_name: str,
    client_number: str,
    insurance_type: str,
    item: str,
) -> bool:

    print("Connecting with agent...")
    print("Sending email to client...")
    print(f"{client_email} : {client_name} : {insurance_type} : {item}")
    """Connects client with an agent for further quotation.

    Args:
        client_email (str): The recipient's email address (e.g., 'recipient@example.com').
        client_name (str): The name of the client (e.g., 'John Doe').
        client_number (str): The contact number of the client (e.g., '123-456-7890').
        insurance_type (str): The type of insurance (e.g., 'Car', 'Home', 'Belongings').
        item (str): the item details of the item being insured depending on the insurance type.(e.g.,'volkswagen polo' , '2000m2 home', 'Samsung laptop')

    Returns:
        bool: True if the email was sent successfully, otherwise False.
    """
    try:
        insurance_details = "Insurance Nje"
        # Build message content based on insurance type

        if insurance_type.lower() == "car" or "car" in insurance_type.lower():
            insurance_details = f"Insurance for {item}"

        elif insurance_type.lower() == "home" or "home" in insurance_type.lower():
            insurance_details = f"Home Insurance for property located at {item}"

        elif (
            insurance_type.lower() == "personal belongings insurance"
            or "belongings" in insurance_type.lower()
        ):
            insurance_details = f"Insurance for personal belongings: {item}"

        else:
            insurance_details = "Insurance details"

        # Create the message body
        message = f"""

Dear {client_name},

Thank you for using QuoteBuddy to obtain your insurance quote! We are pleased to provide you with a detailed estimate for the coverage you're looking for.

Attached to this email, you will find a copy of your quote.

Here is a summary of the information you provided:
{insurance_details}

An insurance agent will be contacting you within 2-3 business days to discuss your quote in more detail and assist you with any further questions or adjustments to the coverage. We are committed to providing you with personalized service to ensure your needs are fully met.

If you would like to make any changes to the details or have any immediate questions, feel free to respond to this email, and we will be happy to assist.

Thank you for choosing QuoteBuddy for your insurance needs!

Best regards,  
QuoteBuddy Team  
+ 1 415 523 8886  
Qoutelynx by Innovaiteers

"""
        send_email(
            message,
            f"Quotation for {client_name} - {insurance_type} Insurance",
            client_email,
        )
        send_sms(client_name,client_number)
        print("Email sent :)")
        return True

    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        return False


def send_email(message, subject, email):
    # Sender email creds
    admin_email = "teamqoutebuddy@gmail.com"
    password = "chpuwonpdfjyjefe"

    # starting server and connecting to gmail
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(admin_email, password)

        server.sendmail(
            from_addr=admin_email,
            to_addrs={email},
            msg=f"Subject: {subject} \n\n{message}",
        )


def send_sms(username, number):
    message = f"""
Hi {username}, we’ve received your insurance inquiry. Please check your email for more details and next steps. If you have any questions contact us at +18154585391. Thank you for choosing QuoteBuddy!"""

    account_sid = os.getenv("SMS_SID")
    auth_token = os.getenv("SMS_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(from_="+18154585391", body=message, to=number)

    print("Message successfully sent")