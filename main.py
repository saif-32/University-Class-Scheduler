import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


def scrape_class_times(course_numbers):
    # Initialize Chrome options and service
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    s = Service("/Users/pirani/Desktop/chromedriver")

    # Loop through each course number and create a new browser instance
    class_dicts_list = []

    for course_number in course_numbers:
        driver = webdriver.Chrome(service=s, options=chrome_options)
        driver.get("https://asap.utsa.edu/pls/prod/xwskschd.P_UTSA_OpenSch")
        select_term = Select(driver.find_element(By.NAME, "term"))
        select_term.select_by_visible_text('Fall 2023')
        select_subject = Select(driver.find_element(By.XPATH, "/html/body/div[3]/form/table/tbody/tr[2]/td[4]/select"))
        select_subject.select_by_visible_text('Computer Science (CS)')
        select_course_number = driver.find_element(By.NAME, "sel_crse")
        select_course_number.send_keys(course_number)
        search_button = driver.find_element(By.XPATH, "/html/body/div[3]/form/center/input[2]")
        search_button.click()
        small_elements = driver.find_elements(By.XPATH, "//small")
        values = [element.text for element in small_elements]

        data = []
        start = False
        for value in values:
            if value.startswith("CS") and not start:
                start = True
            if start:
                if value.startswith("View Book Information"):
                    start = False
                else:
                    data.append(value)

        data = list(filter(None, data))
        chunks = [data[i:i + 17] for i in range(0, len(data), 17)]
        class_dicts = []

        for chunk in chunks:
            class_dict = {
                "Subject": chunk[0],
                "Course": int(chunk[1]),
                "Section": chunk[2],
                "Course Number": int(chunk[3]),
                "Class Name": chunk[4],
                "Credits": int(chunk[5]),
                "Meeting Days": [chunk[6]],
                "Meeting Time": chunk[7],
                "Campus": chunk[8],
                "Location": chunk[9],
                "Dates": chunk[10],
                "Weeks": int(chunk[11]),
                "Instructor": chunk[12],
                "Seats": int(chunk[13]),
                "Entry": int(chunk[14]),
                "Availability": int(chunk[15])
            }
            class_dicts.append(class_dict)

        class_dicts_list.append(class_dicts)
        driver.quit()

    return class_dicts_list


def generate_schedule_combinations(classes):
    schedules = []
    current_schedule = []

    def backtrack(index):
        if index == len(classes):
            schedules.append(current_schedule.copy())
            return

        for session in classes[index]["sessions"]:
            if not has_conflict(session, current_schedule):
                current_schedule.append(session)
                backtrack(index + 1)
                current_schedule.pop()

    backtrack(0)
    return schedules


def has_conflict(session, schedule):
    for existing_session in schedule:
        if any(day1 in existing_session["Meeting Days"] and overlaps(session["Meeting Time"],
                                                                     existing_session["Meeting Time"])
               for day1 in session["Meeting Days"]):
            return True
    return False


def overlaps(time1, time2):
    start1, end1 = map(parse_time, time1.split("-"))
    start2, end2 = map(parse_time, time2.split("-"))
    return start1 < end2 and start2 < end1


def parse_time(time_str):
    # Convert a time string (e.g., "7:30am") to minutes since midnight
    parts = time_str.strip().split(":")
    hour = int(parts[0])
    minutes = int(parts[1][:2])
    if "pm" in parts[1] and hour != 12:
        hour += 12
    return hour * 60 + minutes


def get_schedule():
    course_numbers = [entry.get() for entry in course_number_entries if entry.get()]

    if not course_numbers:
        messagebox.showerror("Error", "Please enter at least one course number.")
        return

    # Scrape class times
    class_dicts_list = scrape_class_times(course_numbers)

    # Create class structures
    classes = []

    for class_dicts in class_dicts_list:
        class_info = {
            "Name": class_dicts[0]["Class Name"],
            "Course Number": class_dicts[0]["Course Number"],
            "sessions": []
        }

        for session_dict in class_dicts:
            session_info = {
                "Meeting Days": [session_dict["Meeting Days"]],
                "Meeting Time": session_dict["Meeting Time"]
            }
            class_info["sessions"].append(session_info)

        classes.append(class_info)

    # Generate schedules
    schedules = generate_schedule_combinations(classes)

    # Display schedules in the GUI
    result_text.delete(1.0, tk.END)
    for i, schedule in enumerate(schedules):
        result_text.insert(tk.END, f"Schedule {i + 1}:\n")
        for j, session in enumerate(schedule):
            class_info = classes[j]
            result_text.insert(tk.END, f"Class {j + 1} - {class_info['Name']} ({class_info['Course Number']}):\n")
            for key, value in session.items():
                result_text.insert(tk.END, f'"{key}": {value}\n')
            result_text.insert(tk.END, "\n")
        result_text.insert(tk.END, "\n")


# Create a Tkinter window
root = tk.Tk()
root.title("Course Schedule Generator")

# Create and configure input fields for course numbers
course_number_entries = []
for i in range(5):
    label = tk.Label(root, text=f"Enter course number {i + 1}:")
    label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    course_number_entries.append(entry)

# Create a button to generate schedules
generate_button = tk.Button(root, text="Generate Schedule", command=get_schedule)
generate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Create a text area to display schedules
result_text = tk.Text(root, height=20, width=60)
result_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()
