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

distTolerance = 2 #pixels between front HPs (residual burning)


os.chdir('/Users/kirsten/Documents/data/MODIS/FRE_TEST_DATA')
filList = os.listdir('.')

##GET ALL FRP CSVs
##FOR EACH DAY, GET ALL OVERPASSES
##GET DISTANCES BETWEEN NEW DETECTIONS AND PREVIOUS ONES FROM THE SAME YEAR
##ASSIGN CONT/FRONT ACCORDINGLY
##OUTPUT TO A NEW CSV FILE


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
    jDayAreas = np.asarray([])
    jDayFRPs = np.asarray([])
    jDayFRPsareas = np.asarray([])
    jDayHrs = np.asarray([])
    jDayMints = np.asarray([])
    jDayJdays = np.asarray([])
    jDayYrs = np.asarray([])
    jDaySats = np.asarray([])
    jDayFils = np.asarray([])
    #FRPx,FRPy,FRPxProj,FRPyProj,Area,FRP,FrpArea,hrs,mints,js,yrs,filNams
    
    for oP in ovrPassFilList:
        oPdata = genfromtxt(oP, delimiter=',')
        if np.size(oPdata)>0:
            oPxs = oPdata[:,0]
            jDayXs = np.append(jDayXs,oPxs)
            oPys = oPdata[:,1]
            jDayYs = np.append(jDayYs,oPys)
            oPprojXs = oPdata[:,2]
            jDayProjXs = np.append(jDayProjXs,oPprojXs)
            oPprojYs = oPdata[:,3]
            jDayProjYs = np.append(jDayProjYs,oPprojYs)
            oPareas = oPdata[:,4]
            jDayAreas = np.append(jDayAreas,oPareas)
            opFRPs = oPdata[:,5]
            jDayFRPs = np.append(jDayFRPs,opFRPs)
            opFRPareas = oPdata[:,6]
            jDayFRPsareas = np.append(jDayFRPsareas,opFRPareas)
            opHrs = oPdata[:,7]
            jDayHrs = np.append(jDayHrs,opHrs)
            opMints = oPdata[:,8]
            jDayMints = np.append(jDayMints,opMints)
            opJdays = oPdata[:,9]
            jDayJdays = np.append(jDayJdays,opJdays)
            opYrs = oPdata[:,10]
            jDayYrs = np.append(jDayYrs,opYrs)
            
    opXY = np.asarray((jDayXs,jDayYs))
    if jDay == minJday:
        prevDetects = opXY
    else:
        dists = do_kdtree(prevDetects,opXY)
        filName = np.array(np.repeat(oP,len(dists)))
        exportCSV = np.column_stack([jDayXs,jDayYs,jDayProjXs,jDayProjYs,jDayAreas,jDayFRPs,jDayFRPsareas,jDayHrs,jDayMints,jDayJdays,jDayYrs,filName,dists])
        np.savetxt(str(jDay)+'contFront_XY_proj_crds.csv', exportCSV, delimiter=",",fmt = '%s')
        
##ADD HEADER TO FILES
filList = os.listdir('.')
hdr = 'X,Y,AEA_AK_X,AEA_AK_Y,Area,FRP,FrpArea,hr,min,julian,year,fileName,dist_to_closest\n'
for filnam in filList:
    if filnam[-8:] == 'crds.csv':
        newfilnam = filnam.replace('.csv','_hdr.csv')
        newfil = open(newfilnam,'w')
        newfil.write(hdr)
        fil = open(filnam,'r')
        content = fil.read()
        newfil.write(content)
        newfil.close()

    

        
            
    
    
        
        
        
