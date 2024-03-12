import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to load tasks from tasks.txt file
def load_tasks():
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w"):
            pass

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)
    
    return task_list

# Function to save tasks to tasks.txt file
def save_tasks(tasks):
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in tasks:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Function to register a new user
def reg_user():
    new_username = input("New Username: ")
    if new_username in username_password:
        print("Username already exists. Please choose a different one.")
        return

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    username_password[new_username] = new_password
    with open("user.txt", "a") as user_file:
        user_file.write(f"\n{new_username};{new_password}")

    print("New user added.")

# Function to add a new task
def add_task():
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    save_tasks(task_list)
    print("Task successfully added.")

# Function to view all tasks
def view_all():
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine():
    task_indices = []

# Display tasks assigned to the current user and allow interaction
    task_number = 0
    for i, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            task_number += 1
            disp_str = f"Task: {task_number} \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            task_indices.append(i - 1)  # Append the index of the displayed task to task_indices

    while True:
        selection = input("Enter the task number to mark it as complete, or type '-1' to return to the main menu: ")
        
        if selection == '-1':
            break
        
        try:
            task_index = int(selection) - 1
            if task_index in task_indices:  # Check if the selected index is within task_indices
                action = input("Enter 'c' to mark the task as complete, or 'e' to edit the task: ")
                if action == 'c':
                    task_list[task_index]['completed'] = True
                    save_tasks(task_list)
                    print("Task marked as complete.")
                elif action == 'e':
                    if not task_list[task_index]['completed']:
                        new_username = input("Enter new username or leave blank to keep current: ").strip()
                        new_due_date = input("Enter new due date (YYYY-MM-DD) or leave blank to keep current: ").strip()
                        if new_username:
                            task_list[task_index]['username'] = new_username
                        if new_due_date:
                            try:
                                new_due_date = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                task_list[task_index]['due_date'] = new_due_date
                            except ValueError:
                                print("Invalid date format. Task due date not updated.")
                        save_tasks(task_list)
                        print("Task updated successfully.")
                    else:
                        print("Cannot edit a completed task.")
                else:
                    print("Invalid action. Please enter 'c' to mark as complete or 'e' to edit.")
            else:
                print("Invalid task number. Please select a valid task.")
        except ValueError:
            print("Invalid input. Please enter a number.")
   
# Function to generate reports
def generate_reports():
    task_list = load_tasks()

    # Task overview
    total_tasks = len(task_list)
    completed_tasks = sum(1 for t in task_list if t['completed'])
    uncompleted_tasks = total_tasks - completed_tasks
    # Compare with date part only
    overdue_tasks = sum(1 for t in task_list if not t['completed'] 
                        and t['due_date'].date() < date.today())  
    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    # Write task overview to task_overview.txt
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview:\n")
        task_overview_file.write(f"Total Tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted Tasks: {uncompleted_tasks}\n")
        task_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of Incomplete Tasks: {incomplete_percentage}%\n")
        task_overview_file.write(f"Percentage of Overdue Tasks: {overdue_percentage}%\n")

    # User overview
    users = set(t['username'] for t in task_list)
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview:\n")
        user_overview_file.write(f"Total Users: {len(users)}\n")
        user_overview_file.write(f"Total Tasks: {total_tasks}\n")

        for user in users:
            user_tasks = [t for t in task_list if t['username'] == user]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(1 for t in user_tasks if t['completed'])
            incomplete_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for t in user_tasks if not t['completed'] and t['due_date'].date() < date.today())

            user_task_percentage = (total_user_tasks / total_tasks) * 100
            completed_task_percentage = (completed_user_tasks / total_user_tasks) * 100
            incomplete_task_percentage = (incomplete_user_tasks / total_user_tasks) * 100
            overdue_task_percentage = (overdue_user_tasks / total_user_tasks) * 100

            user_overview_file.write(f"\nUser: {user}\n")
            user_overview_file.write(f"Total User Tasks: {total_user_tasks}\n")
            user_overview_file.write(f"Percentage of Total Tasks: {user_task_percentage}%\n")
            user_overview_file.write(f"Percentage of Completed Tasks: {completed_task_percentage}%\n")
            user_overview_file.write(f"Percentage of Incomplete Tasks: {incomplete_task_percentage}%\n")
            user_overview_file.write(f"Percentage of Overdue Tasks: {overdue_task_percentage}%\n")

# Function to display statistics
def display_statistics():
    task_list = load_tasks()
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")

# Main code
username_password = {}

# Load username and password data from user.txt
if os.path.exists("user.txt"):
    with open("user.txt", "r") as user_file:
        for line in user_file:
            username, password = line.strip().split(";")
            username_password[username] = password

# Load task data
task_list = load_tasks()

# Login
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
    else:
        print("Login Successful!")
        logged_in = True

# Main loop
while True:
    print()
    menu = input('''Select one of the following Options below:
    r - Register a user
    a - Add a task
    va - View all tasks
    vm - View my tasks
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        if curr_user == "admin":
            generate_reports()
            print("Reports generated successfully.")
        else:
            print("The current user does not have permission to generate the report!")
    elif menu == 'ds':
        if curr_user == "admin":
            display_statistics()
        else:
            print("The current user does not have permission to display the statistics")
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("Invalid choice. Please try again.")