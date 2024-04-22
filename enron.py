# Import required modules
import re
import argparse
import sys

# Define a class to store email details
class Email:
    def __init__(self, message_id, date, subject, sender, receiver, body):
        self.message_id = message_id
        self.date = date
        self.subject = subject
        self.sender = sender
        self.receiver = receiver
        self.body = body

# Define a class to handle email processing
class Server:
    def __init__(self, path):
        self.emails = []
        try:
            with open(path, 'r') as file:
                data = file.read()
                emails = data.split("End Email")  # Split the data into separate emails
                for email in emails:
                    if email.strip():  # Check if the email is not just whitespace
                        self.process_email(email)
        except Exception as e:
            print(f"Error reading file or processing emails: {e}")

    def process_email(self, email):
        try:
            fields = {
                "message_id": r'Message-ID: (.+?)\n',
                "date": r'Date: (.+?)\n',
                "subject": r'Subject: (.*?)\n',  # Non-greedy match for subject (may be empty)
                "sender": r'From: (.+?)\n',
                "receiver": r'To: (.+?)\n',
                "body": r'\n\n(.+)'  # Assumes body starts after two newlines
            }
            extracted = {}
            for key, pattern in fields.items():
                match = re.search(pattern, email, re.DOTALL)
                if match:
                    extracted[key] = match.group(1).strip()
                else:
                    print(f"Missing {key} in email.")
                    return  # Skip this email if any field is missing
            self.emails.append(Email(**extracted))
        except re.error as e:
            print(f"Regex error: {e}")

# Define a function to parse command-line arguments
def parse_args(args_list):
    parser = argparse.ArgumentParser(description="Parse Enron emails.")
    parser.add_argument('path', type=str, help='The path to the text file to be parsed.')
    return parser.parse_args(args_list)

# Define the main function that initializes the server and counts processed emails
def main(path):
    server = Server(path)
    return len(server.emails)

# Entry point for the script, processes command line arguments and prints the total number of emails
if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    print(f"Total emails processed: {main(args.path)}")

