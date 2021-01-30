import sys
import math
import random
import statistics
import csv
random.seed(5)
#%matplotlib inline
import matplotlib.pyplot as plt

# Main parameters (excludes parameters to do with generating room sizes distribution)
NUM_STUDENTS=20000  #Number of students at university
MEAN_MOD_PER_STU=4  #Mean number of modules per student
SD_MOD_PER_STU=2    #Standard Deviation of number of modules per student
MIN_MOD_PER_STU=1   #Minimum number of modules per student
MAX_MOD_PER_STU=8  #Maximum number of modules per student
NUM_MODULES=340     #Total number of modules to be timetabled per day
NUM_1HRMODULES=300  #Total number of 1 hour modules to be timetabled per day
NUM_2HRMODULES=30   #Total number of 2 hour modules to be timetabled per day
NUM_4HRMODULES=10   #Total number of 4 hour modules to be timetabled per day
NUM_DEPTS=50        #Number of Departments (each having unique 2 character module code)
NUM_ROOMS=100       #Number of rooms for timetabling (Default, overwritten by actual Room List)
ROOMHOURS_PER_DAY=9 #Number of timetabled hours per room per day

# Read in rooms from room list CSV
rooms={}
filename=input("Enter filename for file containing room sizes [Room List.csv]: ")
filename=filename or 'Room List.csv'
with open(filename) as csv_file:
    csv_reader=csv.reader(csv_file,delimiter=',')
    line_count=0
    for row in csv_reader:
        if line_count==0:
            print(f'{row[0]:20}',f'{row[1]:20}',f'{row[2]:10}')
        else:
            print(f'{row[0]:20}',f'{row[1]:20}',f'{row[2]:10}')
            roomno=row[0]
            bldg=row[1]
            if row[2]=="":
                cap=0
            else:
                cap=int(row[2])
            rooms[roomno]={'building':bldg,'size':cap,'free':ROOMHOURS_PER_DAY,'bkgs':['','','','','','','','','']}
        line_count+=1
    NUMROOMS=line_count-1
    print("Number of rooms is: ",NUMROOMS)

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

plt.figure(figsize=(10,8))
plt.hist(roomsizes,bins=50)
plt.title("Distribution of Room Sizes")
plt.ylabel("Frequency")
plt.xlabel("Room Size");
plt.show()

# Function to generate a random individual student number of the form AB123456
def genstudent():
    studentno=chr(ord('@')+random.randint(1,26))+chr(ord('@')+random.randint(1,26))+ \
    str(random.randint(100000,999999))
    return studentno            

# Function to generate a random departmental module code of the form AB
def genmodhead():
    modhead=chr(ord('@')+random.randint(1,26))+chr(ord('@')+random.randint(1,26))    
    return modhead            

# Generate the list of unique random student numbers
print("Generating Student IDs ...")
students=[]
for i in range(NUM_STUDENTS):
    while True:
        stu=genstudent()
        if stu not in students:
            students.append(stu)
            break
print(NUM_STUDENTS," student IDs generated")

# Generate the list of unique 2 Character module headers of the form AB
modheads=[]
for i in range(NUM_DEPTS):
    while True:
        modh=genmodhead()
        if modh not in modheads:
            modheads.append(modh)
            break

# Generate the list of unique module names of the form AB(1,2,3,4,M)XY(16-20)
print("Generating Modules ...")
modules=[]
for day in range(5):
    for i in range(NUM_MODULES):
        while True:
            modcode=modheads[random.randint(0,NUM_DEPTS-1)]+['1','2','3','4','M'][random.randint(0,4)]+\
            chr(ord('@')+random.randint(1,26))+ chr(ord('@')+random.randint(1,26))+str(random.randint(16,20))
            if modcode not in modules:
                modules.append(modcode)
                break
    print(NUM_MODULES," unique module codes generated for day:",day)
# Generate the module to student mapping
print("Generating the modules per student...")
# Initialise the student to module dictionary
stu_mods={}
# Initialise the module to student dictionary, then make each module a random day of the week
mod_stus={}
# and allocate the duration to 1 hour 2 hour and 4 hour modules
for i in range(len(modules)):
    mod_stus[modules[i]]={'dow':0,'hours':0,'nums':0,'students':[]}
    #mod_stus[modules[i]]['dow']=random.randrange(5)
for day in range(5):
    for i in range(NUM_1HRMODULES):
        mod_stus[modules[i+day*NUM_MODULES]]['hours']=1
    for i in range(NUM_1HRMODULES+day*NUM_MODULES,(NUM_1HRMODULES+NUM_2HRMODULES)+day*NUM_MODULES):
        mod_stus[modules[i]]['hours']=2
    for i in range((NUM_1HRMODULES+NUM_2HRMODULES)+day*NUM_MODULES,(NUM_1HRMODULES+NUM_2HRMODULES+NUM_4HRMODULES)+day*NUM_MODULES):
        mod_stus[modules[i]]['hours']=4
    for i in range(day*NUM_MODULES,(day+1)*NUM_MODULES):
        mod_stus[modules[i]]['dow']=day

    # Choose random modules for each student according to normal distribution and update mapping dictionaries
