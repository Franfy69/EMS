from cmath import inf
from fileinput import close
from pickletools import float8
import math
import numpy as np
from geneticalgorithm import geneticalgorithm as ga
import csv



def info(): # this function outputs all informaciokn colected by the input file

    print("\n---------------------------------------------------------------------------------------------")
    print("the car has this features: \n mass (car and battery):", car["Mass"]+ Battery["battery mass"],"\t acceleration power:", car["Power train"],"powertrain efficiency: 0.95\n",  "\n drag coefficient:",car["Drag coefficient"], '\t rolling friction', car['rolling friction'], '\t frontal area', car['frontal area'], '\n\n regenerative breaking' , car['regenerative breaking'], '\t Regenerative breaking MAX power (kW)', car['Regenerative breaking MAX power (kW)'])
    print("\n battery energy(KWH)", Battery["battery energy"],"\t battery power (KW)", Battery["battery power"],"\t battery efficiency", 0.95)
    print("\n light", services["luz"],"\t cooling system", services["cooling"],"\t control module", services["AI"])
    print("\n PV area", PV["pv area"], "\t PV efficiency", PV["PV eficiency"])
    print("\n---------------------------------------------------------------------------------------------")
    print("the track has this sections with this features:")

    for i in range (len(tracklen)):
        print("section",i,"\t lengh:", tracklen[i],"\t maximum speed:", "{:.1f}".format(trackmaxspd1[i]), "\t slope:", trackO[i])

    print("\n---------------------------------------------------------------------------------------------")
    print("\n the car has this fuel info:","\n Primary to Final Efficency Electricity", fuel["Primary to Final Efficency Electricity"],"grid CO2 emissions", fuel ["CO2 emissions"])

    return


def raceenergy( ivel, j): #this fuction will return the energy consumed by engine, final velocity and time took in a single section

    p=1.225
    g=9.8

    deltav = trackmaxspd[j] - ivel

    deltav2 = Fb= Fa = i= Eb =  0

    t = (tracklen[j] * 2)/ (ivel + trackmaxspd[j])

    velmed = (ivel + trackmaxspd[j])/2

    if (j<len(trackO)-1):
        if (trackmaxspd[j+1]<trackmaxspd[j]):
            t = (tracklen[j] * 2)/ (ivel + trackmaxspd[j+1])
            velmed = (ivel + trackmaxspd[j+1])/2

    Fw = 0.5 * p * car["frontal area"] * car["Drag coefficient"] * velmed * velmed  #aerodinamica

    Fr = g * (car["Mass"]+Battery["battery mass"]) * car["rolling friction"] * math.cos(math.radians(trackO[j]))# atrito 

    Fi = (car["Mass"]+Battery["battery mass"]) * g * math.sin(math.radians(trackO[j]))  # força da inclinação

    if(deltav > 0): Fa = deltav * (car["Mass"]+Battery["battery mass"]) / t # aceleração 


    Ft = Fw + Fr + Fa + Fi + Fb # força total


    while(Ft * velmed >=car["Power train"]*0.95):
        i+=1
        aux = (car["Power train"]*0.95)/(Ft * velmed)
        deltav *= (aux * (1-i/50))
        Fa = deltav * (car["Mass"]+Battery["battery mass"]) / t
        velmed = (ivel +ivel + deltav)/2
        Fw = 0.5 * p * car["frontal area"] * car["Drag coefficient"] * velmed * velmed
        Ft = Fw + Fr + Fa + Fi

    while(Ft * velmed >=Battery["battery power"]*0.95):
        i+=1
        aux = (Battery["battery power"]*0.95)/(Ft * velmed)
        deltav *= (aux * (1-i/50))
        Fa = deltav * (car["Mass"]+Battery["battery mass"]) / t
        velmed = (ivel +ivel + deltav)/2
        Fw = 0.5 * p * car["frontal area"] * car["Drag coefficient"] * velmed * velmed
        Ft = Fw + Fr + Fa + Fi

        

    if (j < len(trackmaxspd)-1):
        if(trackmaxspd[j] > trackmaxspd[j+1]):
            deltav2 = trackmaxspd[j+1] - (ivel + deltav)
            Eb = (deltav2 * (car["Mass"]+Battery["battery mass"]))* car["regenerative breaking"] * 2
            Fb = Eb /t
            if((Eb/t)>car["Regenerative breaking MAX power (kW)"]):
                Eb = car["Regenerative breaking MAX power (kW)"]*t
                Fb = car["Regenerative breaking MAX power (kW)"]
            

    if(Ft<0):
        Ft *= car["regenerative breaking"]

    Power =  trackmaxspd[j] * Ft
    if(Power<-Battery["battery power"]): Power = Battery["battery power"]

    Energy = Power * t + Eb # sem rendimento da bateria

    if(printin== 1): csvwriter.writerow([j,Ft,Fa,Fw,Fr,Fi,Fb,ivel+deltav + deltav2,Power,Eb,Energy,t])

    return [Energy, ivel + deltav + deltav2, t]


