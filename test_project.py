from project import collect_data, clean_data, average_data, get_files_year, draw_graph
import os
import pytest

def test_collect_data():
    # Test files with data
    assert collect_data("test_weight.csv", ["Date", "Weight"]) == [{'Date': '2023-03-27', 'Weight': '74,5'}, 
                                                                   {'Date': '2023-03-28', 'Weight': '73,6'}, 
                                                                   {'Date': '2023-04-01', 'Weight': '74,1'}, 
                                                                   {'Date': '2023-04-02', 'Weight': '74,3'}, 
                                                                   {'Date': '2023-04-03', 'Weight': ''}, 
                                                                   {'Date': '2023-04-04', 'Weight': ''}]
    assert collect_data("test_intake.csv", ["Date", "Calories", "Protein (g)", "Fat (g)", "Carbs (g)"]) == [{'Date': '2022-07-25', 'Calories': '1611', 'Protein (g)': '182', 'Fat (g)': '40', 'Carbs (g)': '120'}, 
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
    # Missing fields
    with pytest.raises(ValueError) as info:
        assert collect_data("test_intake_noFields.csv", ["Date", "Calories", "Protein (g)", "Fat (g)", "Carbs (g)"])
    assert str(info.value) == '(\'Date\', \'Calories\', \'Protein (g)\', \'Fat (g)\', \'Carbs (g)\') field(s) missing/incorrect in: "test_intake_noFields.csv"'
    # Missing date field
    with pytest.raises(ValueError) as info:
        assert collect_data("test_weight_noDate_field.csv", ["Date", "Weight"])
    assert str(info.value) == '(\'Date\',) field(s) missing/incorrect in: "test_weight_noDate_field.csv"'
    # No columns provided to function
    with pytest.raises(ValueError) as info:
        assert collect_data("test_intake.csv", [])
    assert str(info.value) == "Please provide a list of fields (str)"
    # No data in the file
    with pytest.raises(ValueError) as info:
        assert collect_data("test_intake_noData.csv", ["Date", "Calories", "Protein (g)", "Fat (g)", "Carbs (g)"])
    assert str(info.value) == "No data was appended"


def test_clean_data():
    # Variables with data so it will work even if collect_data was to break
    weight_data = [ {'Date': '2023-03-27', 'Weight': '74,5'}, 
                    {'Date': '2023-03-28', 'Weight': '73,6'}, 
                    {'Date': '2023-04-01', 'Weight': '74,1'}, 
                    {'Date': '2023-04-02', 'Weight': '74,3'}, 
                    {'Date': '2023-04-03', 'Weight': ''}, 
                    {'Date': '2023-04-04', 'Weight': ''}
                    ]
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
                    {'Date': '2023-02-02', 'Calories': '1888', 'Protein (g)': '184', 'Fat (g)': '61', 'Carbs (g)': '144'}
                    ]
    macros_no_date = [  {'Calories': '1611', 'Protein (g)': '182', 'Fat (g)': '40', 'Carbs (g)': '120'}, 
                        {'Calories': '1562', 'Protein (g)': '163', 'Fat (g)': '50', 'Carbs (g)': '111'}, 
                    ]
    macros_no_values = [{'Date': '2023-01-01', 'Calories': '', 'Protein (g)': None, 'Fat (g)': None, 'Carbs (g)': None}]
    empty_year = "2024"
    # Returns clean data
    assert clean_data(weight_data, "2023") == [ {'Date': '2023-03-27', 'Weight': 74.5}, 
                                                {'Date': '2023-03-28', 'Weight': 73.6}, 
                                                {'Date': '2023-04-01', 'Weight': 74.1}, 
                                                {'Date': '2023-04-02', 'Weight': 74.3}]
    
    assert clean_data(macros_data, "2023") == [ {'Date': '2023-01-02', 'Calories': 1588.0, 'Protein (g)': 203.0, 'Fat (g)': 39.0, 'Carbs (g)': 105.0}, 
                                                {'Date': '2023-01-29', 'Calories': 1986.0, 'Protein (g)': 209.0, 'Fat (g)': 41.0, 'Carbs (g)': 190.0}, 
                                                {'Date': '2023-01-30', 'Calories': 1832.0, 'Protein (g)': 215.0, 'Fat (g)': 48.0, 'Carbs (g)': 130.0}, 
                                                {'Date': '2023-01-31', 'Calories': 1836.0, 'Protein (g)': 215.0, 'Fat (g)': 43.0, 'Carbs (g)': 141.0}, 
                                                {'Date': '2023-02-01', 'Calories': 2086.0, 'Protein (g)': 203.0, 'Fat (g)': 54.0, 'Carbs (g)': 189.0}, 
                                                {'Date': '2023-02-02', 'Calories': 1888.0, 'Protein (g)': 184.0, 'Fat (g)': 61.0, 'Carbs (g)': 144.0}]
    # Year not in csv
    with pytest.raises(ValueError) as info:
        assert clean_data(macros_data, empty_year)
    #assert info.value.args[0] == '"test_intake.csv" contains no values for Date and/or (\'Calories\', \'Protein (g)\', \'Fat (g)\', \'Carbs (g)\') or no data is recorded for "2024"'
    assert str(info.value) == f"Data contains no entries for {empty_year}"

    # Input has no values
    with pytest.raises(ValueError) as info:
        assert clean_data(macros_no_values, "2023")
    str(info.value) == "Data input contains no values for some or all of the following: ('Date', 'Calories', 'Protein (g)', 'Fat (g)', 'Carbs (g)')"

    with pytest.raises(ValueError) as info:
        assert clean_data(macros_no_date, "2023")
    str(info.value) == 'Missing required key "Date"'


