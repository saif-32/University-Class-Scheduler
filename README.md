# University Class Scheduler

## Introduction

This Python program is a University Class Scheduler that helps you generate possible schedules for your university courses.

## Getting Started

To use this program, you'll need to have the following dependencies installed on your system:

- Python
- tkinter (Python GUI library)
- Selenium (Python library for web automation)
- ChromeDriver

You can install the required Python libraries using pip:

```bash
pip install tkinter selenium
```

Additionally, you'll need to download ChromeDriver (https://sites.google.com/chromium.org/driver/) and specify the path to the ChromeDriver executable in the `Service` object inside the `scrape_class_times` function:

```python
s = Service("/path/to/chromedriver")
```

## How to Use

1. Run the Python script, and a GUI window will appear.
2. Enter up to five course numbers in the input fields provided.
3. Click the "Generate Schedule" button to initiate the schedule generation process.

The program will then scrape the course information for the provided course numbers, generate all possible schedule combinations without time conflicts, and display them in the text area provided.

## Program Structure

The program is structured as follows:

- It uses tkinter to create a graphical user interface (GUI) for input and output.
- It uses Selenium to automate web scraping of course information from the course registration website.
- The `scrape_class_times` function extracts class information for the specified course numbers.
- The `generate_schedule_combinations` function generates all possible schedule combinations without time conflicts.
- The `has_conflict` function checks if there is a time conflict between two class sessions.
- The `overlaps` function checks if two time intervals overlap.
- The `parse_time` function converts a time string (e.g., "7:30am") to minutes since midnight.
- The `get_schedule` function coordinates the entire process, from web scraping to schedule generation and display.

## Disclaimer

This program is intended for educational purposes only. Be sure to abide by your university's course registration policies and procedures when using it.

## Support and Contributions

If you encounter issues or have suggestions for improvements, please feel free to contribute to the project by submitting issues or pull requests on GitHub.

Enjoy using the University Class Scheduler!
