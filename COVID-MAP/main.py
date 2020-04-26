# Kunal Mukherjee
# COVID MAP
# 3/13/20 - Friday the 13th
# Dataset: 2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE
# https://github.com/CSSEGISandData/COVID-19


# import libraries
import os
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import cv2
import glob
from datetime import datetime, timedelta


# file path to different dataset
csse_confirmed = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
csse_death = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
csse_recovered = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
csse_daily = "COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"


# function that updates the COVID dataset
def updateCOVIDdataset():
    os.chdir("COVID-19")
    os.system("git pull")
    os.chdir("..")


# function to push update
def pushCommit():
    os.system("git status")
    os.system("git add img/* Video/* gif/* main.py")
    os.system("git commit -m \"img, Video, gif updated with current data\"")
    os.system("git push")


# load the dataset of the COVID
# from the file path
def loadDataset(filename):
    data = pd.read_csv(filename)
    return data


# get the 'Province/State', 'Country/Region', 'Lat', 'Long', 'Total
def getProcessedData(data):
    new_data = data[['Province/State', 'Country/Region', 'Lat', 'Long']]
    new_data['Total'] = data.iloc[:, -1]

    # remove the lat and long where no case detected
    new_data = new_data[new_data['Total'] != 0]

    return new_data


# get list of 'Province/State', 'Country/Region', 'Lat', 'Long', 'Total, + 'Date'
def getProcessedDataperDate(data):
    # get the number of dates
    date_cols = data.columns.tolist()[4:]

    # create a dateframe with location info
    new_data = data[['Province/State', 'Country/Region', 'Lat', 'Long']]

    # list of dataframe
    list_data_date = []

    # merge location info and case info for each date
    for col in date_cols:
        mod_data = new_data.copy()
        mod_data[col] = data[col]

        # remove the lat and long where no case detected
        mod_data = mod_data[mod_data[col] != 0]

        list_data_date.append(mod_data)

    # return the list
    return list_data_date


# return the latitude and longitude from the dataframe
def getLatitudeandLongitude(data):
    lat = data['Lat']
    long = data['Long']

    return lat, long


# a dictionary that contains Latitude/Longitude lower/upper right corner
def getDictPlaceLatLongCol():
    Lat_long_DB = dict({'World': [-90, 90, -180, 180, '#fff30a'],
                        'Texas': [25, 38, -110, -90, '#44ff00'],
                        'US': [20, 50, -130, -60, '#00ffea'],
                        'India': [6, 40, 68, 100, '#ff9500']})

    return Lat_long_DB


def drawMapbackground(llcrnrlat_, urcrnrlat_, llcrnrlon_, urcrnrlon_):

    mapB = Basemap(projection='mill',
                llcrnrlat=llcrnrlat_, # Latitude lower right corner
                urcrnrlat=urcrnrlat_, # Latitude upper right corner
                llcrnrlon=llcrnrlon_, # Longitude lower right corner
                urcrnrlon=urcrnrlon_, # Longitude upper right corner
                resolution='c') # Crude resolution

    mapB.drawcoastlines()
    mapB.drawcountries()
    mapB.drawstates()
    '''mapB.drawmapboundary(fill_color='#FFFFFF')'''

    mapB.bluemarble()


    return mapB


