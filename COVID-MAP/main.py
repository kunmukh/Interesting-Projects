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

# file path to different dataset
csse_confirmed = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
csse_death = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
csse_recovered = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"


# function that updates the COVID dataset
def updateCOVIDdataset():
    os.chdir("COVID-19")
    os.system("git pull")
    os.chdir("..")


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
def drawMap(latitude, longitide, caseStatus, markerType, date, closeFlag, totalCase):

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
        plt.text(0, 0,
                 'Dataset: 2019 Novel Coronavirus COVID-19 (2019-nCoV)' +
                 ' Data Repository by Johns Hopkins CSSE', color="yellow")
        plt.title(k + caseStatus + " " + date + " People: "+str(totalCase), color='red')


        if closeFlag:
            plt.savefig('img/' + k + "/" + date + '.png', dpi=100)
            plt.close()


# format the date in correct order
def getDate(date):

    format_date = date.replace("/", "_")
    month, date, year = format_date.split("_")

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
    img = cv2.imread(sorted(glob.glob(filedir+'/*.png'))[-1])
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

    # load the dataset
    covid_confirmed = getProcessedData(loadDataset(csse_confirmed))
    covid_death = getProcessedData(loadDataset(csse_death))
    covid_recovered = getProcessedData(loadDataset(csse_recovered))

    # print the dataset
    # print(covid_confirmed)
    # print(covid_death)
    # print(covid_recovered)

    # get the latitude and Longitude
    latCaseConfirmed, longCaseConfirmed = getLatitudeandLongitude(covid_confirmed)

    drawMap(latCaseConfirmed, longCaseConfirmed, " : Case Confirmed", 'ro',
            getDate(str(loadDataset(csse_confirmed).columns.tolist()[-1])), False,
            covid_confirmed.iloc[:, -1].sum())

    # get the data in terms of date
    covid_confirmed_list = getProcessedDataperDate(loadDataset(csse_confirmed))

    # create the images
    for date in covid_confirmed_list:
        # load the dataset
        lat, long = getLatitudeandLongitude(date)
        drawMap(lat, long, " :Case Confirmed", 'ro',
                getDate(str(date.columns.tolist()[-1])), True,
                date.iloc[:, -1].sum())

    makeVideoandGif()

    plt.show()


if __name__ == '__main__':
    main()