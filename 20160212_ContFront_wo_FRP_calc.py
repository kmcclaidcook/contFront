import scipy.spatial
import numpy as np
from numpy import genfromtxt
import datetime
import os

def do_kdtree(prevDetects,newXY):
    old_x_array = prevDetects[0]
    old_y_array = prevDetects[1]   
    YXprev = np.dstack([old_y_array.ravel(),old_x_array.ravel()])[0]
    new_x_array = newXY[0]
    new_y_array = newXY[1]
    YXnew = np.dstack([new_y_array.ravel(),new_x_array.ravel()])[0]
    tree = scipy.spatial.cKDTree(YXprev)
    dist = tree.query(YXnew)[0]
    return dist


#AK BOREAL EXTENT
##minX = -511738.931
##minY = 1176158.734
##maxX = 672884.463
##maxY = 2117721.949
distTolerance = 2 #pixels between front HPs (residual burning)

##inProj = Proj(init='epsg:4326') #GEOGRAPHIC WGS84
##outProj = Proj(init='esri:102006') #AK ALBERS EQUAL AREA CONIC
##nProjRows = np.int_(np.rint((maxY-minY)/1000))
##nProjCols = np.int_(np.rint((maxX-minX)/1000))


os.chdir('/Users/kirsten/Documents/data/MODIS/FRE_TEST_DATA')
filList = os.listdir('.')

##GET ALL FRP CSVs
##FOR EACH DAY, GET ALL OVERPASSES
##GET DISTANCES BETWEEN NEW DETECTIONS AND PREVIOUS ONES FROM THE SAME YEAR
##ASSIGN CONT/FRONT ACCORDINGLY
##OUTPUT TO A NEW CSV FILE

#newCSV = #...
jDayList = []
csvList = []
minJday = 365

for fil in filList:
    if fil[-6:] == 'XY.csv':
        csvList.append(fil)
        datTim = fil.split('.')[1].replace('A','') + fil.split('.')[2]
        dateTime = datetime.datetime.strptime(datTim, "%Y%j%H%M")
        julianDay = dateTime.timetuple().tm_yday
        if julianDay<minJday:
            minJday = julianDay
        jDayList.append(julianDay)

jDayList = sorted(set(jDayList))

for jDay in jDayList:
    ovrPassFilList = []
    for fil in csvList:
        filJday = int(fil.split('.')[1][5:8])
        if filJday == jDay:
            ovrPassFilList.append(fil)
    jDayXs = np.asarray([])
    jDayYs = np.asarray([])
    jDayProjXs = np.asarray([])
    jDayProjYs = np.asarray([])
    jDayFRPs = np.asarray([])
    jDayHrs = np.asarray([])
    jDayMints = np.asarray([])
    jDayJdays = np.asarray([])
    jDayYrs = np.asarray([])
    jDaySats = np.asarray([])
    jDayConfs = np.asarray([])
    jDayData = np.asarray([])
    #...
    for oP in ovrPassFilList:
        oPdata = genfromtxt(oP, delimiter=',')
        if np.size(oPdata)>0:
            oPxs = oPdata[:,2]
            jDayXs = np.append(jDayXs,oPxs)
            oPys = oPdata[:,3]
            jDayYs = np.append(jDayYs,oPys)
            oPprojXs = oPdata[:,2]
            jDayProjXs = np.append(jDayProjXs,oPprojXs)
            oPprojYs = oPdata[:,3]
            jDayProjYs = np.append(jDayProjYs,oPprojYs)
            opFRPs = oPdata[:,5]
            jDayFRPs = np.append(jDayFRPs,opFRPs)
            
        #    opFRPs = ...
            #ALL OTHER HP INFO...
    opXY = np.asarray((jDayXs,jDayYs))
    if jDay == minJday:
        prevDetects = opXY
    else:
        dists = do_kdtree(prevDetects,opXY)
        exportCSV = np.column_stack([jDayXs,jDayYs,dists,jDayProjXs,jDayProjYs,jDayFRPs])
        np.savetxt(str(jDay)+'contFront_XY_proj_crds.csv', exportCSV, delimiter=",")
        
        #    opNewData = ###COMBINE IT ALL TOGETHER
        ##ADD TO jDayData

     #THEN WRITE ALL jDayData TO newCSV

        
            
    
    
        
        
        
