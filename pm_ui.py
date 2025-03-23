"""
pm_objects.py
Project Manager)

GUI Project Manager software that stores data into a database

Last modified 12/5/2020
"""

from tkinter import ttk
import tkinter as tk
import pm_db
from tkinter import *
import urllib.request
import pm_objects
from tkinter import messagebox
import tkinter.messagebox

ABOUT = 'pm_objects.py\n(Project Manager)\nCoded by Marcos Simoes\nGUI Project Manager software that stores data into a database'


def create_tables():
    """Creates the 4 tables used by the project management software"""

    sql_create_employee_table = ''' CREATE TABLE IF NOT EXISTS employee (
                                        id integer PRIMARY KEY,
                                        first text NOT NULL,
                                        last text NOT NULL,
                                        phone text,
                                        email text,
                                        UNIQUE (first, last)
                                    ); '''

    sql_create_task_table = '''CREATE TABLE IF NOT EXISTS task (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL UNIQUE,
                                    description text NOT NULL,
                                    price real NOT NULL,
                                    hours real NOT NULL
                                );'''

    sql_create_status_table = '''CREATE TABLE IF NOT EXISTS status (
                                    id integer PRIMARY KEY,
                                    description text NOT NULL UNIQUE
                                );'''

    sql_create_assignment_table = '''CREATE TABLE IF NOT EXISTS assignment (
                                    id integer PRIMARY KEY,
                                    emp_id integer NOT NULL,
                                    task_id integer NOT NULL,
                                    status_id integer NOT NULL,
                                    FOREIGN KEY (emp_id) REFERENCES employee (id),
                                    FOREIGN KEY (task_id) REFERENCES task (id),
                                    FOREIGN KEY (status_id) REFERENCES status (id)
                                );'''

    pm_db.create_table(sql_create_employee_table)
    pm_db.create_table(sql_create_task_table)
    pm_db.create_table(sql_create_status_table)
    pm_db.create_table(sql_create_assignment_table)


def populate_tables():
    """Populates the tables with sample data so the user can test the software"""

    pm_db.drop_all_tables()
    create_tables()
    pm_db.insert_employee(pm_objects.Employee('Alfreds', 'Futterkiste', '311-555-2368', 'afutterkiste@protonmail.com'))
    pm_db.insert_employee(pm_objects.Employee('Artie', 'Bucco', '212-664-7665', 'nuovovesuvio@gmail.com'))
    pm_db.insert_employee(pm_objects.Employee('Jennifer', 'Melfi', '212-718-1234', 'melfipsychiatry@outlook.com'))
    pm_db.insert_employee(pm_objects.Employee('Christopher', 'Moltisanti', '916-225-5887', 'dimeo2@yahoo.com'))
    pm_db.insert_employee(pm_objects.Employee('Salvatore', 'Bonpensiero', '415-273-9164', 'bigp@icloud.com'))
    pm_db.insert_task(pm_objects.Task('Graylyn', 'Cater wedding', 3550.00, 4.5))
    pm_db.insert_task(pm_objects.Task('Wilshire', 'Manicure playing field', 2000.00, 5))
    pm_db.insert_task(pm_objects.Task('Wells Fargo Center', 'Clean exterior windows', 15000.00, 300))
    pm_db.insert_task(pm_objects.Task('W-S Beltway', 'Clear acre of land for road construction', 2150.00, 3.5))
    pm_db.insert_task(pm_objects.Task('Winston Salem Fairgrounds', 'General cleanup after an event', 500.00, 4))
    pm_db.insert_status(pm_objects.Status('Not started'))
    pm_db.insert_status(pm_objects.Status('In Progress'))
    pm_db.insert_status(pm_objects.Status('Completed'))
    pm_db.insert_status(pm_objects.Status('Postponed'))
    pm_db.insert_status(pm_objects.Status('Cancelled'))
    pm_db.insert_assignment(pm_objects.Assignment(1, 2, 3))
    pm_db.insert_assignment(pm_objects.Assignment(2, 3, 1))
    pm_db.insert_assignment(pm_objects.Assignment(3, 4, 2))
    pm_db.insert_assignment(pm_objects.Assignment(4, 5, 3))
    pm_db.insert_assignment(pm_objects.Assignment(5, 1, 1))
    pm_db.insert_assignment(pm_objects.Assignment(1, 3, 2))
    pm_db.insert_assignment(pm_objects.Assignment(2, 1, 3))
    pm_db.insert_assignment(pm_objects.Assignment(3, 2, 1))
    pm_db.insert_assignment(pm_objects.Assignment(4, 4, 2))
    pm_db.insert_assignment(pm_objects.Assignment(5, 5, 2))