def test_average_data():
    macros_clean = [{'Date': '2023-01-02', 'Calories': 1588.0, 'Protein (g)': 203.0, 'Fat (g)': 39.0, 'Carbs (g)': 105.0}, 
                    {'Date': '2023-01-29', 'Calories': 1986.0, 'Protein (g)': 209.0, 'Fat (g)': 41.0, 'Carbs (g)': 190.0}, 
                    {'Date': '2023-01-30', 'Calories': 1832.0, 'Protein (g)': 215.0, 'Fat (g)': 48.0, 'Carbs (g)': 130.0}, 
                    {'Date': '2023-01-31', 'Calories': 1836.0, 'Protein (g)': 215.0, 'Fat (g)': 43.0, 'Carbs (g)': 141.0}, 
                    {'Date': '2023-02-01', 'Calories': 2086.0, 'Protein (g)': 203.0, 'Fat (g)': 54.0, 'Carbs (g)': 189.0}, 
                    {'Date': '2023-02-02', 'Calories': 1888.0, 'Protein (g)': 184.0, 'Fat (g)': 61.0, 'Carbs (g)': 144.0}
                    ]
    # Returns dict with averages
    assert average_data(macros_clean) == {'Calories': {'January': 1810.5, 'February': 1987.0}, 
                                        'Protein (g)': {'January': 210.5, 'February': 193.5}, 
                                        'Fat (g)': {'January': 42.8, 'February': 57.5}, 
                                        'Carbs (g)': {'January': 141.5, 'February': 166.5}}
    
    weight_clean = [{'Date': '2023-03-27', 'Weight': 74.5}, 
                    {'Date': '2023-03-28', 'Weight': 73.6}, 
                    {'Date': '2023-04-01', 'Weight': 74.1}, 
                    {'Date': '2023-04-02', 'Weight': 74.3}
                    ]
    assert average_data(weight_clean) == {'Weight': {'March': 74.0, 'April': 74.2}}


def test_get_files_year(monkeypatch):
    # inputs is an iterator object, allowing the call of next to go through the list.
    # setattr on the built-in (python) input function, set the value to current
    # iteration of inputs. Essentially "pathcing" input() to return desired value
    inputs = iter(["test_weight.csv", "test_intake.csv", "2023"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    # Store the value returned by the function and assert 
    returns = get_files_year()
    assert returns == ["test_weight.csv", "test_intake.csv", "2023"]

    # Incorrect inputs, will prompt again so it should still get the correct values
    inputs = iter([" ", "test_weight.csv", "cat", "test_intake.csv", "ad02", "2023"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    # Store the value returned by the function and assert 
    returns = get_files_year()
    assert returns == ["test_weight.csv", "test_intake.csv", "2023"]


def test_draw_graph():
    year = "2023"
    macros_avg = {'Calories': {'January': 1810.5, 'February': 1987.0}, 
                'Protein (g)': {'January': 210.5, 'February': 193.5}, 
                'Fat (g)': {'January': 42.8, 'February': 57.5}, 
                'Carbs (g)': {'January': 141.5, 'February': 166.5}}
    weight_avg = {'Weight': {'March': 74.0, 'April': 74.2}}
    with pytest.raises(KeyError):
        draw_graph(macros_avg, weight_avg, year)

    cwd = os.getcwd()
    assert draw_graph(weight_avg, macros_avg, year) == f"File saved: {cwd}\\averages_{year}.png"

# https://pavolkutaj.medium.com/simulating-single-and-multiple-inputs-using-pytest-and-monkeypatch-6968274f7eb9