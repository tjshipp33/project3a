'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal

timeSeriesTypes = ["INTRADAY", "DAILY", "WEEKLY", "MONTHLY"]
timeSeriesURL = ['Time Series (60min)', 'Time Series (Daily)', 'Weekly Time Series', 'Monthly Time Series']
apiKey = "33451WDSYYNTOXAH"

chartLists = {
    'chartOpen': [],
    'chartHigh': [],
    'chartLow': [],
    'chartClose': [],
    'chartDates': [],
}

#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def callAPI(symbol, timeSeries):
    interval = '&interval=60min' if timeSeries == "INTRADAY" else ''
    apiURL = "https://www.alphavantage.co/query?function=" + "TIME_SERIES_" + timeSeries + "&symbol=" + symbol + interval + "&outputsize=full&apikey=" + apiKey
    print(apiURL)
    r = requests.get(apiURL)
    data = r.json()
    return data

def fillLists(data, dates, timeSeriesProp):
    try:
        for entry in data[timeSeriesProp]:
            entryDate = datetime.datetime(int(entry[0:4]), int(entry[5:7]), int(entry[8:10]))
            if(entryDate >= dates[0] and entryDate <= dates[1]):
                entryObject = data[timeSeriesProp][entry]
                chartLists['chartOpen'].append(float(entryObject["1. open"]))
                chartLists['chartHigh'].append(float(entryObject["2. high"]))
                chartLists['chartLow'].append(float(entryObject["3. low"]))
                chartLists['chartClose'].append(float(entryObject["4. close"]))
                chartLists['chartDates'].append(entry)
    except KeyError:
        print("No data for the stock was found.")
        exit()

def reverseLists():
    chartLists['chartOpen'].reverse()
    chartLists['chartHigh'].reverse()
    chartLists['chartLow'].reverse()
    chartLists['chartClose'].reverse()
    chartLists['chartDates'].reverse()

def emptyLists():
    chartLists['chartOpen'].clear()
    chartLists['chartHigh'].clear()
    chartLists['chartLow'].clear()
    chartLists['chartClose'].clear()
    chartLists['chartDates'].clear()

def renderChart(symbol, dates, chartType):
    chart = pygal.Line(x_label_rotation=65) if chartType ==1 else pygal.Bar(x_label_rotation=65)
    chart.title = 'Stock Data for ' + symbol + ": " + str(dates[0])[0:10] + " to " +  str(dates[1])[0:10]
    chart.x_labels = chartLists['chartDates']
    chart.add('Open', chartLists['chartOpen'])
    chart.add('High',  chartLists['chartHigh'])
    chart.add('Low',      chartLists['chartLow'])
    chart.add('Close',  chartLists['chartClose'])
    if(len(chartLists['chartClose']) == 0):
        print("No data was received for your inputs!")
        return
    chart.render_in_browser()