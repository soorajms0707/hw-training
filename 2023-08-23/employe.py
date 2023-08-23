from datetime import datetime
import json

class employee:
    tasks=[]

    def __init__(self,emp_id,emp_name):
        self.emp_id = emp_id
        self.emp_name = emp_name
        self.login_time = datetime.now()

    def start_task(self):
        self.task = {
            "task_title": task_title,
            "task_description": task_description,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "end_time": None,
            "task_success": None
         }
        self.tasks.append(self.task)

    def end_task(self):
        if self.task:
            self.task["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.task["task_success"] = task_success

    def logout(self):
        self.logout_time = datetime.now()
        self.save_to_json()

    def save_to_json(self):
        data = {
            "emp_name": self.emp_name,
            "emp_id": self.emp_id,
            "login_time": self.login_time.strftime("%Y-%m-%d %H:%M"),
            "logout_time": self.logout_time.strftime("%Y-%m-%d %H:%M"),
            "tasks": self.tasks
        }

        filename = f"{self.emp_name}_{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(filename, "a") as file:
            json.dump(data,file,indent=4)



emp_name = input("Enter employee name: ")
emp_id = int(input("Enter employee ID: "))

emp = employee(emp_name=emp_name,emp_id=emp_id) 

while True:
    choice = input(" \n\n Please Enter \n 'start' to start a task\n 'end' to end the current task \n 'logout' to log out \n").lower()
    if choice == "start":
        task_title = input("Enter task title: ")
        task_description = input("Enter task description: ")
        emp.start_task()
    elif choice == "end":
        task_success = input("Did the task succeed? (True/False): ").lower()
        emp.end_task()
        print("Task completed")
    elif choice == "logout":
        emp.logout()
        break
    else:
        print("Invalid choice. Please enter 'start', 'end', or 'logout'.")
