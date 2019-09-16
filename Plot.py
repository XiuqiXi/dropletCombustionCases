import numpy as np
from matplotlib import pyplot as plt
import re

from matplotlib import rcParams
rcParams['font.family']='serif'
rcParams['font.sans-serif']=['Times New Roman']

#plt.style.use('dark_background')

#fig, ax = plt.subplots()

f_velocity = 'InjectionVelocity'
f_droplet = 'DropletProperties'
f_heatFlux = 'HeatFlux'
f_rawData = "data_full_dropletSize"
f_coeff = "Coefficient"
f_FSR = "data_full_FSR"
f_flameTemperature = "data_flameTemperature"

data_velocity = np.loadtxt(f_velocity)
data_droplet = np.loadtxt(f_droplet)
data_heatFlux = np.loadtxt(f_heatFlux)
data_rawData = np.loadtxt(f_rawData)
data_coeff = np.loadtxt(f_coeff)
data_FSR = np.loadtxt(f_FSR)
data_flameTemperature = np.loadtxt(f_flameTemperature)

font = {'style':'Time New Roman'}

plt.figure()
plt.plot(data_coeff[:,0],data_coeff[:,1],color ='black')
plt.xlim(3,5)
#plt.title('coefficient')
plt.xlabel('Time(s)')
plt.ylabel('C')
plt.savefig('C.png', format = 'png', dpi = 1200)


plt.figure()
plt.plot(data_velocity[:,0],data_velocity[:,1])
plt.title('injection velocity')

#plt.savefig('injection velocity', format = 'png', dpi = 1200)

plt.figure()
plt.plot(data_droplet[:,0],data_droplet[:,1]*10**3, label = 'predictions',color = 'black')
plt.plot(data_rawData[:,0],np.sqrt(data_rawData[:,1])*10**3, label = 'experimental data',ls = '--', color = 'r')
plt.xlim(0,10)
plt.ylim(1.6,2.1)
plt.xlabel('Time(s)')
plt.ylabel('Droplet Radius(mm)')
plt.legend(loc='upper right')
#plt.title('droplet radius')

plt.savefig('droplet radius.png', format = 'png', dpi = 1200)

plt.figure()
plt.plot(data_droplet[:,0],data_droplet[:,2])
plt.title('inerface temperature')

#plt.savefig('inerface temperature', format = 'png', dpi = 1200)


plt.figure()
plt.plot(data_droplet[:,0],data_droplet[:,3])
plt.title('inerface fuel')

#plt.savefig('inerface fuel', format = 'png', dpi = 1200)

for i in range(0):
    data_droplet = np.delete(data_droplet,0,0)

#plt.savefig('FSR', format = 'png', dpi = 1200)

plt.figure()
plt.plot(data_heatFlux[:,0],data_heatFlux[:,1], label = 'max heat flux')
plt.plot(data_heatFlux[:,0],data_heatFlux[:,2], label = 'min heat flux')
plt.plot(data_heatFlux[:,0],data_heatFlux[:,3], label = 'mean heat flux')
plt.legend(loc='upper right')
plt.title('heat flux')


#plt.savefig('heat flux', format = 'png', dpi = 1200)

with open('./postProcessing/fieldMinMax1/0/fieldMinMax.dat') as txtData:

    lines = txtData.readlines()
    lines = np.delete(lines,0,0)
    lines = np.delete(lines,0,0)

    n = len(lines)
    flamePosition = np.zeros(n)
    flameTemperature = np.zeros(n)
    
    for i in range(n):
        abs = re.findall(r'[(](.*?)[)]',lines[i])
        abs = abs[1]
        position = abs.split()
        for j in range(len(position)):
            position[j] = float(position[j])
        flamePosition_temp = np.sqrt(position[0]*position[0]+position[1]*position[1])
        flamePosition[i] = flamePosition_temp
        
        abs = lines[i].split()
        flameTemperature[i] = abs[6]
        

flamePosition = np.delete(flamePosition,0,0)
flameTemperature = np.delete(flameTemperature, 0, 0)

timeFlamePosition = data_velocity[:,0];
timeFlamePosition = np.delete(timeFlamePosition, 0, 0)


plt.figure()
plt.plot(timeFlamePosition,flamePosition)
plt.title('flame position')

data_droplet = np.delete(data_droplet,0,0)

dropletSize = data_droplet[:,1]
fsr = flamePosition/dropletSize

plt.figure()
plt.plot(timeFlamePosition,fsr,label = 'prediction',color = 'black')
plt.scatter(data_FSR[:,0],data_FSR[:,1], label = 'experimental data', color = 'r', marker = 'x')
plt.legend(loc='lower right')
plt.xlabel('Time(s)')
plt.ylabel('FSR')
#plt.title('FSR')

plt.savefig('Flame Stand-off Ratio.png', format = 'png', dpi = 1200)

plt.figure()
plt.plot(timeFlamePosition,flameTemperature,label = 'prediction',color = 'black')
plt.plot(data_flameTemperature[:,0],data_flameTemperature[:,1],label = 'experiments',ls = '--')
plt.plot(data_flameTemperature[:,0],data_flameTemperature[:,2],label = 'analytical solution', ls = '-.')
plt.xlabel('Time(s)')
plt.ylabel('Temperature(K)')
plt.legend(loc = 'lower right')
plt.title('Flame Temprature')

plt.savefig('Flame Temprature.png', format = 'png', dpi = 1200)

f = open('FSR', 'w')

for i in range(len(fsr)):
    f.write(str(timeFlamePosition[i]))
    f.write('\t')
    f.write(str(fsr[i]))
    f.write('\n')

f.close