def make_treeview_sortable(table: ttk.Treeview, col, reverse: bool):
    """
    Makes clicking the table headers sort the whole table by the selected field

    :param table: a database table
    :param col: the column header the user has clicked on
    :param reverse: boolean value to toggles the sorting
    """

    try:
        sequence = [(float(table.set(element, column=col)), element) for element in table.get_children("")]
    except ValueError:
        sequence = [(table.set(element, column=col), element) for element in table.get_children("")]
    sequence.sort(reverse=reverse)
    for index, (val, element) in enumerate(sequence):
        table.move(element, "", index)
    table.heading(column=col, text=col, command=lambda _col=col: make_treeview_sortable(table, _col, not reverse))


def add_employee(first: tk.StringVar, last: tk.StringVar, phone: tk.StringVar, email: tk.StringVar,
                 table: ttk.Treeview, emp_list: list):
    """
    Attempts to add an employee to the table with user entered values

    :param first: first name
    :param last: last name
    :param phone: phone number
    :param email: email address
    :param table: a table widget
    :param emp_list: a list of all employee full names
    """

    try:
        if pm_db.insert_employee(pm_objects.Employee(first.get(), last.get(), phone.get(), email.get())):
            rows = pm_db.get_last_employee()
            for employee in rows:
                emp = list(employee)
                table.insert("", tk.END, values=emp)
            emp_list.append(first.get() + ' ' + last.get())
            first.set("")
            last.set("")
            phone.set("")
            email.set("")
    except TypeError as e:
        messagebox.showerror("Validation Error", str(e))


def add_task(name: tk.StringVar, desc: tk.StringVar, price: tk.StringVar, hours: tk.StringVar, table: ttk.Treeview,
             task_list: list):
    """
    Attempts to add a task to the table with user entered values

    :param name: task name
    :param desc: task description
    :param price: price charged for price
    :param hours: estimated hours to complete task
    :param table: a table widget
    :param task_list: a list of all task names
    """

    try:
        if pm_db.insert_task(pm_objects.Task(name.get(), desc.get(), price.get(), hours.get())):
            rows = pm_db.get_last_task()
            for task in rows:
                tsk = list(task)
                table.insert("", tk.END, values=tsk)
            task_list.append(name.get())
            name.set("")
            desc.set("")
            price.set("")
            hours.set("")
    except TypeError as e:
        messagebox.showerror("Validation Error", str(e))


def add_status(desc: tk.StringVar, table: ttk.Treeview, status_list: list):
    """
    Attempts to add a status to the table with a user entered value

    :param desc: description of project status
    :param table: a table widget
    :param status_list: a list of all status descriptions
    """

    try:
        if pm_db.insert_status(pm_objects.Status(desc.get())):
            rows = pm_db.get_last_status()
            for status in rows:
                stat = list(status)
                table.insert("", tk.END, values=stat)
            status_list.append(desc.get())
            desc.set("")
    except TypeError as e:
        messagebox.showerror('Validation Error', str(e))


def add_assignment(empl: str, task: str, stat: str, table: ttk.Treeview, asgmt_list: list):
    """
    Adds an assignment to the table from user selected values

    :param empl: employee full name
    :param task: task name
    :param stat: status description
    :param table: a table widget
    :param asgmt_list: a list of all assignments ids
    """

    emp_id = int(*pm_db.get_employee_id(empl))
    task_id = int(*pm_db.get_task_id(task))
    stat_id = int(*pm_db.get_stat_id(stat))
    try:
        if pm_db.insert_assignment(pm_objects.Assignment(emp_id, task_id, stat_id)):
            reload_asgmt_table(table)
            asgmt_list.append((len([a for a, in pm_db.get_asgmt_ids()])))
    except TypeError as e:
        messagebox.showerror('Validation Error', str(e))


