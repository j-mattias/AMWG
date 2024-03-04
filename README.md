# Average Macros & Weight Graph
### Description:
The project was created in order to be able to visualize with a simple graph, the average weight and macros (calories, protein, fat and carbs) for each month during a given year. Since I track my weight and intake each day I thought it would be nice to have an easy way to do just that without any extra fluff, tailored to my personal needs.

## Summary:
The program will take three inputs, _Weight (csv file)_, _Macros (csv file)_ and _Year (The year to average data from)_. The data it processes is based on the format I've been using to track each day. In the weight file it will expect the fieldnames: _Date_ and _Weight_. In the macros file it will expect the fieldnames: _Date_, _Calories_, _Protein (g)_, _Fat (g)_ and _Carbs (g)_. It will run some error checking to make sure that the expected fields are present and check that there's data for the fields and given year. It will then average the data and pass it along to create the graph saving it as a .png file and finally printing out the directory where it was saved (the current working directory). 

## Files:
**project.py (Main file)**
The main file contains _five_ functions.
### collect_data
Takes a csv file, and a list of the fields you want to parse and then returns a list of dictionaries for each relevant row. If the provided list is empty it will raise a ValueError. If one or more of the fields provided in the list are missing in the file input, it will raise a ValueError, specifying which fields are missing as well as the name of the relevant file. If there was no data in the file it will raise a ValueError.

```python
collect_data(f: str, fields: list) -> list
```
Example:
> "macros.csv" <br />
>Date, Calories, Protein (g), Fat (g), Carbs (g), Cat <br />
>2023-01-30,1832,215,48,130, <br />
>2023-01-31,1836,215,43,141, <br />

```python
collect_data("macros.csv", ["Date", "Calories", "Protein (g)", "Fat (g)", "Carbs (g)"])

returns:
[{'Date': '2023-01-30', 'Calories': '1832', 'Protein (g)': '215', 'Fat (g)': '48', 'Carbs (g)': '130'},
 {'Date': '2023-01-31', 'Calories': '1836', 'Protein (g)': '215', 'Fat (g)': '43', 'Carbs (g)': '141'}] 
```
### clean_data
Takes a list of dictionaries and a year (YYYY format). Expects a list of dictionaries, "Date" is a required key, and one or more keys that can be converted to float (weight or macros in the context of this program). The year will limit the data that gets returned to that specific year, as well as only do the "cleaning" for that year. If the provided list doesn't contain a "Date" key it will raise a ValueError. If there are no entries for the provided year it will raise a ValueError. If a field contains a blank value it will skip that row. The reason for that is to avoid averaging with blank values and if a row had a blank value the rest of the row likely did as well based on how I do my tracking. If no data was gathered it will raise a ValueError.
    
```python
clean_data(data: list, year: str) -> list
```
Example:
    