def totaleverything (lapvel, fbat): #this funtions returns thr total energy consumed by the car in a single lap as well as its final velocity and time tool to finish it

    TE = TT= 0

    for i in range(len(tracklen)):

        if (i==0): aux = raceenergy(lapvel,i)
        else: 
            aux = raceenergy(aux[1],i)

        TE += aux[0]
        TT += aux[2]


    pv = TT * PV["PV eficiency"] * PV["pv area"] * 1000

    Cir = TT * (services["AI"] + services["cooling"] + services["luz"])

    fbat -= (TE*0.95 - pv + Cir)/(3600000*0.95)

    if(printin== 1):
        csvwriter.writerow([])
        csvwriter.writerow(["PV energy", pv, "circuit energy", Cir,"total energy consumed in this lap",(TE*0.95 - pv + Cir)/(3600000*0.95),"battery remaning energy",fbat ])
        csvwriter.writerow([])

    return [ (TE*0.95 - pv + Cir)/(3600000*0.95), aux[1],fbat, TT]


def optimizer(X): # this is the function that the genetical algoritm works on as being a single lap analisys 

    pen = 0

    trackmaxspd = X

    result = totaleverything(0, Battery["battery energy"])

    if (result[0]<=Battery["battery energy"]/20.10): 
        pen =  1000 * result[3]

    return result[3] + pen


def GERBAT (): #suposed function to evaluate  generation, conversion and storage technologies

    print("pilhas de lítio e cenas\t\a\n")

    battery1 = {'mass':0, 'capacity': 69, 'voltage': 24, 'max current':69}
    battery2 = {'mass':0, 'capacity': 69, 'voltage': 24, 'max current':69}
    battery3 = {'mass':0, 'capacity': 69, 'voltage': 24, 'max current':69}
    battery4 = {'mass':0, 'capacity': 69, 'voltage': 24, 'max current':69}
    PV1 = {'mass':0, 'efficiency':.2}
    PV2 = {'mass':0, 'efficiency':.2}


    return





strat = printin = 1

print("strategy id by default to best track time: (1)")

print("please tell me yor csv file directory (without extension)\n")


filename = input()


car = {'Mass': 100, 'Drag coefficient': 0.01,'rolling friction':0.01, 'frontal area': 0.4, 'Power train':100, 'regenerative breaking':0, 'Regenerative breaking MAX power (kW)': 50000} #dicionário do carro

Battery = {'battery mass':100, 'battery energy':300, 'battery eficiency':0.95, 'battery power':100} # tá em KWh

services = { 'luz': 0, 'AI':0, 'cooling':0} # W

PV = {'pv area': 0, 'PV eficiency': 0}

trackmaxspd = []

trackmaxspd1 = []

trackmaxspd0 = []

tracklen = [] #info sobre a pista

trackO = [] # inclinação da pista

fuel = {'CO2 emissions': 0, 'RAD': 3000, 'Primary to Final Efficency Electricity': 1} # dicionário sobre o combustível

