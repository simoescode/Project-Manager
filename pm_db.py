"""
pm_objects.py
(Project Manager)

GUI Project Manager software that stores data into a database

Last modified 12/5/2020
"""

import sys
import os
import sqlite3
from sqlite3 import Error
from contextlib import closing
from tkinter import messagebox
import pm_objects

CONN = None
DB_NAME = 'pm.sqlite'


def connect():
    """Establishes connection to database"""

    global CONN
    if not CONN:
        if sys.platform == "win32":
            db_file = DB_NAME
        else:
            db_file = os.environ["HOME"] + DB_NAME
        try:
            CONN = sqlite3.connect(db_file)
            CONN.row_factory = sqlite3.Row
        except Error as e:
            messagebox.showerror("Database Error", str(e))


def close():
    """Closes connection to database"""

    if CONN:
        CONN.close()


def create_table(sql_query):
    """
    Creates database table

    :param sql_query: an SQL query
    """
    try:
        CONN.cursor().execute(sql_query)
    except Error as e:
        messagebox.showerror("Database Error", str(e))


def drop_all_tables():
    """Drops all 4 tables"""

    CONN.cursor().execute('DROP TABLE IF EXISTS employee')
    CONN.cursor().execute('DROP TABLE IF EXISTS task')
    CONN.cursor().execute('DROP TABLE IF EXISTS status')
    CONN.cursor().execute('DROP TABLE IF EXISTS assignment')
    CONN.commit()


def empty_table():
    """
    determines if assignment table is empty

    :return:
        bool - true if empty, false if not empty
    """

    try:
        return CONN.execute('''SELECT count(*) FROM (select 1 from assignment limit 1)''') is None
    except sqlite3.Error as e:
        if str(e) != 'no such table: assignment':
            messagebox.showerror("Database Error", str(e))
        return True