```python
macros_data = [ {'Date': '2022-07-25', 'Calories': '1611', 'Protein (g)': '182', 'Fat (g)': '40', 'Carbs (g)': '120'}, 
                {'Date': '2022-07-26', 'Calories': '1562', 'Protein (g)': '163', 'Fat (g)': '50', 'Carbs (g)': '111'}, 
                {'Date': '2022-12-31', 'Calories': '', 'Protein (g)': '', 'Fat (g)': '', 'Carbs (g)': ''}, 
                {'Date': '2023-01-01', 'Calories': '', 'Protein (g)': '', 'Fat (g)': '', 'Carbs (g)': ''}, 
                {'Date': '2023-01-02', 'Calories': '1588', 'Protein (g)': '203', 'Fat (g)': '39', 'Carbs (g)': '105'}, 
                {'Date': '2023-01-03', 'Calories': '', 'Protein (g)': '', 'Fat (g)': '', 'Carbs (g)': ''}, 
                {'Date': '2023-01-29', 'Calories': '1986', 'Protein (g)': '209', 'Fat (g)': '41', 'Carbs (g)': '190'}, 
                {'Date': '2023-01-30', 'Calories': '1832', 'Protein (g)': '215', 'Fat (g)': '48', 'Carbs (g)': '130'}, 
                {'Date': '2023-01-31', 'Calories': '1836', 'Protein (g)': '215', 'Fat (g)': '43', 'Carbs (g)': '141'}, 
                {'Date': '2023-02-01', 'Calories': '2086', 'Protein (g)': '203', 'Fat (g)': '54', 'Carbs (g)': '189'}, 
                {'Date': '2023-02-02', 'Calories': '1888', 'Protein (g)': '184', 'Fat (g)': '61', 'Carbs (g)': '144'}]

clean_data(macros_data, "2023")

returns:
[{'Date': '2023-01-02', 'Calories': 1588.0, 'Protein (g)': 203.0, 'Fat (g)': 39.0, 'Carbs (g)': 105.0}, 
{'Date': '2023-01-29', 'Calories': 1986.0, 'Protein (g)': 209.0, 'Fat (g)': 41.0, 'Carbs (g)': 190.0}, 
{'Date': '2023-01-30', 'Calories': 1832.0, 'Protein (g)': 215.0, 'Fat (g)': 48.0, 'Carbs (g)': 130.0}, 
{'Date': '2023-01-31', 'Calories': 1836.0, 'Protein (g)': 215.0, 'Fat (g)': 43.0, 'Carbs (g)': 141.0}, 
{'Date': '2023-02-01', 'Calories': 2086.0, 'Protein (g)': 203.0, 'Fat (g)': 54.0, 'Carbs (g)': 189.0}, 
{'Date': '2023-02-02', 'Calories': 1888.0, 'Protein (g)': 184.0, 'Fat (g)': 61.0, 'Carbs (g)': 144.0}]
```
### average_data
Expects a list of dicitonaries, "Date" is a required key, and one or more keys with int or float values. The "Date" key is necessary in order to convert the date in YYYY-MM-DD format to a text format for each month (i.e. 2023-10-21 gets converted to "October"). It will extract the keys from the first dictionary in the provided list (since it expects all the dictionaries to be the same keys). "Date" will then be removed as it's not a key we want to average values for, but it's necessary to extract the months. Following that it iterates over each key (ex: "Calories", "Protein (g)", "Fat (g)", "Carbs (g)"), and the values for that month then gets appended to a list and stored in a temporary dictionary with the month (converted to text) being the key and the list of values being the value. If the key (ex: "Calories" ) is not in the dictionary that is to be returned, it will add that key and assign the value to be a dictionary of the months as keys and averages as values for the corresponding months.
    
```python
average_data(data: list,) -> dict
```
Example:
    
```python
macros_clean = [{'Date': '2023-01-02', 'Calories': 1588.0, 'Protein (g)': 203.0, 'Fat (g)': 39.0, 'Carbs (g)': 105.0}, 
                {'Date': '2023-01-29', 'Calories': 1986.0, 'Protein (g)': 209.0, 'Fat (g)': 41.0, 'Carbs (g)': 190.0}, 
                {'Date': '2023-01-30', 'Calories': 1832.0, 'Protein (g)': 215.0, 'Fat (g)': 48.0, 'Carbs (g)': 130.0}, 
                {'Date': '2023-01-31', 'Calories': 1836.0, 'Protein (g)': 215.0, 'Fat (g)': 43.0, 'Carbs (g)': 141.0}, 
                {'Date': '2023-02-01', 'Calories': 2086.0, 'Protein (g)': 203.0, 'Fat (g)': 54.0, 'Carbs (g)': 189.0}, 
                {'Date': '2023-02-02', 'Calories': 1888.0, 'Protein (g)': 184.0, 'Fat (g)': 61.0, 'Carbs (g)': 144.0}]

average_data(macros_clean)

returns:
{'Calories': {'January': 1810.5, 'February': 1987.0}, 
'Protein (g)': {'January': 210.5, 'February': 193.5}, 
'Fat (g)': {'January': 42.8, 'February': 57.5}, 
'Carbs (g)': {'January': 141.5, 'February': 166.5}}
```
### get_files_year
This function is simply to ask three questions and get input, that's specific to this program in order to get two CSV files and a valid year. It take's not input and it's not a particularly reusable function outside of the context of this program. It will first get the two files, if the user inputs a file other than a csv or a file that doesn't exist, they will be reprompted. Once two valid files have been collected it will ask for a year, if it's not in YYYY format it will prompt again. When all questions have been answered it will return a list of the answers.
    
