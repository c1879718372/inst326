#Bruce Reyes Tongkai Chen
import re

"""creates values that are set to attributes which are taken from intances 
    that addresses are created"""
class Address:
    def __init__(self, street, city, state):
        self.street = street
        self.city = city
        self.state = state

"""will have four attributes that relate to an employee
    created by passing in a row of a file when an instance of employee is created
    name will be taken from parse name
    address will be taken by parse_address
    email taken from parse email"""
class Employee:
    def __init__(self, text):
        self.first_name, self.last_name = parse_name(text)
        self.address = parse_address(text)
        self.email = parse_email(text)

"""Uses regular expressions to get the first and last name of person"""
def parse_name(text):
    name_part = re.split(r'\d', text, 1)[0].strip()
    names = name_part.split()
    if len(names) > 1:
        first_name = ' '.join(names[:-1])  # First name could be a compound name
        last_name = names[-1] 
        return first_name, last_name
    return None, None

"""returns address by using the street city and state that is identified
    it will use regular experessions as well"""
def parse_address(text):
    pattern = r"(\d+.*?)\s([A-Za-z_]+)\s([A-Z]{2})\s"
    match = re.search(pattern, text)
    if match:
        return Address(match.group(1), match.group(2).replace('_', ' '), match.group(3))
    return None

"""gets the email of person using regular expression"""
def parse_email(text):
    pattern = r"\s([^\s]+@[^\s]+)$"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None

"""creates path to file that is being parsed"""
def main(path):
    employee_list = []
    with open(path, 'r') as file:
        for line in file:
            employee = Employee(line.strip())
            employee_list.append(employee)
    return employee_list

"""returns returned value of people.txt"""
if __name__ == "__main__":
    employee_list = main("/mnt/data/people.txt")
    for employee in employee_list:
        print(employee)