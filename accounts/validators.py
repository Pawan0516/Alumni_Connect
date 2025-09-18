from django.core.exceptions import ValidationError
import re

def validate_phone(phone:str)->bool:
    phone = phone.strip()
    if len(phone) == 10 and phone.isnumeric():
        return phone

    else:
        raise ValidationError("Invalid Phone Number")

def validate_college(college:str)->bool:
    college = college.strip()
    if len(college)>=3:
        return college

    else:
        raise ValidationError("College name atleast 3 letters long")

def validate_gender(gender:str)->bool:
    gender = gender.strip()
    if gender in ('m', 'f', 'x'):
        return gender

    else:
        raise ValidationError("Invalid Gender, require ('m','f','x')")

def validate_email(email:str)->bool:
    email = email.strip().lower()
    pattern1 = r'[\.\@\-]{2,}'
    pattern2 = r'^[a-z][a-z\.\d]{1,}[a-z\d]\@(?:[a-z]|[a-z][a-z\d\-]{0,}[a-z\d]{1,})\.((?:[a-z]{2,}[\.\-]{0,1}[a-z]{2,}|[a-z]{2,}))$'

    if re.search(pattern1, email) is not None or re.search(pattern2, email) is None:
        raise ValidationError("Invalid Email Address")

    return email

def validate_password(password:str)->bool:
    password = password.strip()
    pattern1 = r'^[a-zA-Z0-9\@\$\^\(\)\?\~\.\/]{8,}$'

    def invalid_password():
        raise ValidationError("Password length must be 8 to 30 long and contain alphanumeric (a-z, A-Z, 0-9) and @, !, $, %, ^, &, *, (, ), +, -, ?, /")

    if re.search(pattern1, password) is None:
        invalid_password()

    pattern2 = r'[A-Z]+'
    pattern3 = r'[a-z]+'
    pattern4 = r'[0-9]+'
    pattern5 = r'[\@\$\^\(\)\?\~\.\/\&\*\+\-]+'

    if re.search(pattern2, password) is None:
        invalid_password()
    if re.search(pattern3, password) is None:
        invalid_password()
    if re.search(pattern4, password) is None:
        invalid_password()
    if re.search(pattern5, password) is None:
        invalid_password()

    return password

def validate_first_name(first_name:str)->bool:
    first_name = first_name.strip().lower()
    if first_name.isalpha() and len(first_name) >= 3:
        return first_name

    raise ValidationError("First Name must be alphabetical and minimum of 3 character")

def validate_last_name(last_name:str)->bool:
    last_name = last_name.strip().lower()
    if last_name.isalpha():
        return last_name
    
    pattern1 = r'\s{2,}'
    pattern2 = r'^[a-z\s]{3,}$'
    if re.search(pattern1, last_name) is None and re.search(pattern2, last_name) is not None:
        return last_name

    raise ValidationError("Remove extra spaces or number from Last Name")