```python
get_files_year() -> list:
```
Example:
    
```python
get_files_year()
```
```
Weight file: weight.csv
Macros file: macros.txt
macros.txt is not a CSV
Macros file: macros1.csv
macros1.csv does not exist
Macros file: macros.csv
Year: cat2
Please provide a year in YYYY format
Year: 2023

returns:
["weight.csv", "macros.csv", "2023"]
```
### draw_graph
Expects two dictionaries and a year as a string, and will draw a graph with two subplots, one for weight as a line graph and another for macros as a bar graph. The first dictionary should have a key "Weight" with its value being another dictionary containing keys and values for the months and their average. The second dictionary is much the same except it will contain a key for each macro with the value being another dictionary with the months and their average. It will apply some styling and formatting to the graph and save it as a _.png_ in the current working directory. It returns a string confirming where the file has been saved.
    
```python
draw_graph(weight_dict: dict, macros_dict: dict, year: str) -> str:
```
Example:
    
```python
weight_avg = {'Weight': {'March': 74.0, 'April': 74.2}}
macros_avg = {'Calories': {'January': 1810.5, 'February': 1987.0}, 
            'Protein (g)': {'January': 210.5, 'February': 193.5}, 
            'Fat (g)': {'January': 42.8, 'February': 57.5}, 
            'Carbs (g)': {'January': 141.5, 'February': 166.5}}
year = "2023"

draw_graph(weight_avg, macros_avg, year)

returns:
"File saved: ..\averages_2023.png"
```

![Example image of what the graph of weight and macros averages looks like](https://github.com/j-mattias/AMWG/blob/main/averages_2023.png?raw=true)

**test_project.py (Unit tests)**
The test file contains a number of unit tests, using pytest, for each of the functions in the main file.

**requirments.txt**
This file contains the required pip installable libraries in order to run the program.

**Misc**
Some other miscellaneous files are included in the project such as "test_....csv" files which are used in order to perform the unit tests.

## Design choices & Reasoning:

### collect_data
Was made to be a reusable function that could be used to extract any specified field(s) from a CSV file. I thought that it would be nice to be able to only extract the data you wanted rather than all of it. It has some errors that can be raised built-in so that a message could be displayed for the user to figure out what might've gone wrong. Earlier on in the project it was more specific towards what fields it was looking for, and also did the cleaning of the data in the same function. However it made it feel less reusable and harder to keep track of, so it was abstracted away and separated into two separate functions.


### clean_data
Mostly tailored towards this project itself as way to clean up and convert data to suit the needs of this program. As the program requires to be able to average the numbers provided, the data collected as strings needs to be converted. It has some errors that can be raised built-in so that a message could be displayed for the user to figure out what might've gone wrong.


### average_data
Much like clean_data it's mostly tailored towards this project as it expects a "Date" field and some other fields with divisible values. I decided to make it return a dictionary so that I could store all the fields for one file in one place, rather than creating a loop in the main function.

### get_files_year
Was made to abstract away getting input from the user, very specific to this particular program. As well as to be able to validate the files and year during input in order to not immediately exit if there was invalid input. At first I was going to use argparse to get the input, but decided against that since it'd be nicer to validate the input right away.

### draw_graph
Early on when planning for the project I was considering using PySide6 to draw the graph, but decided to go with matplotlib as there wasn't really a reason to provide a GUI. At first I also wanted to have the graphs use the same plot, but because of the large difference in the values between macros and weight it would flatten the curve significantly. Along with some other issues, which led to splitting them into two subplots which ended up much cleaner and being a nicer visual representation of the data.
