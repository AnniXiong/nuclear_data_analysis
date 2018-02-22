#import csv
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

#input file
ch2data = np.genfromtxt("h2data17.csv", dtype=int, delimiter='\t')
print('Dimension of ch2data time * energy', data.shape)
ch3data = np.genfromtxt("h3data17.csv", dtype=int, delimiter='\t')
print('Dimension of ch3data time * energy', data.shape)


#////////////Subject to change
#timemax/interval has to be a integer
timemax = 2000
interval = 50
#/////////////Subject to change


def distribution (ch2data, tmin, tmax, Emin, Emax):
	
	tmaxx = tmax + 1
	# extracting data from 0 to tmax rows(time range)
	time_range = data[tmin:tmaxx]        
	#print("time_range dimension",time_range.shape)
	#Choose column from Emin to Emax
	Emaxx = Emax + 1
	data_choosen = time_range[ : ,Emin:Emaxx]
	s = data_choosen.sum(axis = 0)
	# s returns a list of total counts for a given time interval and energy range
	return s


def centroid (input, Emin, Emax):
	cen_list = []
	erange = list(range(17,Emax + 1))
	numerator = [x * y for x, y in zip (erange, count)]
	centroid = sum(numerator) / sum(count)
	cen_list.append(centroid)
	return cen_list




a = list(range(timemax + 1))
b = a[interval:timemax + interval - 1:interval]
trial = int(timemax/interval)
print('number of trials', trial)
count_s = []
#cen_list = []
for i in range(trial):
	tmin = b[i] - (interval - 1)
	tmax = b[i]
	count = distribution(ch2data,tmin,tmax,17,800)
	count_s.append(sum(count))

	cent = centroid(count, 17, 800)
	
	'''erange = list(range(17,801))
				numerator = [x * y for x, y in zip (erange, count)]
				centroid = sum(numerator) / sum(count)
				cen_list.append(centroid)'''

print(len(erange), len(count))
print("counts", count_s)
print("centroid", cen)

plt.style.use('ggplot')
fig,ax = pl.subplots() 
#fig.set_size_inches(11,8.5)
#y = distribution(data,0,137,0,400)
y = count_s
x = np.array(list(range(len(y)))) + 1
print('x dimension ',len(x),'y diemnsion ',len(y))
print('max counts is ', max(y), ', min counts is', min(y), 'percent difference is', (max(y)-min(y))/max(y))
ax.plot(x, y,marker="o",linestyle="-",markersize=5)
ax.set_xlabel('trials by time interval')
ax.set_ylabel('counts')
#ax.set_xlim(17,800)
#ax.set_ylim(0,5000)
#ax.set_yscale('log')
ax.autoscale()
#print(x)


plt.show()
#print (y)


