import sys
import csv
import math
import random
import statistics
random.seed(5)
#%matplotlib inline
import matplotlib.pyplot as plt

# Module to generate rooms according to specific random distributions
# Can choose Exponential, Gamma, Lognormal, Normal or Uniform
# To run:
#           python genrooms.py
#
NUM_BUILDINGS=15    #Total number of buildings
NUM_ROOMS=100       #Number of rooms for timetabling
MEAN_ROOM_SIZE=49   #Mean room size
SD_ROOM_SIZE=55     #Standard Deviation of room size
MIN_ROOM_SIZE=6     #Minimum room size
MAX_ROOM_SIZE=400   #Maximum room size
ROOMHOURS_PER_DAY=9 #Number of timetabled hours per room per day

# Write out room sizes
def writerooms(title):
    with open(title+'.csv',mode='w') as roomout_file:
        room_writer=csv.writer(roomout_file,delimiter=',')
        room_writer.writerow(['Room              ',' Building           ','Capacity           '])
        for roomno in rooms:
            room_writer.writerow([roomno,rooms[roomno]['building'],rooms[roomno]['size']])

rooms={}
for i in range(NUM_ROOMS):
    # Generate random room numbers of the form ABC123
    while True:
        roomno=chr(ord('@')+random.randint(1,26))+chr(ord('@')+random.randint(1,26))+ \
        chr(ord('@')+random.randint(1,26))+str(random.randint(100,999))
        if roomno not in rooms:
            rooms[roomno]={'building':'BUILDING '+str(random.randint(1,NUM_BUILDINGS)), \
                           'size':0,'free':ROOMHOURS_PER_DAY,'bkgs':['','','','','','','','','']}
            break
while True:
    dist=input("Enter Distribution for Room Sizes (E)xponential, (G)amma, (L)ognormal, (N)ormal or (U)niform?")
    dist=dist.upper()
    # Uniform Distribution
    if (dist=="U"):
        disttype="Uniform"
        for roomno in rooms:
            rooms[roomno]['size']=random.randint(MIN_ROOM_SIZE,2*MEAN_ROOM_SIZE-MIN_ROOM_SIZE)
        break
    # Normal Distribution    
    elif (dist=="N"):
        disttype="Normal"
        for roomno in rooms:
            rooms[roomno]['size']=min(max(MIN_ROOM_SIZE,int(random.normalvariate(MEAN_ROOM_SIZE,SD_ROOM_SIZE))),MAX_ROOM_SIZE)
        break
    # LogNormal Distribution    
    elif (dist=="L"):
        disttype="LogNormal"
        mu=math.log(MEAN_ROOM_SIZE**2/math.sqrt(MEAN_ROOM_SIZE**2+SD_ROOM_SIZE**2))
        sigma=math.sqrt(math.log(1+((SD_ROOM_SIZE**2)/(MEAN_ROOM_SIZE**2))))
        for roomno in rooms:
            rooms[roomno]['size']=min(max(MIN_ROOM_SIZE,int(random.lognormvariate(mu,sigma))),MAX_ROOM_SIZE)
        break    
    # Gamma Distribution    
    elif (dist=="G"):
        disttype="Gamma"
        k=(MEAN_ROOM_SIZE/SD_ROOM_SIZE)**2
        theta=(SD_ROOM_SIZE**2)/MEAN_ROOM_SIZE
        for roomno in rooms:
            rooms[roomno]['size']=min(max(MIN_ROOM_SIZE,int(random.gammavariate(k,theta))),MAX_ROOM_SIZE)
        break
    # Exponential Distribution
    elif (dist=="E"):
        disttype="Exponential"
        for roomno in rooms:
            rooms[roomno]['size']=min(max(MIN_ROOM_SIZE,int(random.expovariate(1/MEAN_ROOM_SIZE))),MAX_ROOM_SIZE)
        break
    else:
        print("Incorrect Input")
print(disttype+" Room Size Distribution Selected")
writerooms(disttype)
roomsizes=[]
for x in rooms.values():
    roomsizes.append(x['size'])
print()
print("Total Capacity: ",sum(roomsizes)," Students")
print("Total Capacity: ",sum(x['size']*x['free'] for x in rooms.values())," Room Hours")
print("Max Room Size: ",max(roomsizes))
print("Min Room Size: ",min(roomsizes))
print("Mean Room Size: ",int(sum(roomsizes)/len(rooms)))
print("Median Room Size: ",int(statistics.median(roomsizes)))
print("Standard Deviation of Room Size: ",int(statistics.stdev(roomsizes)))
print()
# Plot results
plt.figure(figsize=(10,8))
plt.hist(roomsizes,bins=50)
plt.title("Plot of Room Sizes Generated, "+disttype+" Distribution Selected")
plt.ylabel("Frequency")
plt.xlabel("Room Size");
plt.show()
sys.exit("Rooms generated")

