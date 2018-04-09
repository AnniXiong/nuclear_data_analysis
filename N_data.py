import numpy as np
import sys

#input file
# h2data17.csv, h3data17.csv, trigdata.csv, pulserdata.csv
# ch2_b.csv, ch3_t.csv, scaler.csv

if str(sys.argv[1]) == "1":
	ch2file = "h2data17.csv"
	ch3file = "h3data17.csv"
	ch2_E_range = [16,1023]  # 16 1023  /4 500
	ch3_E_range = [25,1023]
elif str(sys.argv[1]) == "2":
	ch2file = "ch2_b.csv"
	ch3file = "ch3_t.csv"
	ch2_E_range = [4,500]  # 16 1023  /4 500
	ch3_E_range = [4,900]

ch2data = np.genfromtxt(ch2file,dtype=int, delimiter='\t')
#print(ch2data)
print('Dimension of ch2 data time * energy',ch2data.shape)

ch3data = np.genfromtxt(ch3file, dtype=int, delimiter='\t')
print('Dimension of data time * energy', ch3data.shape)

trigger = np.genfromtxt("trigdata.csv", dtype=int, delimiter='\t')
print('diemnsion of trigger data ', trigger.shape)

pulserdata = np.genfromtxt("pulserdata.csv", dtype=int, delimiter='\t')
print('diemension of pulser data', pulserdata.shape)

#////////////Subject to change
#timemax/interval has to be a integer
timeoffset = 5
timemax = 1000 + timeoffset
interval = 100
trial = int(timemax/interval)
t1 = (interval/137)*3600
t2 = 3600
#/////////////Subject to change

def distribution (data, tmin, tmax, Emin, Emax):
	# extracting data from 0 to tmax rows(time range)
	time_range = data[tmin:tmax + 1]        
	#Choose column from Emin to Emax
	data_choosen = time_range[ : ,Emin:Emax + 1]
	#s = data_choosen.sum(axis = 0)
	return data_choosen

def centroid (In_count, Emin, Emax):
	erange = list(range(Emin,Emax + 1))
	numerator = [x * y for x, y in zip (erange, In_count)]
	Centroid = sum(numerator) / sum(In_count)
	# centroid error
	eps_n = ((sum(np.array(In_count)*(np.array(erange)**2)))**0.5)/sum(np.array(erange) * np.array(In_count))
	eps_d = ((sum(np.array(In_count)))**0.5)/sum(np.array(In_count))
	c_eps = (eps_n**2 + eps_d**2)**0.5
	c_std = Centroid * c_eps
	c = [Centroid, c_std]
	return c

def chisquare_std (input_sigma, input_rate, input_count):
	num = sum(np.array(input_rate)/(input_sigma**2) )
	dem = sum(1/input_sigma**2)
	mean = num/dem
	
	chisquare = sum( ((np.array(input_rate) - mean)/input_sigma)**2) /(trial - 1)
	std = (sum((np.array(input_rate) - mean)**2)/(trial-1)**0.5)
	return [chisquare,std/mean]

def rescale(input_cen, input_rate, linear_fit, c_std):
	slope = linear_fit[0][0]
	mean_cen = np.mean(np.array(input_cen))
	print("mean_cen",mean_cen)
	del_cen = np.array(input_cen) - mean_cen
	del_rate = del_cen * slope
	corr_rate = np.array(input_rate) - del_rate
	corr_rate2 = corr_rate
	
	cen_std = np.array(c_std)
	s_std = (linear_fit[1]/trial)**0.5 # Slope uncertainty
	cs_std = del_cen * linear_fit[0][0]*((cen_std/input_cen)**2 + (s_std / slope)**2 )**0.5
	r_std = ((input_rate/t1) + cs_std**2)**0.5
	return [corr_rate2, r_std]
			
# Calculating denominator of the fraction alive
'''def denominator (count_list):
	scaling_factor = 8
	rev = (len(count_list) - idx for idx, item in enumerate(reversed(count_list), 1) if item)
	last_non_zero_index = next(rev) + 1
	max_count = max(count_list)
	max_indeces = [i for i, j in enumerate(count_list) if j == max_count]
	channel = max(max_indeces) + 1 # channel number with the largest count
	
	#dem = channel * scaling_factor
	dem = ((max_count-1) * last_non_zero_index) + channel
	return dem'''

def denominator (count_list):
    
    length = len(count_list)
    nonzero_indeces = (length-idx for idx, item in enumerate(reversed(count_list), 0) if item != 0 and idx > 0)
    last_non_zero_index = next(nonzero_indeces, -1)

    max_count = max(count_list)
    max_indeces = (length-i for i, j in enumerate(reversed(count_list), 0) if j == max_count)
    channel = next(max_indeces, -2) # channel number with the largest count
    
    dem = (max_count-1) * last_non_zero_index + channel
    return dem

a = list(range(timemax + 1))
b = a[interval:timemax + interval - 1:interval]