for i in range(NUM_STUDENTS):
    chosen_mods=[]
    nmods=min(max(MIN_MOD_PER_STU,int(random.normalvariate(MEAN_MOD_PER_STU,SD_MOD_PER_STU))),MAX_MOD_PER_STU)
    for j in range(nmods):
        while True:
            curmod=modules[random.randrange(len(modules))]
            if curmod not in chosen_mods:
                chosen_mods.append(curmod)
                if curmod not in mod_stus:
                    mod_stus[curmod]['students']=[students[i]]
                    mod_stus[curmod]['nums']=1
                else:
                    mod_stus[curmod]['students'].append(students[i])
                    mod_stus[curmod]['nums']+=1
                break
    stu_mods[students[i]]=chosen_mods
while True:
    ip=input("Enter Day of Week to Analyse (0-4)?")
    try:
        dow = int(ip)
    except ValueError:
        print('This needs to be a valid integer')
        continue
    if (dow>=0)&(dow<=4):
        print ("Day of Week is:",dow)
        break
    else:
        print("The Day of Week is out of range")
# Get modules to schedule corresponding to day of week selected
mod_to_sched=[]
for mods in mod_stus:
    if mod_stus[mods]['dow']==dow:
        getmodlist=[mods,mod_stus[mods]['hours'],mod_stus[mods]['nums']]
        mod_to_sched.append(getmodlist)
print(len(mod_to_sched),"modules selected for day: ",dow)
count=0
for i in range(len(mod_to_sched)):
    count+=1
    vbutil=0.0
    vbscore=0.0
    vbsize=0
    fflg=False
    for mods,hrs,nums in mod_to_sched:
        for room in rooms.keys():
            # First check room is viable from a capacity and hours perspective
            if (rooms[room]['size']>=nums)&(rooms[room]['free']>=hrs):
                util=nums/rooms[room]['size']
                score=util+hrs*2
                if (score>vbscore)|((score==vbscore)&(nums>vbsize)):
                    fflg=True
                    vbscore=score
                    vbutil=util
                    vbroom=room
                    vbmod=mods
                    vbnums=nums
                    vbhrs=hrs
    if fflg:
        print(f"{count:3d}",": Module:",vbmod,"numbers:",vbnums,"hours:",vbhrs,"best room:",f"{vbroom:15}","size:",f"{rooms[vbroom]['size']:3d}","utilisation:",f"{vbutil:6.1%}")
        rooms[vbroom]['free']-=vbhrs
        for k in range(ROOMHOURS_PER_DAY):
            if rooms[vbroom]['bkgs'][k]=="":
                break
        for l in range(vbhrs):
            rooms[vbroom]['bkgs'][k+l]=vbmod
        mod_to_sched.remove([vbmod,vbhrs,vbnums])   
    else:
        print("Module:",mods,"not allocated, size:",nums,"hours:",hrs)
        mod_to_sched.remove([mods,hrs,nums])          
gtothrs=0.0
gutilhrs=0.0
gtotphrs=0.0
gutilphrs=0.0
print("\nRoom Status")
for room in rooms:
    tothrs=ROOMHOURS_PER_DAY
    gtothrs+=ROOMHOURS_PER_DAY
    totphrs=ROOMHOURS_PER_DAY*rooms[room]['size']
    gtotphrs+=ROOMHOURS_PER_DAY*rooms[room]['size']
    utilhrs=ROOMHOURS_PER_DAY-rooms[room]['free']
    gutilhrs+=ROOMHOURS_PER_DAY-rooms[room]['free']
    utilphrs=0
    for k in range(ROOMHOURS_PER_DAY):
        if rooms[room]['bkgs'][k]!="":
            utilphrs+=mod_stus[rooms[room]['bkgs'][k]]['nums']
            gutilphrs+=mod_stus[rooms[room]['bkgs'][k]]['nums']
    if rooms[room]['size']>0:
        print(f"{room:15}","size:",f"{rooms[room]['size']:3d}","total hours:",tothrs,"util-hours:",utilhrs,"ratio",f"{utilhrs/tothrs:6.1%}",\
          "person-hours:",f"{totphrs:4d}","util-phours:",f"{utilphrs:4d}","ratio:",f"{utilphrs/totphrs:6.1%}")
print("total hours",gtothrs,"util hours",gutilhrs,"ratio",f"{gutilhrs/gtothrs:5.1%}","person-hours",gtotphrs,"util-phours",gutilphrs, \
      "ratio",f"{gutilphrs/gtotphrs:6.1%}")
#sys.exit("rooms allocated")

# Need to add:
# - More representative module size distribution
# - Lecturer per module
# - Lecturer schedule and constraints
# - Unplaced module list
# - Actions to perform when module in unplaced
# - Room equipment facilities and constraints
# - Optimisation of schedule once a feasible one has been developed. 

