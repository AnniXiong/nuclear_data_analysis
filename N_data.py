import numpy as np
import matplotlib.pyplot as plt
#import pylab as pl

#input file
ch2data = np.genfromtxt("h2data17.csv",dtype=int, delimiter='\t')
print('Dimension of ch2 data time * energy',ch2data.shape)

ch3data = np.genfromtxt("h3data17.csv", dtype=int, delimiter='\t')
print('Dimension of data time * energy', ch3data.shape)

trigger = np.genfromtxt("trigdata.csv", dtype=int, delimiter='\t')
print('diemnsion of trigger data ', trigger.shape)

pulserdata = np.genfromtxt("pulserdata.csv", dtype=int, delimiter='\t')
print('diemension of pulser data', pulserdata.shape)


#////////////Subject to change
#timemax/interval has to be a integer
timemax = 2000
interval = 100
real_t_interval = (interval/137)*3600
#/////////////Subject to change


def distribution (data, tmin, tmax, Emin, Emax):
	
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

def centroid (Input, Emin, Emax):
	erange = list(range(Emin,Emax + 1))
	numerator = [x * y for x, y in zip (erange, Input)]
	Centroid = sum(numerator) / sum(Input)
	return Centroid

def chisquare (input_rate, input_count):
	rate_sigma = ((np.array(input_count))**0.5)/real_t_interval
	num = sum( np.array(input_rate)/(rate_sigma**2) )
	dem = sum(1/rate_sigma**2)
	mean = num/dem
	chisquare = (sum(((np.array(input_rate) - mean)/rate_sigma)**2))/19
	return chisquare

def rescale(input_cen, input_rate, slope):
	mean_cen = np.mean(np.array(input_cen))
	print("mean_cen",mean_cen)
	del_cen = np.array(input_cen) - mean_cen
	corr_rate = np.array(input_rate) - (del_cen * slope)
	return corr_rate


a = list(range(timemax + 1))
b = a[interval:timemax + interval - 1:interval]
trial = int(timemax/interval)
print('number of trials', trial)
cen_list2 = []
cen_list3 = []
count_list2 = []
count_list3 = []
count_trig = []
pulser_list = []

for i in range(trial):
	tmin = b[i] - (interval - 1) + 5
	tmax = b[i] + 5
	
	# Gathering data for trigger, pulser, counts and centroid calculation by time interval
	counttrig = distribution(trigger,tmin,tmax,0,5000)
	count_trig.append(sum(counttrig))
	
	pulser = distribution(pulserdata,tmin,tmax,840,860)
	pulser_list.append(sum(pulser))

	
	count1 = distribution(ch2data,tmin,tmax,16,1023)
	count_list2.append(sum(count1))
	count2 = distribution(ch3data,tmin,tmax,25,1023)
	count_list3.append(sum(count2))

	centroid2 = centroid(count1,16, 1023)
	cen_list2.append(centroid2)
	centroid3 = centroid(count2,25,1023)
	cen_list3.append(centroid3)


fraction_alive = np.array(count_list2)/np.array(count_trig)
print("fraction alive",fraction_alive)

ch2rate = np.array(count_list2)/real_t_interval
ch3rate = np.array(count_list3)/real_t_interval

print("channel 2 data", count_list2)
print("channel 2 centroid", cen_list2)
print("channel 2 rate", ch2rate)
print("")
print("channel 3 data", count_list3)
print("channel 3 centroid", cen_list3)
print("channel 3 rate", ch3rate)
print("")
print("trigger data", count_trig)
print("pulser data", pulser_list)

#Linear fit between centroid and count rate
linear_fit2 = np.polyfit(np.array(cen_list2),ch2rate,1)
linear_fit3 = np.polyfit(np.array(cen_list3), ch3rate,1)
print("")
print('L fit ch2', linear_fit2, "L fit ch3", linear_fit3)

corrected_rate = rescale(cen_list3, ch3rate,4.80039 )
print("corrected_rate3", corrected_rate)

corrected_count = np.array(corrected_rate)*real_t_interval

chi = chisquare(ch2rate, count_list2)
print("chi_square_before", chi)

corr_chi = chisquare(corrected_rate,corrected_count)
print(corr_chi)





