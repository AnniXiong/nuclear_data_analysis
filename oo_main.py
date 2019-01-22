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
sig = d1.Sigma(td)
chisd = d1.chisquare_std(sig, td)

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