import csv
from datetime import datetime
import matplotlib.pyplot as plt
import os
import re
from statistics import mean
import sys


def main():

    WEIGHT_FIELDS = ["Date", "Weight"]
    MACROS_FIELDS = ["Date", "Calories", "Protein (g)", "Fat (g)", "Carbs (g)"]

    # Get inputs
    weight_file, macros_file, year = get_files_year()

    # Collect data from csv
    try:
        weight_data = collect_data(weight_file, WEIGHT_FIELDS)
        macros_data = collect_data(macros_file, MACROS_FIELDS)
    except ValueError as err:
        sys.exit(err)

    # Cleanup the data in the files
    try:
        weight_clean = clean_data(weight_data, year)
        macros_clean = clean_data(macros_data, year)
    except ValueError as err:
        sys.exit(err)

    # Average the data
    weight_average = average_data(weight_clean)
    macros_average = average_data(macros_clean)

    # Save the graph and print save location
    try:
        print(draw_graph(weight_average, macros_average, year)) 
    except KeyError:
        sys.exit("Something went wrong. You might have switched up your file inputs.")


def collect_data(f: str, fields: list) -> list:
    """ 
    Collect data from CSV file.

    :param f: File to read from
    :type f: str
    :param fields: Fields to read and return
    :type fields: list
    :raise ValueError: If fields is empty. If specified fields are missing/incorrect in the file
        If no data was appended
    :return: A list of dictionaries containing specified fields and their values, one dict per row
    :rtype: list
    """

    data = []
    file_name = os.path.split(f)
    missing_fields = []

    if fields == []:
        raise ValueError("Please provide a list of fields (str)")

    with open(f, "r") as file:
        reader = csv.DictReader(file)

        # Get fieldnames
        csv_fields = reader.fieldnames

        # Check that the included fields are present, otherwise exit
        for field in fields:
            if field not in csv_fields:
                missing_fields.append(field)
        if missing_fields != []:
           raise ValueError(f'{*missing_fields,} field(s) missing/incorrect in: "{file_name[1]}"')
        
        # Go through the csv, if a field is not supposed to be included, remove it
        for row in reader:
            for field in csv_fields:
                if field not in fields:
                    row.pop(field)

            data.append(row)
    if data == []:
        raise ValueError("No data was appended")
    
    return data


def clean_data(data: list, year: str) -> list:
    """ 
    Clean data from list of dictionaries using year to limit what data to clean and return.
    The key "Date" containing the date (YYYY-MM-DD) is required. Converts str values to float 
    and omits entries that have atleast one empty value.

    :param data: List of dictionaries to clean
    :type data: list
    :param year: Year to limit what to clean and return
    :type year: str
    :raise ValueError: If key "Date" missing. If there are no entries for given year. 
        Data input contains no values for some or all fields.
    :return: A list of dictionaries with dates corresponding to the given year, containing the 
        fields (keys) provided in the list of dictionaries with their values converted to float.
    :rtype: list
    """

    data_year = []
    fields = data[0].keys()
    cleaned_data = []

    if "Date" not in fields:
        raise ValueError('Missing required key "Date"')

    for row in data:
        # Only append if the given year is in the datasets "Date" field
        if year in row["Date"][:4]:
            data_year.append(row)
    
    if data_year == []:
        raise ValueError(f"Data contains no entries for {year}")
    
    # For each row in original data, for each field in that row, convert the value to float
    for row in data_year:
        for field in fields:
            blank = []

            # Convert str to float, skip the value if it's empty
            if row[field] == "" or "," in row[field]:
                try:
                    row[field] = float(row[field].replace(",", ".").strip())
                except ValueError:
                    blank.append("")
                    break
            # Convert str to float, skip if the value is not numbers only
            elif row[field].isdigit():
                 row[field] = float(row[field])
            # Do nothing if the field is "Date"
            elif field == "Date":
                pass
            else:
                blank.append("")
                break
        
        # If there are no empty values append row to cleaned_data
        if "" not in blank:
            cleaned_data.append(row)

    # If not data was appended show message and exit, otherwise return the data
    if cleaned_data == []:
        raise ValueError(f'Data input contains no values for some or all of the following: {*fields,}')
    else:
        return cleaned_data
    

def average_data(data: list) -> dict:
    """ 
    Averages the data from a list of dictionaries, returning a dictionary. The new dictionary will
    omit the key "Date" (used only to collect and store averages for a given month). Each of the other
    keys' values will be another dictionary, containing the month as key and average as value. The key 
    "Date" containing the date (YYYY-MM-DD) is required. 

    :param data: A list of dictionaries
    :type data: list
    :return: A dictionary containing each key (except "Date"), with the values being a dictionary of
        the months and their average.
    :rtype: dict
    """
    # Remove "Date" from fields so it won't try to append and average the dates
    fields = [*data[0].keys()]
    fields.remove("Date")

    averages = {}

    for field in fields:
        # Reset the dict so it won't keep appending to the values of the previous field
        month_data = {}

        for row in data:

            # Extract date YYYY-MM-DD format
            date_day = datetime.strptime(row["Date"], r"%Y-%m-%d")
            
            # Format month num to month str, ex. 10 to October
            month_str = "{0:%B}".format(date_day)     
            
            # If month (str), not in dict store the data for that month in a list as the value for the month
            if month_str not in month_data:
                month_data[month_str] = [row[field]]
            else:
                month_data[month_str].append(row[field])

        # Store the averages per month as the value for the specific field
        if field not in averages:
            averages[field] = {month: round(mean(month_data[month]), 1) for month in month_data}

    return averages


