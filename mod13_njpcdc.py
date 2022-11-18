from datetime import date, datetime
import pygal
import requests
import json
import lxml

#API KEY 
API_KEY = "AH4E9KX41PXBFQQI"

#commit test - ella 

#Symbol Selection 
SYMBOL = input("Enter the stock symbol you would like to use: ")

if SYMBOL.isalpha() == True and len(SYMBOL) <= 7 and SYMBOL.isupper() == True:
    print("Valid Symbol")
else:
    print("Invalid Symbol: Please ensure that the input contains only capitalied alphabetic characters")
    SYMBOL = input("Enter the stock symbol you would like to use: ")

def select_chart_type():
    # Note: when calling this method, it must be set to a variable as it returns an
    # instance of the graph selected (Line or Bar)

    # Printed menu
    print('\nChart Types')
    print('---------------')
    print('1. Bar')
    print('2. Line')

    # Input validation
    chart_selection = 0
    while True:
        try:
            chart_selection = int(input('Select a chart type: '))
            if chart_selection < 1 or chart_selection > 2:
                print('Invalid input! Chart selection must be one of the provided options.')
                continue
            else:
                break
        except ValueError:
            print('Invalid input! Chart selection must be a number 1 or 2.')

    # Return an instance of the chart selected by the user
    if chart_selection == 1:
        return "Bar"
    elif chart_selection == 2:
        return "Line"