# Declering empty lists
cen_list2 ,cen_list3 , count_list2 , count_list3 , count_trig, pulser_list,frac_alive, c2_std,c3_std, corr_r2_std, corr_r3_std = ([] for i in range(11))

for i in range(trial):
	tmin = b[i] - (interval - 1) + timeoffset
	tmax = b[i] + timeoffset
	
	# Gathering data for trigger, pulser, counts and centroid calculation by time interval
	counttrig = distribution(trigger,tmin,tmax,0,5000)

	#non_zero_ele = np.count_nonzero(counttrig)
	#non_zero.append(non_zero_ele)
	#den = non_zero_ele * 8
	#count_trig.append(sum(counttrig.sum(axis = 0)))

	den = denominator(counttrig.sum(axis = 0))
	fraction_alive = sum(counttrig.sum(axis = 0))/den
	frac_alive.append(fraction_alive)

	pulser = distribution(pulserdata,tmin,tmax,840,860)
	pulser_list.append(sum(pulser.sum(axis = 0)/t1))

	count1 = distribution(ch2data,tmin,tmax,ch2_E_range[0],ch2_E_range[1])
	count_list2.append(sum(count1.sum(axis = 0)))
	count2 = distribution(ch3data,tmin,tmax,ch3_E_range[0],ch3_E_range[1])
	count_list3.append(sum(count2.sum(axis = 0)))

	centroid2 = centroid(count1.sum(axis = 0),ch2_E_range[0],ch2_E_range[1])
	cen_list2.append(centroid2[0])
	c2_std.append(centroid2[1])
	
	
	centroid3 = centroid(count2.sum(axis = 0),ch3_E_range[0],ch3_E_range[1])
	cen_list3.append(centroid3[0])
	c3_std.append(centroid3[1])
	

print("fraction alive",frac_alive)
#print("non zero", non_zero)
ch2rate = np.array(count_list2)/t1
ch3rate = np.array(count_list3)/t1

print("channel 2 data", count_list2)
print("channel 2 centroid", cen_list2)
print("centroid 2 uncertainty", c2_std)
print("")
print("channel 2 rate", ch2rate)

print("")
print("channel 3 data", count_list3)
print("channel 3 centroid", cen_list3)
print("centroid 3 uncertainty", c3_std)
print("channel 3 rate", ch3rate)
print("")
print("trigger data", count_trig)
print("pulser data", pulser_list)

#Linear fit between centroid and count rate
linear_fit2 = np.polyfit(np.array(cen_list2),ch2rate,1,full = True)
linear_fit3 = np.polyfit(np.array(cen_list3), ch3rate,1, full = True)
print("")
print('L fit ch2', linear_fit2)
print("L fit ch3", linear_fit3)
print("")
corrected_rate2 = rescale(cen_list2, ch2rate, linear_fit2, c2_std)
print("corrected_rate2", corrected_rate2[0])
del_count2 = (corrected_rate2 - ch2rate) * t1

corrected_rate3 = rescale(cen_list3, ch3rate, linear_fit3, c3_std)
print("corrected_rate3", corrected_rate3[0])
del_count3 = (corrected_rate3 - ch3rate) * t1

corrected_count2 = np.array(corrected_rate2[0])*t1
corrected_count3 = np.array(corrected_rate3[0])*t1

# Two scintillator channels
print("Ch2")
chi2 = chisquare_std( (np.array(count_list2)**0.5/t1), ch2rate, count_list2)
print("ch2 chi_square_before", chi2[0])
corr_chi2 = chisquare_std(corrected_rate2[1],corrected_rate2[0], corrected_count2)
print("ch2 corrected chi", corr_chi2[0])
print("ch2 stdv", chi2[1] )
print("ch2 corrected stdv", corr_chi2[1])

print("ch3")
chi3 = chisquare_std(np.array(count_list3)**0.5/t1,ch3rate, count_list3)
print("ch3 chi_square_before", chi3[0])
corr_chi3 = chisquare_std(corrected_rate3[1],corrected_rate3[0],corrected_count3)
print("ch3 corrected chi", corr_chi3[0])
print("ch3 stdv", chi3[1] )
print("ch3 corrected stdv", corr_chi3[1])

'''gas = np.array([551575, 583902,549772, 578526, 503847, 466445, 542250, 462750, 460382, 514718, 484827, 507486])
si = np.array([979359, 984088, 984482, 986426,982208,1060825,987379,988599,991460,990345,988944, 989079])
gasrate = gas/t2
sirate = si/t2

# Si and gas counter
print("")
print("")
chigas = chisquare(gasrate, gas, None, t2)
print("gas chi square", chigas)
std_gas = stdv(gasrate, gas, 11)/np.mean(gasrate)
print("standard dev gas", std_gas)

chisi = chisquare(sirate, si, None, t2)
print("si chi square", chisi)
std_si = stdv(sirate, si, 11)/np.mean(sirate)
print("standard dev si", std_si)

c = distribution(trigger,1,2000,0,5000)
s = np.count_nonzero(counttrig, axis = 1)

print(s)'''

#print(corrected_rate2)