# draw the map based on the latitude and longitude provided
def drawMap(latitude, longitide, markerType, date, closeFlag,
            _totalCaseConfim, _totalCaseDeath, _totalCaseRecover):

    for k in getDictPlaceLatLongCol().keys():
        fig = plt.figure(figsize=(10, 10), dpi=100)

        #get the latitude
        lat_long = getDictPlaceLatLongCol()[k]

        # Draw the map
        m = drawMapbackground(lat_long[0], lat_long[1], lat_long[2], lat_long[3])
        # m.fillcontinents(color=lat_long[4], lake_color='#FFFFFF')

        # Draw the data points
        for lo, la in zip(longitide, latitude):
            lo, la = m(lo, la)
            m.plot(lo, la, markerType)

        # Add details

        totalCaseConfim = _totalCaseConfim.loc[(_totalCaseConfim['Lat'] >= lat_long[0]) &
                                               (_totalCaseConfim['Lat'] <= lat_long[1]) &
                                               (_totalCaseConfim['Long'] >= lat_long[2]) &
                                               (_totalCaseConfim['Long'] <= lat_long[3])].sum()[-1]

        totalCaseDeath = _totalCaseDeath.loc[(_totalCaseDeath['Lat'] >= lat_long[0]) &
                                               (_totalCaseDeath['Lat'] <= lat_long[1]) &
                                               (_totalCaseDeath['Long'] >= lat_long[2]) &
                                               (_totalCaseDeath['Long'] <= lat_long[3])].sum()[-1]

        totalCaseRecover = _totalCaseRecover.loc[(_totalCaseRecover['Lat'] >= lat_long[0]) &
                                                (_totalCaseRecover['Lat'] <= lat_long[1]) &
                                                (_totalCaseRecover['Long'] >= lat_long[2]) &
                                                (_totalCaseRecover['Long'] <= lat_long[3])].sum()[-1]

        plt.text(0, 0,
                 'Dataset: 2019 Novel Coronavirus COVID-19 (2019-nCoV)' +
                 ' Data Repository by Johns Hopkins CSSE', color="yellow")
        plt.title(k + " DATE: " + date + "| Confirm: " + str(totalCaseConfim) +
                  "| Death: " + str(totalCaseDeath) + "| Recovered: " + str(totalCaseRecover),
                  color='red')
        plt.xlabel('Kunal Mukherjee| https://github.com/kunmukh', color='blue')



        if closeFlag:
            plt.savefig('img/' + k + "/" + date + '.png', dpi=100)
            plt.close()


# draw the latest map of today
def drawTodayMap():
    # Draw the latest map
    # load the data set
    today = datetime.today() - timedelta(days=1)
    data = loadDataset(csse_daily + today.strftime('%m-%d-%Y') + ".csv")
    # change column name
    data = data.rename(columns={'Long_': 'Long'})

    # get the required data
    data_confirmed = data.loc[data['Confirmed'] != 0]
    lat = data_confirmed['Lat']
    long = data_confirmed['Long']
    dateConfirm = data_confirmed[['Lat', 'Long', 'Confirmed']]
    dateDeath = data_confirmed[['Lat', 'Long', 'Deaths']]
    dateRecover = data_confirmed[['Lat', 'Long', 'Recovered']]

    # update the map
    drawMap(lat, long, 'r.',
            getDate(data['Last_Update'].iloc[1][:10]), False,
            dateConfirm, dateDeath, dateRecover)


# draw the maps from the date given till today
def drawMapFromDate(startDateDaily, stopDateDaily):
    # CSSE Datset changed
    '''# get the data in terms of date
    covid_confirmed_list = getProcessedDataperDate(loadDataset(csse_confirmed))
    covid_death_list = getProcessedDataperDate(loadDataset(csse_death))
    covid_recovered_list = getProcessedDataperDate(loadDataset(csse_recovered))

    # create the images from the time series
    for dateConfirm, dateDeath, dateRecover in zip(covid_confirmed_list,
                                                   covid_death_list,
                                                   covid_recovered_list):
        # load the dataset
        lat, long = getLatitudeandLongitude(dateConfirm)
        drawMap(lat, long, 'ro',
                getDate(str(dateConfirm.columns.tolist()[-1])), True,
                dateConfirm, dateDeath, dateRecover)'''


    while stopDateDaily.strftime('%m-%d-%Y') != startDateDaily.strftime('%m-%d-%Y'):
        # load the data set
        data = loadDataset(csse_daily + startDateDaily.strftime('%m-%d-%Y') + ".csv")
        # change column name
        data = data.rename(columns={'Long_': 'Long'})

        # print(data)

        # get the required data
        data_confirmed = data.loc[data['Confirmed'] != 0]
        lat = data_confirmed['Lat']
        long = data_confirmed['Long']
        dateConfirm = data_confirmed[['Lat', 'Long', 'Confirmed']]
        dateDeath = data_confirmed[['Lat', 'Long', 'Deaths']]
        dateRecover = data_confirmed[['Lat', 'Long', 'Recovered']]

        # update the map from daily update
        drawMap(lat, long, 'r.',
                getDate(data['Last_Update'].iloc[1][:10]), True,
                dateConfirm, dateDeath, dateRecover)

        # update date
        startDateDaily += timedelta(days=1)