def modify_assignment(asgmt_id: str, empl: str, task: str, stat: str):
    """
    Modifies a user selected assignment with selected values

    :param asgmt_id: assignment id
    :param empl: an employees full name
    :param task: a task name
    :param stat: a status description
    """

    emp_id = int(*pm_db.get_employee_id(empl))
    task_id = int(*pm_db.get_task_id(task))
    stat_id = int(*pm_db.get_stat_id(stat))
    pm_db.modify_assignment(int(asgmt_id), emp_id, task_id, stat_id)


def reload_empl_table(table: ttk.Treeview):
    """
    Reloads the employee widget with data from the employee database table

    :param table: a table widget
    """

    table.delete(*table.get_children())
    rows = pm_db.get_all_employees()
    for employee in rows:
        emp = list(employee)
        table.insert("", tk.END, values=emp)


def reload_task_table(table: ttk.Treeview):
    """
    Reloads the task widget with data from the task database table

    :param table: a table widget
    """

    table.delete(*table.get_children())
    rows = pm_db.get_all_tasks()
    for task in rows:
        tsk = list(task)
        table.insert("", tk.END, values=tsk)


def reload_stat_table(table: ttk.Treeview):
    """
    Reloads the status widget with data from the status database table

    :param table: a table widget
    """

    table.delete(*table.get_children())
    rows = pm_db.get_all_statuses()
    for stat in rows:
        cond = list(stat)
        table.insert("", tk.END, values=cond)


def reload_asgmt_table(table: ttk.Treeview):
    """
    Reloads the assignment widget with data from the assignment database table

    :param table: a table widget
    """

    table.delete(*table.get_children())
    rows = pm_db.get_all_assignments()
    for assignment in rows:
        job = list(assignment)
        table.insert("", tk.END, values=job)


def asgmt_table_by_empl(empl: str, table: ttk.Treeview):
    """
    Filters assignment widget to display for selected employee

    :param empl: an employees full name
    :param table: a table widget
    """

    table.delete(*table.get_children())
    rows = pm_db.get_by_empl_from_asgmt(empl)
    for assignment in rows:
        job = list(assignment)
        table.insert("", tk.END, values=job)


def asgmt_table_by_stat(stat: str, table: ttk.Treeview):
    """
    Filters assignment widget to display for selected status

    :param stat: a status description
    :param table: a table widget
    """

    table.delete(*table.get_children())
    rows = pm_db.get_by_stat_from_asgmt(stat)
    for assignment in rows:
        job = list(assignment)
        table.insert("", tk.END, values=job)


def update_option_menu(ddl: tk.OptionMenu, collection: list, variable: tk.StringVar):
    """
    Updates list being used by a drop down list

    :param ddl: drop down list widget
    :param collection: a list of selectable items
    :param variable: storage area for selected item from the list
    """

    menu = ddl["menu"]
    menu.delete(0, 'end')
    for items in collection:
        menu.add_command(label=items, command=lambda value=items: variable.set(value))


def background_color(style: ttk.Style):
    style.configure('TFrame', background='red')


def update_all_drop_down_lists(emp: list, tsk: list, stat: list, asg: list):
    """
    Updates all the lists being used by all the drop down menus

    :param emp: a list of employee full names
    :param tsk: a list of task names
    :param stat: a list of status descriptions
    :param asg: a list of assignment ids
    :return:
    """

    emp[:] = [e for e, in pm_db.get_empl_names()]
    tsk[:] = [t for t, in pm_db.get_task_names()]
    stat[:] = [s for s, in pm_db.get_status_names()]
    asg[:] = [a for a, in pm_db.get_asgmt_ids()]


def about():
    """Display the opening docstring in a messagebox"""

    tkinter.messagebox.showinfo('About Program Manager', ABOUT)