with open(filename+ '.csv', mode ='r')as file:

    csvFile = csv.reader(file)

    for line in csvFile:
   

        if (line[0]=="mass (kg)"):
            car['Mass']=float(line[1])
            continue

        if (line[0]=="Power train (kW)"):
            car["Power train"]=float(line[1])*1000
            continue

        if (line[0]=="Rolling friction"):
            car['rolling friction']=float(line[1])
            continue

        if (line[0]=="Frontal Area"):
            car['frontal area']=float(line[1])
            continue

        if (line[0]=="Regenerative breakign average efficiency"):
            car['regenerative breaking']=float(line[1])
            continue

        if (line[0]=="Regenerative breaking MAX power (kW)"):
            car['Regenerative breaking MAX power (kW)']=float(line[1])
            continue

        if (line[0]=="Battery Power (kW)"):
            Battery['battery power']=float(line[1])*1000
            continue

        if (line[0]=="Battery Capacity(kWh)"):
            Battery['battery energy']=float(line[1])
            continue

        if (line[0]=="Battery weigth (kg)"):
            Battery["battery mass"]=float(line[1])
            continue

        if (line[0]=="Cooling System Average Power (W)"):
            services["cooling"]=float(line[1])
            continue   

        if (line[0]=="Lights average power (W)"):
            services["luz"]=float(line[1])
            continue

        if (line[0]=="Control system includign sensors (W)"):
            services["AI"]=float(line[1])
            continue

        if (line[0]=="Primary to Final Efficency Electricity"):
            fuel['Primary to Final Efficency Electricity']=float(line[1])
            continue

        if (line[0]=="CO2 emissions (kgCO2/kWh)"):
            fuel['CO2 emissions']=float(line[1])
            continue

        if (line[0]=="Solar cell efficiency (1000W/m2)"):
            PV["PV eficiency"]=float(line[1])
            continue

        if (line[0]=="Drag coefficient"):
            car['Drag coefficient']=float(line[1])
            continue

        if (line[0]=="Available area for PV cells (m2)"):
            PV["pv area"]=float(line[1])
            continue


        if (line[0]=="acc/break" or line[0]=="1" or line[0]=="2" or line[0]=="3" or line[0]=="4" or line[0]=="5" or line[0]=="6" or line[0]=="7" or line[0]=="8" or line[0]=="9" or line[0]=="10" or line[0]=="11" or line[0]=="12" or line[0]=="13" or line[0]=="14" or line[0]=="15" or line[0]=="16" or line[0]=="17" or line[0]=="18" or line[0]=="19" or line[0]=="20" or line[0]=="21"):
            trackmaxspd1.append(float(line[1]))
            tracklen.append(float(line[2])*1000)
            trackO.append(float(line[3]))
            continue


        line = "\0"


minspd = trackmaxspd1[0] / 3.6
for i in range (0, len(trackmaxspd1)): # from km/h to m/s
    trackmaxspd1[i] = trackmaxspd1[i] / 3.6
    if (minspd > trackmaxspd1[i]): minspd = trackmaxspd1[i]

for i in range (0, len(trackmaxspd1)):
    trackmaxspd0.append(minspd)

trackmaxspd = trackmaxspd1
trackmaxspd2 = trackmaxspd0

menuin = '0'

print("--------------------------------------------------------------")
print("what do you wish to do now \nchoose the command with the number it is represented \n\
---------------------------------------------------------------\
\n| 1: see car, track and fuel info \t 2: Calculate energy and power nedded and calculate all indicators \n| 3: change strategy \t 5: race with current strategy \n| 6: optimize the race \t 7: exit \n| \n|also you can tipe 'h' to see this menu\n\
-----------------------------------------------------------------------\n")