# plot the latest map
def showLatestMap():
    # Draw the latest map
    # load the data set
    today = datetime.today() - timedelta(days=1)
    data = loadDataset(csse_daily + today.strftime('%m-%d-%Y') + ".csv")
    # change column name
    data = data.rename(columns={'Long_': 'Long'})

    # get the required data
    data_confirmed = data.loc[data['Confirmed'] != 0]
    lat = data_confirmed['Lat']
    long = data_confirmed['Long']
    dateConfirm = data_confirmed[['Lat', 'Long', 'Confirmed']]
    dateDeath = data_confirmed[['Lat', 'Long', 'Deaths']]
    dateRecover = data_confirmed[['Lat', 'Long', 'Recovered']]

    # update the map
    drawMap(lat, long, 'r.',
            getDate(data['Last_Update'].iloc[1][:10]), False,
            dateConfirm, dateDeath, dateRecover)



# format the date in correct order
def getDate(date):

    format_date = date.replace("/", "_").replace("-", "_")
    if "-" not in date:
        month, date, year = format_date.split("_")
    else:
        year, month, date = format_date.split("_")

    if len(month) < 2:
        month = '0' + month
    if len(date) < 2:
        date = '0' + date
    if len(year) < 2:
        year = '0' + year

    return month + "_" + date + "_" + year


# make the video of the pic
def makeVideo(filedir, outfile):

    img_array = []
    size = [0, 0]

    # HACK for README
    img = cv2.imread(sorted(glob.glob(filedir+'/*.png'))[-2])
    cv2.imwrite(filedir+'/'+outfile+'Latest.png', img)

    # open the file and read the images
    for filename in sorted(glob.glob(filedir+'/*.png')):
        img = cv2.imread(filename)

        height, width, layers = img.shape
        size = (width, height)

        img_array.append(img)

    # create the video output
    out = cv2.VideoWriter('Video/'+ outfile +'.avi', cv2.VideoWriter_fourcc(*'DIVX'), 2, size)

    # Appending the images to the video one by one
    for i in range(len(img_array)):
        out.write(img_array[i])

    # Deallocating memories taken for window creation
    cv2.destroyAllWindows()

    out.release()  # releasing the video generated


# make the video from the images and gif
def makeVideoandGif():

    # make the videos
    makeVideo('img/World', 'World')
    makeVideo('img/US', 'US')
    makeVideo('img/India', 'India')
    makeVideo('img/Texas', 'Texas')

    # convert to Gif
    os.system("ffmpeg -i Video/World.avi gif/World.gif -y")
    os.system("ffmpeg -i Video/Texas.avi gif/Texas.gif -y")
    os.system("ffmpeg -i Video/US.avi gif/US.gif -y")
    os.system("ffmpeg -i Video/India.avi gif/India.gif -y")


def main():
    # update the dataset
    updateCOVIDdataset()

    # COVID Dataset changed the data location and format
    # starting date changed to 3/23/20-> 4/15/20->4/25/20
    startDateDaily = datetime(2020, 4, 15)
    stopDateDaily = datetime.today() + timedelta(days=2)
    drawMapFromDate(startDateDaily, stopDateDaily)

    # uncomment if you want to create and save today's date
    # drawTodayMap()

    # show the latest map
    showLatestMap()

    # make the gif and the map
    makeVideoandGif()

    # push the latest img, video, gif with current data
    pushCommit()

    plt.show()


if __name__ == '__main__':
    main()