def main():
    # sets up the main window
    root = tk.Tk()
    root.title('Project Manager')
    root.iconphoto(False, tk.PhotoImage(file='cow.png'))
    style = ttk.Style()
    style.configure('Treeview.Heading', foreground='green')

    # file menu
    menu = Menu(root)
    root.config(menu=menu)
    file_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Exit', command=root.quit)
    color_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label='Background Color', menu=color_menu)
    color_menu.add_command(label="Red", command=lambda: style.configure('TFrame', background='red'))
    color_menu.add_command(label='Orange', command=lambda: style.configure('TFrame', background='orange'))
    color_menu.add_command(label='Yellow', command=lambda: style.configure('TFrame', background='yellow'))
    color_menu.add_command(label='Green', command=lambda: style.configure('TFrame', background='green'))
    color_menu.add_command(label='Blue', command=lambda: style.configure('TFrame', background='blue'))
    color_menu.add_command(label='Purple', command=lambda: style.configure('TFrame', background='purple'))
    color_menu.add_command(label='Gray (default)', command=lambda: style.configure('TFrame', background='grey94'))
    color_menu.add_command(label='Black', command=lambda: style.configure('TFrame', background='black'))
    help_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label='Help', menu=help_menu)
    help_menu.add_command(label='About Program Manager', command=about)

    # declares all the String Variables needed
    emp_first = tk.StringVar()
    emp_last = tk.StringVar()
    emp_phone = tk.StringVar()
    emp_email = tk.StringVar()
    task_name = tk.StringVar()
    task_desc = tk.StringVar()
    task_price = tk.StringVar()
    task_hours = tk.StringVar()
    stat_desc = tk.StringVar()
    asgmt_empl = tk.StringVar()
    asgmt_tsk = tk.StringVar()
    asgmt_stat = tk.StringVar()
    asgmt_id = tk.StringVar()
    asgmt_empl2 = tk.StringVar()
    asgmt_tsk2 = tk.StringVar()
    asgmt_stat2 = tk.StringVar()
    asgmt_empl_filter = tk.StringVar()
    asgmt_stat_filter = tk.StringVar()

    # connects to database and adds sample data if tables are empty
    pm_db.connect()
    if pm_db.empty_table():
        populate_tables()

    # sets up tabs
    tab_control = ttk.Notebook(root)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab4 = ttk.Frame(tab_control)
    tab5 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Main')
    tab_control.add(tab2, text='Employee Table')
    tab_control.add(tab3, text='Task Table')
    tab_control.add(tab4, text='Status Table')
    tab_control.add(tab5, text='Assignment Table')
    tab_control.pack(expand=1, fill='both')

    # creates Main tab
    top_start_frm = Frame(tab1)
    bottom_start_frm = Frame(tab1)
    img = tk.PhotoImage(file='logo.png')
    top_start_frm.pack()
    bottom_start_frm.pack()
    logo = tk.Text(top_start_frm, height=13, width=25)
    logo.insert(tk.END, '\n')
    logo.image_create(tk.END, image=img)
    logo.pack(side=LEFT)
    logo.config(state=DISABLED)
    text = tk.Text(top_start_frm, height=13, width=50)
    text.pack(side=LEFT)
    text.insert(tk.END, '\nAccess the different tables by clicking the tabs\n'
                        'above. Under each table you will find\n'
                        'functionality to modify or view the corresponding\n'
                        'table data. Clicking table headers will sort the\n'
                        'whole table by the selected field. Clicking a\n'
                        'second time will resort the whole table in the\n'
                        'opposite order.\n')
    text.config(state=DISABLED)
    drop_all_btn = Button(bottom_start_frm, text='Drop All Tables', command=lambda: (pm_db.drop_all_tables(),
                                                                                     tab_control.tab(tab2, state='disabled'),
                                                                                     tab_control.tab(tab3, state='disabled'),
                                                                                     tab_control.tab(tab4, state='disabled'),
                                                                                     tab_control.tab(tab5, state='disabled'),
                                                                                     load_sample_btn.configure(state=NORMAL),
                                                                                     drop_all_btn.configure(state=DISABLED)))
    drop_all_btn.pack(side=LEFT, padx=5, pady=5)
    load_sample_btn = Button(bottom_start_frm, text='Load Sample Data', command=lambda: (populate_tables(),
                                                                                         tab_control.tab(tab2, state='normal'),
                                                                                         tab_control.tab(tab3, state='normal'),
                                                                                         tab_control.tab(tab4, state='normal'),
                                                                                         tab_control.tab(tab5, state='normal'),
                                                                                         load_sample_btn.configure(state=DISABLED),
                                                                                         drop_all_btn.configure(state=NORMAL),
                                                                                         reload_empl_table(emp_tree),
                                                                                         reload_task_table(task_tree),
                                                                                         reload_stat_table(stat_tree),
                                                                                         reload_asgmt_table(asgmt_tree),
                                                                                         update_all_drop_down_lists(employee_list, task_list, status_list, id_list),
                                                                                         update_option_menu(asgmt_employee_ddl, employee_list, asgmt_empl),
                                                                                         update_option_menu(modify_employee_ddl, employee_list, asgmt_empl2),
                                                                                         update_option_menu(filter_by_empl_ddl, employee_list, asgmt_empl_filter),
                                                                                         update_option_menu(asgmt_task_ddl, task_list, asgmt_tsk),
                                                                                         update_option_menu(modify_task_ddl, task_list, asgmt_tsk2),
                                                                                         update_option_menu(asgmt_status_ddl, status_list, asgmt_stat),
                                                                                         update_option_menu(modify_status_ddl, status_list, asgmt_stat2),
                                                                                         update_option_menu(filter_by_status_ddl, status_list, asgmt_stat_filter),
                                                                                         update_option_menu(asgmt_id_ddl, id_list, asgmt_id)))
    load_sample_btn.pack(side=LEFT, padx=5, pady=5)
    if pm_db.empty_table():
        drop_all_btn.configure(state=DISABLED)
    else:
        load_sample_btn.configure(state=DISABLED)

    # creates Employee Table tab
    top_emp_frm = Frame(tab2)
    bottom_emp_frm = Frame(tab2, highlightbackground='black', highlightthickness=1, padx=4, pady=4)
    top_emp_frm.pack()
    bottom_emp_frm.pack()
    rows = pm_db.get_all_employees()
    row = rows.fetchone()
    headings = row.keys()
    headings = [x.upper() for x in headings]
    emp_tree = ttk.Treeview(top_emp_frm, columns=headings, show='headings')
    emp_tree.pack()
    rows = pm_db.get_all_employees()
    for employee in rows:
        emp = list(employee)
        emp_tree.insert("", tk.END, values=emp)
    for col in headings:
        emp_tree.heading(col, text=col, command=lambda _col=col: make_treeview_sortable(emp_tree, _col, False))
    add_emp_lbl = Label(bottom_emp_frm, text="ADD EMPLOYEE:  ").pack(side=LEFT)
    fn_lbl = Label(bottom_emp_frm, text="First Name:").pack(side=LEFT)
    first_name_txt = Entry(bottom_emp_frm, textvariable=emp_first).pack(side=LEFT)
    ln_lbl = Label(bottom_emp_frm, text="Last Name:").pack(side=LEFT)
    last_name_txt = Entry(bottom_emp_frm, textvariable=emp_last).pack(side=LEFT)
    phone_lbl = Label(bottom_emp_frm, text="Phone:").pack(side=LEFT)
    phone_txt = Entry(bottom_emp_frm, textvariable=emp_phone).pack(side=LEFT)
    email_lbl = Label(bottom_emp_frm, text="Email:").pack(side=LEFT)
    email_txt = Entry(bottom_emp_frm, textvariable=emp_email).pack(side=LEFT)
    add_emp_btn = Button(bottom_emp_frm, text="Add", command=lambda: (add_employee(emp_first, emp_last, emp_phone, emp_email, emp_tree, employee_list),
                                                                      update_option_menu(asgmt_employee_ddl, employee_list, asgmt_empl),
                                                                      update_option_menu(modify_employee_ddl, employee_list, asgmt_empl2),
                                                                      update_option_menu(filter_by_empl_ddl, employee_list, asgmt_empl_filter))).pack(side=LEFT)

    # creates Task table tab
    top_task_frm = Frame(tab3)
    bottom_task_frm = Frame(tab3, highlightbackground='black', highlightthickness=1, padx=4, pady=4)
    top_task_frm.pack()
    bottom_task_frm.pack()
    rows = pm_db.get_all_tasks()
    row = rows.fetchone()
    headings = row.keys()
    headings = [x.upper() for x in headings]
    task_tree = ttk.Treeview(top_task_frm, columns=headings, show='headings')
    task_tree.pack()
    rows = pm_db.get_all_tasks()
    for task in rows:
        tsk = list(task)
        task_tree.insert("", tk.END, values=tsk)
    for col in headings:
        task_tree.heading(col, text=col, command=lambda _col=col: make_treeview_sortable(task_tree, _col, False))
    add_task_lbl = Label(bottom_task_frm, text='ADD TASK:  ').pack(side=LEFT)
    name_lbl = Label(bottom_task_frm, text='Name:').pack(side=LEFT)
    name_txt = Entry(bottom_task_frm, textvariable=task_name).pack(side=LEFT)
    desc_lbl = Label(bottom_task_frm, text='Description:').pack(side=LEFT)
    description_txt = Entry(bottom_task_frm, textvariable=task_desc).pack(side=LEFT)
    price_lbl = Label(bottom_task_frm, text='Price:').pack(side=LEFT)
    price_txt = Entry(bottom_task_frm, textvariable=task_price).pack(side=LEFT)
    hours_lbl = Label(bottom_task_frm, text='Hours:').pack(side=LEFT)
    hours_txt = Entry(bottom_task_frm, textvariable=task_hours).pack(side=LEFT)
    add_tsk_btn = Button(bottom_task_frm, text='Add', command=lambda: (add_task(task_name, task_desc, task_price, task_hours, task_tree, task_list),
                                                                       update_option_menu(asgmt_task_ddl, task_list, asgmt_tsk),
                                                                       update_option_menu(modify_task_ddl, task_list, asgmt_tsk2))).pack(side=LEFT)

    # creates Status tab
    top_stat_frm = Frame(tab4)
    bottom_stat_frm = Frame(tab4, highlightbackground='black', highlightthickness=1, padx=4, pady=4)
    top_stat_frm.pack()
    bottom_stat_frm.pack()
    rows = pm_db.get_all_statuses()
    row = rows.fetchone()
    headings = row.keys()
    headings = [x.upper() for x in headings]
    stat_tree = ttk.Treeview(top_stat_frm, columns=headings, show='headings')
    stat_tree.pack()
    rows = pm_db.get_all_statuses()
    for status in rows:
        mode = list(status)
        stat_tree.insert("", tk.END, values=mode)
    for col in headings:
        stat_tree.heading(col, text=col, command=lambda _col=col: make_treeview_sortable(stat_tree, _col, False))
    add_stat_lbl = Label(bottom_stat_frm, text='ADD STATUS:  ').pack(side=LEFT)
    stat_desc_lbl = Label(bottom_stat_frm, text='Description:').pack(side=LEFT)
    stat_description_txt = Entry(bottom_stat_frm, textvariable=stat_desc).pack(side=LEFT)
    add_stat_btn = Button(bottom_stat_frm, text='Add', command=lambda: (add_status(stat_desc, stat_tree, status_list),
                                                                        update_option_menu(asgmt_status_ddl, status_list, asgmt_stat),
                                                                        update_option_menu(modify_status_ddl, status_list, asgmt_stat2),
                                                                        update_option_menu(filter_by_status_ddl, status_list, asgmt_stat_filter))).pack(side=LEFT)

    # creates Assignment tab
    top_asgmt_frm = Frame(tab5)
    add_asgmt_frm = Frame(tab5, highlightbackground='black', highlightthickness=1, padx=4, pady=4)
    modify_asgmt_frm = Frame(tab5, highlightbackground='black', highlightthickness=1, padx=4, pady=4)
    bottom_asgmt_frm = Frame(tab5)
    filter_by_empl_frm = Frame(bottom_asgmt_frm, highlightbackground='black', highlightthickness=1, padx=4, pady=4)
    filter_by_status_frm = Frame(bottom_asgmt_frm, highlightbackground='black', highlightthickness=1, padx=4, pady=4)
    show_all_frm = Frame(bottom_asgmt_frm, highlightbackground='black', highlightthickness=1, padx=9, pady=8)
    top_asgmt_frm.pack()
    add_asgmt_frm.pack()
    modify_asgmt_frm.pack()
    bottom_asgmt_frm.pack()
    filter_by_empl_frm.pack(side=LEFT)
    filter_by_status_frm.pack(side=LEFT)
    show_all_frm.pack(side=LEFT)
    rows = pm_db.get_all_assignments()
    row = rows.fetchone()
    headings = row.keys()
    headings = [x.upper() for x in headings]
    asgmt_tree = ttk.Treeview(top_asgmt_frm, columns=headings, show='headings')
    asgmt_tree.pack()
    rows = pm_db.get_all_assignments()
    for assignment in rows:
        job = list(assignment)
        asgmt_tree.insert("", tk.END, values=job)
    for col in headings:
        asgmt_tree.heading(col, text=col, command=lambda _col=col: make_treeview_sortable(asgmt_tree, _col, False))
    employee_list = [e for e, in pm_db.get_empl_names()]
    asgmt_empl.set(employee_list[0])
    task_list = [t for t, in pm_db.get_task_names()]
    asgmt_tsk.set(task_list[0])
    status_list = [s for s, in pm_db.get_status_names()]
    asgmt_stat.set(status_list[0])
    id_list = [a for a, in pm_db.get_asgmt_ids()]
    add_asgmt_lbl = Label(add_asgmt_frm, text='ADD ASSIGNMENT:  ').pack(side=LEFT)
    asgmt_employee_ddl = OptionMenu(add_asgmt_frm, asgmt_empl, *employee_list)
    asgmt_employee_ddl.pack(side=LEFT, padx=2, pady=2)
    asgmt_task_ddl = OptionMenu(add_asgmt_frm, asgmt_tsk, *task_list)
    asgmt_task_ddl.pack(side=LEFT, padx=2, pady=2)
    asgmt_status_ddl = OptionMenu(add_asgmt_frm, asgmt_stat, *status_list)
    asgmt_status_ddl.pack(side=LEFT, padx=2, pady=2)
    add_asgmt_btn = Button(add_asgmt_frm, text='Add', command=lambda: (add_assignment(asgmt_empl.get(), asgmt_tsk.get(),
                                                                       asgmt_stat.get(), asgmt_tree, id_list),
                                                                       update_option_menu(asgmt_id_ddl, id_list, asgmt_id),
                                                                       asgmt_empl.set(employee_list[0]), asgmt_tsk.set(task_list[0]),
                                                                       asgmt_stat.set(status_list[0]), show_all_btn.configure(state=DISABLED),
                                                                       asgmt_empl_filter.set(""), asgmt_stat_filter.set(""),
                                                                       asgmt_id.set("Pick an ID"), asgmt_empl2.set(""), asgmt_tsk2.set(""), asgmt_stat2.set(""),
                                                                       modify_employee_ddl.configure(state=DISABLED), modify_task_ddl.configure(state=DISABLED),
                                                                       modify_status_ddl.configure(state=DISABLED), modify_asgmt_btn.configure(state=DISABLED))).pack(side=LEFT, padx=2, pady=2)
    asgmt_id.set('Pick an ID')
    modify_asgmt_lbl = Label(modify_asgmt_frm, text='MODIFY ASSIGNMENT:  ').pack(side=LEFT)
    asgmt_id_ddl = OptionMenu(modify_asgmt_frm, asgmt_id, *id_list)
    asgmt_id_ddl.pack(side=LEFT, padx=2, pady=2)
    modify_employee_ddl = OptionMenu(modify_asgmt_frm, asgmt_empl2, *employee_list)
    modify_employee_ddl.pack(side=LEFT, padx=2, pady=2)
    modify_task_ddl = OptionMenu(modify_asgmt_frm, asgmt_tsk2, *task_list)
    modify_task_ddl.pack(side=LEFT, padx=2, pady=2)
    modify_status_ddl = OptionMenu(modify_asgmt_frm, asgmt_stat2, *status_list)
    modify_status_ddl.pack(side=LEFT, padx=2, pady=2)
    modify_asgmt_btn = Button(modify_asgmt_frm, text='Modify', command=lambda: (modify_assignment(asgmt_id.get(), asgmt_empl2.get(),
                                                                                asgmt_tsk2.get(), asgmt_stat2.get()),
                                                                                asgmt_empl2.set(""), asgmt_tsk2.set(""),
                                                                                asgmt_stat2.set(""), asgmt_id.set("Pick an ID"), show_all_btn.configure(state=DISABLED),
                                                                                modify_employee_ddl.configure(state=DISABLED), modify_task_ddl.configure(state=DISABLED),
                                                                                modify_status_ddl.configure(state=DISABLED), modify_asgmt_btn.configure(state=DISABLED),
                                                                                reload_asgmt_table(asgmt_tree), asgmt_empl_filter.set(""), asgmt_stat_filter.set("")))
    modify_asgmt_btn.pack(side=LEFT, padx=2, pady=2)
    modify_employee_ddl.configure(state=DISABLED)
    modify_task_ddl.configure(state=DISABLED)
    modify_status_ddl.configure(state=DISABLED)
    modify_asgmt_btn.configure(state=DISABLED)
    filter_by_empl_lbl = Label(filter_by_empl_frm, text='FILTER BY EMPLOYEE:  ').pack(side=LEFT)
    filter_by_empl_ddl = OptionMenu(filter_by_empl_frm, asgmt_empl_filter, *employee_list)
    filter_by_empl_ddl.pack(side=LEFT, padx=2, pady=2)

    filter_by_status_lbl = Label(filter_by_status_frm, text='FILTER BY STATUS:  ').pack(side=LEFT)
    filter_by_status_ddl = OptionMenu(filter_by_status_frm, asgmt_stat_filter, *status_list)
    filter_by_status_ddl.pack(side=LEFT, padx=2, pady=2)
    show_all_btn = Button(show_all_frm, text='Show All Assignments', command=lambda: (reload_asgmt_table(asgmt_tree), show_all_btn.configure(state=DISABLED),
                                                                                      asgmt_empl_filter.set(""), asgmt_stat_filter.set("")))
    show_all_btn.pack()
    modify_employee_ddl.configure(state=DISABLED)
    modify_task_ddl.configure(state=DISABLED)
    modify_status_ddl.configure(state=DISABLED)
    modify_asgmt_btn.configure(state=DISABLED)
    show_all_btn.configure(state=DISABLED)

    # Tkinter OptionMenu (drop down list) have the ability to attach commands, however, if you change the list
    # of options the commands also get discarded. If it is one simple command, it can be restored, however the
    # complexity of the anonymous functions (lambdas) being used makes it so that using a trace is the only way
    # to maintain functionality while allowing the flexibility needed. These are placed at the end so that the
    # compiler will have seen all the referenced variables.
    asgmt_id.trace('w', lambda *args: ((asgmt_empl2.set(employee_list[int(*pm_db.get_empl_id_from_asgmt(asgmt_id.get())) - 1]),
                                       asgmt_tsk2.set(task_list[int(*pm_db.get_task_id_from_asgmt(asgmt_id.get())) - 1]),
                                       asgmt_stat2.set(status_list[int(*pm_db.get_status_id_from_asgmt(asgmt_id.get())) - 1]),
                                       modify_employee_ddl.configure(state=NORMAL), modify_task_ddl.configure(state=NORMAL),
                                       modify_status_ddl.configure(state=NORMAL), modify_asgmt_btn.configure(state=NORMAL)) if asgmt_id.get() != "Pick an ID" else ()))
    asgmt_empl_filter.trace('w', lambda *args: ((asgmt_table_by_empl(asgmt_empl_filter.get(), asgmt_tree), asgmt_stat_filter.set(""),
                                                show_all_btn.configure(state=NORMAL)) if asgmt_empl_filter.get() != "" else ()))
    asgmt_stat_filter.trace('w', lambda *args: ((asgmt_table_by_stat(asgmt_stat_filter.get(), asgmt_tree), asgmt_empl_filter.set(""),
                                                 show_all_btn.configure(state=NORMAL)) if asgmt_stat_filter.get() != "" else ()))

    root.mainloop()


main()