def get_files_year() -> list:
    """ 
    Ask questions needed in order to get two CSV files and a valid year in YYYY format. Keep
    asking until valid responses are given.

    :raise FileNotFoundError: If the file doesn't exist
    :return: A list of file names and a year
    :rtype: list
    """
    # Questions to ask the user
    questions = ["Weight file: ", "Macros file: ", "Year: "]
    responses = []
 
    # Get input from the user and store in a list
    i = 0
    while True:

        # Get the file inputs from the user, with extension and error checking
        if i < len(questions)-1:
            response = input(questions[i])  
            extension = os.path.splitext(response)
            if extension[1] != ".csv":
                print(f"{response} is not a CSV")
                continue
            try:
                with open(response):        
                    i += 1
                    responses.append(response)
                    continue
            except FileNotFoundError:
                print(f"{response} does not exist")
                continue

        # Validate that the year is in YYYY format and return a list with the responses
        elif "Year" in questions[i]:
            response = input(questions[i])
            if _ := re.search(r"^(\d{4}){1}$", response):
                responses.append(response)
                return responses
            else:
                print(f"Please provide a year in YYYY format")
                continue


def draw_graph(weight_dict: dict, macros_dict: dict, year: str) -> str:
    """ 
    Plots a line graph for average weight, and a bar graph for average macros (calories, protein,
    fat, carbs). Saves the figure (.png) in the current working directory. 

    :param weight_dict: A dictionary containing average weight for month(s)
    :type weight_dict: dict
    :param macros_dict: A dictionary containing average macros for month(s)
    :type macros_dict: dict
    :param year: Year the average is for
    :type year: str
    :return: String displaying where file was saved
    :rtype: str
    """

    # Store the keys for weight & macros in one list each, no need to store for each macro since they're the same
    weight_keys = [key for key in weight_dict["Weight"].keys()]
    calories_keys = [key for key in macros_dict["Calories"].keys()]

    # Store the values for weight & macros in separate lists, convert macro values to int to avoid decimals in graph
    weight_values = [value for value in weight_dict["Weight"].values()]
    calories_values = [int(value) for value in macros_dict["Calories"].values()]
    protein_values = [int(value) for value in macros_dict["Protein (g)"].values()]
    fat_values = [int(value) for value in macros_dict["Fat (g)"].values()]
    carbs_values = [int(value) for value in macros_dict["Carbs (g)"].values()]

    # Make a separate list for calories height to avoid the bar scales being too different
    calories_height = [key * 0.25 for key in macros_dict["Calories"].values()]

    # Set style
    #plt.style.use('dark_background')
    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

    # Create plot object
    fig, (ax1, ax2) = plt.subplots(2, figsize=(16, 9))

    # Set graph title
    plt.suptitle(f"Averages {year}", size=25, weight="bold", y=0.96)

    # Create line plot
    ax1.plot(
        weight_keys, weight_values, linewidth=3, markersize=10, marker="o", color="deepskyblue", 
        markerfacecolor="dodgerblue", label="Avg. Weight"
        )

    # Plot styling for ax 1
    ax1.spines[["right", "top", "left", "bottom"]].set_visible(False)
    ax1.grid(linestyle = "dashed", color="white", alpha=0.2)
    ax1.tick_params(color="lightgray")
    ax1.set_ylabel('Weight', size=18, weight="bold", style="italic", labelpad=20)

    # Set labels for weight
    weight_labels = [tick for tick in range(len(weight_keys))]
    ax1.set_xticks(weight_labels)
    ax1.set_xticklabels(weight_keys, weight="bold")

    width = 0.21

    # Offsets for bar positions
    x_calories = [x - (width * 1.5) for x in range(len(calories_values))]
    x_protein = [x - (width / 2) for x in range(len(protein_values))]
    x_fat = [x + (width / 2) for x in range(len(fat_values))]
    x_carbs = [x + (width * 1.5) for x in range(len(carbs_values))]

    # Set lables on x-axis for macros
    macro_labels = [tick for tick in range(len(calories_keys))]
    ax2.set_xticks(macro_labels)
    ax2.set_xticklabels(calories_keys, weight="bold")

    # Create bars for macros
    ax2.bar(x_calories, calories_height, width, label="Calories", fc="springgreen")
    ax2.bar(x_protein, protein_values, width, label="Protein", fc="dodgerblue")
    ax2.bar(x_fat, fat_values, width, label="Fat", fc="deepskyblue")
    ax2.bar(x_carbs, carbs_values, width, label="Carbs", fc="aquamarine")

    # Add a label to each bar, use calories values for calorie bars because they are scaled down with 
    # alternative values (calories_height)
    for c in ax2.containers:

        # c is bar containter object
        label = c.get_label()
        if label == "Calories":
            ax2.bar_label(c, labels=calories_values, weight="bold", color="white")

        else:
            ax2.bar_label(c, weight="bold", color="white")
    
    # Plot styling for ax2
    ax2.spines[["right", "top", "left", "bottom"]].set_visible(False)
    ax2.grid(linestyle ="dashed", color="white", alpha=0.2)
    ax2.tick_params(left=0, labelleft=0, color="lightgray")
    ax2.set_ylabel('Macros', size=18, weight="bold", style="italic", labelpad=20)

    # Align the labels describing the category i.e "Weight" and "Macros"
    fig.align_ylabels([ax1, ax2])

    # Show legends
    ax1.legend(frameon=1, shadow=1, framealpha=1.0, borderpad=0.8, bbox_to_anchor=(1.0, 1.05), loc="upper left")
    ax2.legend(frameon=1, shadow=1, framealpha=1.0, borderpad=0.8, bbox_to_anchor=(1.0, 1.05), loc="upper left")

    # Show plot
    #plt.show()
    # Save plot
    cwd = os.getcwd()
    plt.savefig(f"{cwd}\\averages_{year}")

    return f"File saved: {cwd}\\averages_{year}.png"


if __name__ == "__main__":
    main()