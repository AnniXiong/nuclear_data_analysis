# main program
import nuclear_class as o
import numpy as np

d1 = o. Nuclear_data("Data/Si_104.csv",     # input file
					   61,           	    # interval
					  [4,507],              # E_range, ch3_E_range
					   5,                   # timeoffset，the number of time channels to be excluded in the begining					              
					   2567)                # timemax            

# Arrange data and calculate stats
d = d1.DatatoArray()
sd = d1.InitialSelection(d)
sumd = d1.SumECh(sd)
td = d1.OnedTimeArray(sumd)
cr = d1.RateSig(td)[0]
ed = d1.EnergyArray(sd)
sig = d1.RateSig(td)[1]
chisd = d1.chisquare_std(td, sig)

# Calculate centroids and do corrections
cen = d1.centroid(ed)
cencorr = d1.CenCorr(cen[0], d1.RateSig(td)[0], cen[1])
corr_stats = d1.chisquare_std(cencorr[0]*1602.92, cencorr[1])
d1.PCountrate (cr, sig, chisd[3] )
d1.PCenCorr (cen[0], cr, cencorr[2], cencorr[3])

# Do simulation according to the mu and sigma of exp data
sim  = d1.Simulation(1000, 623*26.28)
chisd_sim_array = np.zeros((2, 1000))
for i in range (1000):
	binned_count = d1.OnedTimeArray (sim[i,:])
	chisd_sim = d1.chisquare_std(binned_count, d1.RateSig(binned_count)[1])
	chisd_sim_array[0,i] = chisd_sim [0]
	chisd_sim_array[1,i] = chisd_sim [1]
d1.SimPlot (chisd_sim_array[0,:], chisd[0], chisd_sim_array[1,:], chisd[1])


print (d1.PrintInfo())
print ("Raw data in to array form", d1.DatatoArray())
print ("After initial selection", sd)
print ("Dimension of data array after initial selection", sd.shape)
print ("sum all energy channels", sumd, "length after summing all energy channels", len(sumd))
print ("1 d time array", td)
print ("Sigma", sig)
print ("One d energy array", ed)
print ("Centroid", cen)
print ("Centroid correction", cencorr)
print ("Raw statistics is", chisd[0], "standard deviation is ", chisd[1], "weighted mean is", chisd[2])
print ("Centroid corrected statistics", corr_stats[0], ", standard deviation is ", corr_stats[1], ", weighted mean is", corr_stats[2] )
print ("Simulated data", sim)
print ("Simulation chi and stdev array",chisd_sim_array)