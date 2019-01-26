# main program
import nuclear_class as o

d1 = o. Nuclear_data("Data/Si_104.csv",       	# input file
					   61,           	    # interval
					  [4,507],              # E_range, ch3_E_range
					   5,                   # timeoffset，the number of time 					              
					   2567)                # timemax


d = d1.DatatoArray()
sd = d1.InitialSelection(d)
sumd = d1.SumECh(sd)
td = d1.OnedTimeArray(sumd)
cr = d1.RateSig(td)[0]
ed = d1.EnergyArray(sd)
sig = d1.RateSig(td)[1]
chisd = d1.chisquare_std(td, sig)
cen = d1.centroid(ed)
cencorr = d1.CenCorr(cen[0], d1.RateSig(td)[0], cen[1])

corr_stats = d1.chisquare_std(cencorr[0]*1602.92, cencorr[1])
cr_plot = d1.PCountrate (cr, sig, chisd[3] )
cen_plot = d1.PCenCorr (cen[0], cr, cencorr[2], cencorr[3])

print (d1.PrintInfo())
print (d1.DatatoArray())
print ("after initial selection")
print (sd)
print ("dimension of sd", sd.shape)
print (sumd)
print ("length of sumed", len(sumd))
print ("1 d time array")
print (td)
print ("sigma", sig)
print ("statistics is", chisd[0], "standard deviation is ", chisd[1], "weighted mean is", chisd[2])
print ("One d energy array", ed)
print ("Centroid", cen)
print ("Centroid correction", cencorr)
print ("Centroid corrected statistics", corr_stats[0], ", standard deviation is ", corr_stats[1], ", weighted mean is", corr_stats[2] )