while(menuin != '6'):

    print("\n>>")
    menuin = input()

    if (menuin=='h'):
        print("--------------------------------------------------------------")
        print("what do you wish to do now \nchoose the command with the number it is represented \n\
---------------------------------------------------------------\
        \n| 1: see car, track and fuel info \t 2: Calculate energy and power nedded and calculate all indicators \n| 3: change strategy \t 5: race with current strategy \n| 6: optimize the race \t 7: exit \n| \n|also you can tipe 'h' to see this menu\n\
-----------------------------------------------------------------------\n")

    if (menuin=='1'):

        info()

    if (menuin=='2'):

        print("\n please write the directory in which you want the result file to be\n >>")

        with open(input()+ 'result2.csv', 'w', newline='') as csvfile:

            csvwriter = csv.writer(csvfile)

            csvwriter.writerow(['section','total force','acl force','aerodinamic force','friction force','gravity force','breaking force','final velocity','total power','energy recovered by breaking','total energy consumed','section time'])

            result = totaleverything(0, Battery["battery energy"])


        print("-------------------------------------------")
        print("|results are in  \n for total comsumption:", result[0],"KWh \t final state of charge:", result[2], "KWh \t Primary energy:", (result[0]*3.6)/fuel["Primary to Final Efficency Electricity"], "MJ \t CO2 emissions:",(result[0]*3.6)*fuel['CO2 emissions']/(fuel["Primary to Final Efficency Electricity"]),"Kg/CO2\t Time",result[3])
        print("-------------------------------------------")


    if (menuin=='3'):
        print("Enter your strategy (0 for minimum energy,1 for total race time, 2 for optimized race):\n ")
        print("\n>>")

        strat = input()

        print("strategy selected", strat)

        if (strat != '1' and strat != '0' and strat != '2'):
            print("\a error: value not recognised")

        if (strat == '1'): trackmaxspd = trackmaxspd1
        if (strat == '0'): trackmaxspd = trackmaxspd0
        if (strat == '2'): trackmaxspd = trackmaxspd2


    if (menuin=='4'):

        print("\n please write the directory in which you want the result file to be\n >>")

        with open(input()+ 'result4.csv', 'w', newline='') as csvfile:

            csvwriter = csv.writer(csvfile)

            veltransfer = maxenergy= TT = 0
            bat = Battery["battery energy"]

            for i in range(20):

                csvwriter.writerow([])
                print("lap", i+1)

                csvwriter.writerow(['section','total force','acl force','aerodinamic force','friction force','gravity force','breaking force','final velocity','total power','energy recovered by breaking','total energy consumed','section time'])

                csvwriter.writerow([])
                csvwriter.writerow(['lap',i+1])
                csvwriter.writerow([])        

                result = totaleverything(veltransfer, bat)

                bat = result[2]

                veltransfer = result[1]
                maxenergy += result[0]
                TT += result[3]

                if(bat<0):
                    print("\ni've ran out of battery. I've done ",i," laps")
                    csvwriter.writerow([])
                    csvwriter.writerow(['car out of battery at lap',i])
                    break

        print("\n-------------------------------------------")
        print("results are in  \n for total comsumption:", maxenergy,"KWh \t final state of charge:", bat, "KWh \t Primary energy:", (maxenergy*3.6)/fuel["Primary to Final Efficency Electricity"], "MJ \t CO2 emissions:",(maxenergy*3.6)*fuel['CO2 emissions']/(fuel["Primary to Final Efficency Electricity"]),"Kg/CO2\t time:", TT,"s")
        print("-------------------------------------------")


    if (menuin=='5'):

        printin = 0

        varbound=np.array([minspd-1]*len(tracklen))
        varbound = np.c_[varbound, trackmaxspd]

        algorithm_param = {'max_num_iteration': None,\
                   'population_size':1003,\
                   'mutation_probability':0.4,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.65,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':320}

        model=ga(function=optimizer,dimension=len(trackmaxspd),variable_type='real',variable_boundaries=varbound,algorithm_parameters=algorithm_param)

        model.run()

        trackmaxspd = model.output_dict['variable']

        trackmaxspd2 = trackmaxspd

        printin = 1

        print("\n--------------------------------------")
        print("|done optimizing, press 4 to race\a \n")
        print("--------------------------------------")

print("shutting down")