def get_all_employees():
    """Returns all rows from employee table"""

    try:
        return CONN.execute('''SELECT * FROM employee''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_last_employee():
    """Returns the last row from the employee table"""

    try:
        return CONN.execute('''SELECT * FROM employee ORDER BY id DESC LIMIT 1''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_employee_id(name: str):
    """
    Finds an employee record

    :param name: full name of employee
    :return:
        id of chosen employee
    """

    query = ('''SELECT id FROM employee
                WHERE (first || " " || last)=?''')
    try:
        with closing(CONN.cursor()) as cur:
            cur.execute(query, (name,))
            return cur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_all_tasks():
    """"Returns all rows from task table"""

    try:
        return CONN.execute('''SELECT * FROM task''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_last_task():
    """Returns the last row from the task table"""

    try:
        return CONN.execute('''SELECT * FROM task ORDER BY id DESC LIMIT 1''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_task_id(name: str):
    """
    Finds a task record

    :param name: task name
    :return:
        id of chosen task
    """

    query = ('''SELECT id FROM task
                WHERE name=?''')
    try:
        with closing(CONN.cursor()) as cur:
            cur.execute(query, (name,))
            return cur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_all_statuses():
    """Returns all rows from status table"""

    try:
        return CONN.execute('''SELECT * FROM status''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_last_status():
    """Returns the last row from the status table"""

    try:
        return CONN.execute('''SELECT * FROM status ORDER BY id DESC LIMIT 1''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_stat_id(name: str):
    """
    Finds a status id

    :param name: status description
    :return:
        id of chosen status
    """

    query = ('''SELECT id FROM status
                WHERE description=?''')
    try:
        with closing(CONN.cursor()) as cur:
            cur.execute(query, (name,))
            return cur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_all_assignments():
    """"Returns all adapted rows from assignment table"""

    try:
        return CONN.execute('''SELECT assignment.id, (first || " " || last) as Employee, 
                               task.name as Task, status.description as Status FROM assignment
                               JOIN employee ON assignment.emp_ID = employee.id
                               JOIN task ON assignment.task_ID = task.ID
                               JOIN status ON assignment.status_ID = status.ID''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_last_assignment():
    """Returns the last adapted row from the assignment table"""

    try:
        return CONN.execute('''SELECT assignment.id, (first || " " || last) as Employee, 
                               task.name as Task, status.description as Status FROM assignment
                               JOIN employee ON assignment.emp_ID = employee.id
                               JOIN task ON assignment.task_ID = task.ID
                               JOIN status ON assignment.status_ID = status.ID
                               ORDER BY assignment.id DESC LIMIT 1''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_asgmt_ids():
    """Returns all the assignment ids"""

    try:
        return CONN.execute('''SELECT id FROM assignment''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_empl_names():
    """Returns all the employee full names"""

    try:
        return CONN.execute('''SELECT (first || " " || last) as Employee FROM employee ORDER BY id ASC''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_task_names():
    """Returns all the task names"""

    try:
        return CONN.execute('''SELECT name FROM task ORDER BY id ASC''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_status_names():
    """Returns all the status descriptions"""

    try:
        return CONN.execute('''SELECT description FROM status ORDER BY id ASC''')
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_by_empl_from_asgmt(empl: str):
    """
    Selects all assignment records that pertain to an employee

    :param empl: a full employee name
    :return:
        all adapted rows from the assignment table that are associated with selected employee
    """

    query = ('''SELECT assignment.id, (first || " " || last) as Employee, 
                task.name as Task, status.description as Status FROM assignment
                JOIN employee ON assignment.emp_ID = employee.id
                JOIN task ON assignment.task_ID = task.ID
                JOIN status ON assignment.status_ID = status.ID
                WHERE (first || " " || last) = ? ''')
    try:
        with closing(CONN.cursor()) as cur:
            cur.execute(query, (empl,))
            return cur.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_by_stat_from_asgmt(stat: str):
    """
    Selects all assignment records that pertain to a task

    :param stat: a task name
    :return:
        all adapted rows from the assignment table that are associated with selected task
    """

    query = ('''SELECT assignment.id, (first || " " || last) as Employee, 
                task.name as Task, status.description as Status FROM assignment
                JOIN employee ON assignment.emp_ID = employee.id
                JOIN task ON assignment.task_ID = task.ID
                JOIN status ON assignment.status_ID = status.ID
                WHERE status.description = ? ''')
    try:
        with closing(CONN.cursor()) as cur:
            cur.execute(query, (stat,))
            return cur.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_empl_id_from_asgmt(asgmt_id: int):
    """Gets the employee ID associated with a given assignment

    :param asgmt_id: an assignment id
    :return:
        corresponding employee id for selected assignment id
    """

    query = ('''SELECT emp_id FROM assignment
                WHERE id = ? ''')
    try:
        with closing(CONN.cursor()) as cur:
            cur.execute(query, (asgmt_id,))
            return cur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_task_id_from_asgmt(asgmt_id: int):
    """Gets the task ID associated with a given assignment

    :param asgmt_id: an assignment id
    :return:
        corresponding task id for selected assignment id
    """

    query = ('''SELECT task_id FROM assignment
                WHERE id = ? ''')
    try:
        with closing(CONN.cursor()) as cur:
            cur.execute(query, (asgmt_id,))
            return cur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def get_status_id_from_asgmt(asgmt_id: int):
    """Gets the status ID associated with a given assignment

    :param asgmt_id: an assignment id
    :return:
        corresponding status id for selected assignment id
    """

    query = ('''SELECT status_id FROM assignment
                WHERE id = ? ''')
    try:
        with closing(CONN.cursor()) as cur:
            cur.execute(query, (asgmt_id,))
            return cur.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def insert_employee(empl: pm_objects.Employee):
    """
    Inserts a new employee into the employee database table

    :param empl: an employee object with information for all required fields
    :return:
        bool - True if successful, False if not
    """

    try:
        with closing(CONN.cursor()) as cur:
            query = ''' INSERT INTO employee(first, last, phone, email)
                        VALUES(?,?,?,?) '''
            cur.execute(query, (empl.get_first(), empl.get_last(), empl.get_phone(), empl.get_email()))
        CONN.commit()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return False


def insert_task(task: pm_objects.Task):
    """
    Inserts a new task into the task database table

    :param task: a task object with information for all required fields
    :return:
        bool - True if successful, False if not
    """

    try:
        with closing(CONN.cursor()) as cur:
            query = ''' INSERT INTO task(name, description, price, hours)
                        VALUES(?,?,?,?) '''
            cur.execute(query, (task.get_name(), task.get_description(), task.get_price(), task.get_hours()))
        CONN.commit()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return False


def insert_status(stat: pm_objects.Status):
    """
    Inserts a new status into the status database table

    :param stat: a status object with information for all required fields
    :return:
        bool - True if successful, False if not
    """

    try:
        with closing(CONN.cursor()) as cur:
            query = ''' INSERT INTO status(description)
                        VALUES(?) '''
            cur.execute(query, (stat.get_description(),))
        CONN.commit()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return False


def insert_assignment(asgmt: pm_objects.Assignment):
    """
    Inserts a new assignment into the assignment database table

    :param asgmt: an assignment object with information for all required fields
    :return:
        bool - True if successful, False if not
    """

    try:
        with closing(CONN.cursor()) as cur:
            query = ''' INSERT INTO assignment(emp_id, task_id, status_id)
                        VALUES(?,?,?) '''
            cur.execute(query, (asgmt.get_emp_id(), asgmt.get_task_id(), asgmt.get_status_id()))
        CONN.commit()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
        return False


def modify_assignment(asgmt_id: int, emp_id: int, task_id: int, status_id: int):
    """
    Modifies an existing assignment record

    :param asgmt_id: assignment id
    :param emp_id: employee id
    :param task_id: task id
    :param status_id: status id
    """

    try:
        with closing(CONN.cursor()) as cur:
            query = ''' UPDATE assignment 
                        SET emp_id = ? , task_id = ? , status_id = ?
                        WHERE id = ? '''
            cur.execute(query, (emp_id, task_id, status_id, asgmt_id))
        CONN.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