def select_time_series():
    #user selection
    print("\nSelect the time series of the chart that you want generate")
    print("----------------------------------------------------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")

    #dictionary of all the choices
    # times = {
    #     "Intraday" : "TIME_SERIES_INTRADAY",
    #     "Daily" : "TIME_SERIES_DAILY_ADJUSTED",
    #     "Weekly" : "TIME_SERIES_WEEKLY",
    #     "Monthly" : "TIME_SERIES_MONTHLY",
    # }

    # List of choices (so choice is accessible via index)
    time_choices = ["TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY_ADJUSTED", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY"]

    time_selection = ""
    time_series_selection = ""

    # Input validation
    while True:
        #user input selection
        time_series_selection = input("Enter the time series option you would like to select: ")
        try:
            #new variable is assigned based on selection
            #time_selection = times_[timeSeriesSelection]
            time_selection = time_choices[int(time_series_selection) - 1]
            if (int(time_series_selection) <= 0):
                print('Invalid input! Time series selection must be a number 1-4.')
                continue
            else:
                break
        except ValueError:
            print('Invalid input! Time series selection must be a number 1-4.')
        except IndexError:
            print('Invalid input! Time series selection must be a number 1-4.')

    if time_series_selection == "1":    # "1" is the equivalent option for Intraday

        print("\nTime intervals")
        print("---------------")
        print("1 - 1 minute")
        print("5 - 5 minutes")
        print("15 - 15 minutes")
        print("30 - 30 minutes")
        print("60 - 60 minutes")

        #dictionary of all choices
        intervals = {
            "1" : "1min",
            "5" : "5min",
            "15" : "15min",
            "30" : "30min",
            "60" : "60min",
        }

        interval_selection = ""
        while True:
            interval_series_selection = input("Enter a time interval that you would like to select:")
            try:
                interval_selection = intervals[interval_series_selection]
                break
            except:
                print('Invalid input! Interval selection must be a number 1, 5, 15, 30, or 60.')

        return [time_selection, interval_selection]
    else:
        return [time_selection, ""]
    
def select_beginning_end_dates():

    start_date = datetime.min
    end_date = datetime.now

    while True: 
        try: 
            start_date = input("\nEnter the start date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            break
        except ValueError:
            print("Incorrect data format, should be YYYY-MM-DD")

    while True: 
        try: 
            end_date = input("Enter the end date (YYYY-MM-DD): ")
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            if end_date > start_date:
                break
            else: 
                print("Incorrect data format, End date should occur after the start date.")
        except ValueError: 
            print("Incorrect data format, should be YYYY-MM-DD.")

    return [start_date, end_date]

    # start_date = input("Enter the start date: (YYYY-MM-DD) ")
    # end_date = input("Enter the end date: (YYYY-MM-DD) ")
    # start_date = start_date.split("-")
    # print(datetime(int(start_date[0]), int(start_date[1]), int(start_date[2])))

def build_URL(time_selection):
    if time_selection[0] != "":
        global ogURL
        ogURL = "https://www.alphavantage.co/query?function={}&symbol={}&interval={}&apikey={}".format(time_selection[0], SYMBOL, time_selection[1], API_KEY)
    else:
        ogURL = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(time_selection[0], SYMBOL, API_KEY)
    return ogURL

def parse_json(request_url, date_range, time_series):
    response = requests.get(request_url).text
    response_data = json.loads(response)

    data_title = ""
    data = []
    if time_series[0] == "TIME_SERIES_INTRADAY":
        # Time Series (5min)
        data_title = "Time Series ({})".format(time_series[1])
    elif time_series[0] == "TIME_SERIES_DAILY_ADJUSTED":
        data_title = "Time Series (Daily)"
    elif time_series[0] == "TIME_SERIES_WEEKLY":
        data_title = "Weekly Time Series"
    elif time_series[0] == "TIME_SERIES_MONTHLY":
        data_title = "Monthly Time Series"

    date_format = ''
    if data_title == "Time Series ({})".format(time_series[1]):
        date_format = '%Y-%m-%d %H:%M:%S'
    else:
        date_format = '%Y-%m-%d'

    for entry in response_data[data_title]:
        raw_datetime = datetime.strptime(entry, date_format)
        if raw_datetime >= date_range[0] and raw_datetime <= date_range[1]:
            data.append({'Date':entry, 'Data':response_data[data_title][entry]})

    return data

def generate_coordinates(raw_data, y_title):
    coordinates = [[], []]  # 0 index is all X values, 1 index is all Y values
    date_format = '%Y-%m-%d'
    try:
        test_coordinate = datetime.strptime(raw_data[0]['Date'], date_format)
    except ValueError:
        date_format = '%Y-%m-%d %H:%M:%S'

    for element in raw_data:
        coordinates[0].append(datetime.strptime(element['Date'], date_format))
        coordinates[1].append(float(element['Data'][y_title]))
        # Test print statement
        #print("X: {}\nY: {}".format(element['Date'], element['Data'][y_title]))
    return coordinates

def generate_graph(chart_type, open_line, high_line, low_line, close_line):
    chart = pygal.Bar()
    if chart_type == "Line":
        chart = pygal.Line()

    # date_format('%Y-%m-%d')
    # try:
    #     test_point = datetime.strptime(open_line[0][0], date_format)
    # except ValueError:
    #     date_format = '%Y-%m-%d %H:%M:%S'
    
    chart.title = 'Stock Data for {}: {} to {}'.format(SYMBOL, open_line[0][0], open_line[0][-1])
    chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), open_line[0])
    chart.add('Open', open_line[1])
    chart.add('High', high_line[1])
    chart.add('Low', low_line[1])
    chart.add('Close', close_line[1])
    chart.render_in_browser()

def main():
    chart = select_chart_type()
    time_series = select_time_series()
    ogURL = build_URL(time_series)
    date_range = select_beginning_end_dates()   # List with start date at 0, end date at 1

    raw_data = parse_json(ogURL, date_range, time_series)
    
    open_line = generate_coordinates(raw_data, "1. open")
    high_line = generate_coordinates(raw_data, "2. high")
    low_line = generate_coordinates(raw_data, "3. low")
    close_line = generate_coordinates(raw_data, "4. close")

    generate_graph(chart, open_line, high_line, low_line, close_line)

main()

# Sources:
# - https://www.geeksforgeeks.org/converting-string-yyyy-mm-dd-into-datetime-in-python/
# - https://towardsdatascience.com/json-and-apis-with-python-fba329ef6ef0