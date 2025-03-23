"""
pm_objects.py
(Project Manager)

GUI Project Manager software that stores data into a database

Last modified 12/5/2020
"""

import re


def verify_first_name(first: str):
    """
    Validates first name

    :param first: user supplied field
    :return:
        first - validated first name
    """

    reg_exp = '^[A-Z][a-zA-Z]*$'
    first = first.strip()
    if re.search(reg_exp, first):
        return first
    else:
        raise TypeError('Not a valid first name')


def verify_last_name(last: str):
    """
    Validates last name

    :param last: user supplied field
    :return:
        last - validated last name
    """

    reg_exp = '^[a-zA-Z]+([\'-][a-zA-Z]+)*$'
    last = last.strip()
    if re.search(reg_exp, last):
        return last
    else:
        raise TypeError('Not a valid last name')


def verify_email(email: str):
    """
    Validates email address

    :param email: user supplied field
    :return:
        email - validated email address
    """

    reg_exp = '^[a-z0-9]+[\\._]?[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$'
    email = email.strip().lower()
    if re.search(reg_exp, email):
        return email
    else:
        raise TypeError('Not a valid email')


def verify_phone(phone: str):
    """
    Validates and transforms phone number into standard notation

    :param phone: user supplied field
    :return:
        phone - validated and standardized phone number
    """

    phone = re.sub('[^0-9]', "", phone.strip())
    if len(phone) != 10:
        raise TypeError('Not a valid phone number, must have 10 digits')
    else:
        return phone[:3] + '-' + phone[3:6] + '-' + phone[-4:]


def verify_name(name: str):
    """
    Validates name

    :param name: user supplied field
    :return:
        name - validated name
    """

    if len(name.strip()) > 1:
        return name.strip()
    else:
        raise TypeError('Not a valid name')


def verify_description(description: str):
    """
    Validates description name

    :param description: user supplied field
    :return:
        description - validated description name
    """

    if len(description.strip()) > 1:
        return description.strip()
    else:
        raise TypeError('Not a valid description')


def verify_number(numb: float):
    """
    Validates price/hour

    :param numb: user supplied field
    :return:
        numb - validated price/hour
    """

    try:
        numb = float(numb)
        if numb > 0:
            return numb
        else:
            raise TypeError('Numbers must be greater than zero')
    except ValueError:
        raise TypeError('Hours and Price data must be numeric')


class Employee:
    """Represents an employee"""

    def __init__(self, first: str, last: str, phone: str, email: str, emp_id=-1):
        self.__emp_id = emp_id if emp_id != -1 else None
        self.__first = verify_first_name(first)
        self.__last = verify_last_name(last)
        self.__phone = verify_phone(phone)
        self.__email = verify_email(email)

    def get_id(self):
        """Returns an employees id number"""
        return self.__emp_id

    def get_first(self):
        """Returns an employees first name"""
        return self.__first

    def get_last(self):
        """Returns an employees last name"""
        return self.__last

    def get_phone(self):
        """Returns an employees phone number"""
        return self.__phone

    def get_email(self):
        """Returns an employees email address"""
        return self.__email


class Task:
    """Represents a project task"""

    def __init__(self, name: str, description: str, price: float, hours: float, task_id=-1):
        self.__task_id = task_id if task_id != -1 else None
        self.__name = verify_name(name)
        self.__description = verify_description(description)
        self.__price = verify_number(price)
        self.__hours = verify_number(hours)

    def get_id(self):
        """Returns an employees id number"""
        return self.__task_id

    def get_name(self):
        """Returns an employees first name"""
        return self.__name

    def get_description(self):
        """Returns an employees last name"""
        return self.__description

    def get_price(self):
        """Returns an employees last name"""
        return self.__price

    def get_hours(self):
        """Returns an employees phone number"""
        return self.__hours


class Status:
    """Represents a project status"""

    def __init__(self, description: str, status_id=-1):
        self.__status_id = status_id if status_id != -1 else None
        self.__description = verify_description(description)

    def get_id(self):
        """Returns an employees id number"""
        return self.__status_id

    def get_description(self):
        """Returns an employees last name"""
        return self.__description


class Assignment:
    """Represents a project assignment"""

    def __init__(self, emp_id: int, task_id: int, status_id: int, asgmt_id=-1):
        self.__asgmt_id = asgmt_id if asgmt_id != -1 else None
        self.__emp_id = emp_id
        self.__task_id = task_id
        self.__status_id = status_id

    def get_id(self):
        """Returns an employees id number"""
        return self.__asgmt_id

    def get_emp_id(self):
        """Returns an employees first name"""
        return self.__emp_id

    def get_task_id(self):
        """Returns an employees last name"""
        return self.__task_id

    def get_status_id(self):
        """Returns an employees phone number"""
        return self.__status_id
