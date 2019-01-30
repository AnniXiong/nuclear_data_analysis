import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class Nuclear_data(object):
	
	def __init__ (self,inputfile, interval, E_range, timeoffset, timemax):
		self.inputfile = inputfile
		self.interval = interval
		self.time = (interval /137) * 3600
		self.E_range = E_range
		self.timeoffset = timeoffset
		self.timemax = timemax
		self.TTimeCh = timemax - timeoffset
		self.trial = int((timemax - timeoffset)/interval)

	def PrintInfo (self):
		print("input file", self.inputfile)
		print("the interval", self.interval)
		print("real time is", self.time)
		print("Energy range is", self.E_range)
		print("time max", self.timemax, "trial", self.trial)
		print("total time channels", self.TTimeCh)
	
	def DatatoArray (self):
		DataA = np.genfromtxt(self.inputfile,dtype=int, delimiter="\t")
		print ("Dimension of data file", DataA.shape)
		return DataA

	def InitialSelection(self, inputfile):
		# Time selection from timeoffset to timemax
		time_range = inputfile[self.timeoffset: self.timemax]     
		# Energy selection from Emin to Emax
		data_choosen = time_range[ : ,self.E_range[0]:self.E_range[1] + 1]
		return data_choosen

	def SumECh(self, inputarray):
		S_array = inputarray.sum(axis = 1)
		return S_array

	def OnedTimeArray (self, inputlist):
		sc = inputlist.reshape(self.trial, self.interval)
		time_array = sc.sum(axis = 1)
		return time_array

	def RateSig (self, inputcount):
		count_rate = inputcount/self.time
		sig = np.sqrt(inputcount)/self.time
		return [count_rate, sig]

	def EnergyArray(self, inputarray):
		binned = inputarray.reshape (self.trial, self.interval, inputarray.shape[1])
		energy_array = binned.sum(axis = 1)
		return energy_array

	def chisquare_std (self, inputcount, input_sigma):
		input_rate = inputcount /self.time
		num = sum(input_rate/(input_sigma**2))
		dem = sum(1/input_sigma**2)
		mean = num/dem
		res = (input_rate - mean)/input_sigma
		chi_s = res**2
		chisquare = sum(chi_s)/(self.trial - 1)
			
		std = np.sqrt(sum((input_rate - mean)**2)/(self.trial-1))
		return [chisquare,std/mean, mean, res]  
	
	def centroid (self, inputcount):
		erange = np.arange(self.E_range[0], self.E_range[1] + 1)
		numerator = erange * inputcount
		Centroid = numerator.sum(axis = 1) / inputcount.sum(axis = 1)
		# centroid error
		eps_n = (((inputcount*erange**2).sum(axis = 1))**0.5)/ numerator.sum(axis = 1)
		eps_d = 1/ ((inputcount.sum(axis = 1))**0.5)
		c_eps = (eps_n**2 + eps_d**2)**0.5
		c_std = Centroid * c_eps
		return [Centroid, c_std]

    # review this later about the s_std.
	def CenCorr(self, input_cen, input_rate, cen_std):
		cen_cr_fit = np.polyfit(input_cen, input_rate, 1, full = True)
		print(cen_cr_fit) 
		b = cen_cr_fit[0][0]
		a = cen_cr_fit[0][1]

		mean_cen = np.mean(input_cen)
		del_cen = input_cen - mean_cen
		corr_rate = input_rate - (del_cen * b)
		#corrected rate error
		s_std = (cen_cr_fit[1]/self.trial)**0.5 # Slope uncertainty using residual
		cs_std = del_cen * b *((cen_std/del_cen)**2 + (s_std / b)**2 )**0.5 # sigma_(cen*slope)
		r_std = ((input_rate/self.time) + cs_std**2)**0.5
		return [corr_rate, r_std, b, a]

	def PCountrate (self, cr_input, error_input, res_input):
		plt.figure ()
		x = np.arange(self.trial)
		gs = gridspec.GridSpec(2, 1, width_ratios=[1], height_ratios=[4,1.5]) # there is only one columnso width ratios is 1 D
		ax_m1 = plt.subplot(gs[0])
		ax_m1.plot (x, cr_input, color='b',marker="o",linestyle="None",markersize=3)
		ax_m1.errorbar(x, cr_input, yerr = error_input , xerr = None, ecolor = 'r')
		ax_m1.set_title("Counting rate and residual", fontsize = 17)
		ax_m1.set_ylabel("counting rate (counts/s)",fontsize=16)
		ax_m1.set_xlim (-0.5, max(x)+0.5)
		
		ax_m2 = plt.subplot(gs[1])
		ax_m2.scatter(x, res_input, s = 6)
		ax_m2.set_ylabel ("Residual", fontsize=16)
		ax_m2.set_xlabel("time (channels, 26 sec/channel)",fontsize=16)
		ax_m2.set_xlim (-0.5, max(x)+0.5)
		plt.subplots_adjust(hspace=0.1)
		plt.show ()

	def PCenCorr (self, cendata, input_rate, b, a):
		fig1,ax = plt.subplots()
		ax.plot(cendata, input_rate, color='b',marker="o",linestyle="None",markersize=3)
		ax.plot(cendata, (cendata * b) + a,color='r')
		ax.set_title("Counting rate and centroid correlation", fontsize = 18)
		ax.set_xlabel('Centroid', fontsize = 17)
		ax.set_ylabel('Count rate (counts/(unit time)', fontsize = 17)
		ax.text(np.mean(cendata),np.mean(input_rate) - 0.35, "Count rate = b * Centroid + a ",fontsize=15,color='r')
		ax.text(np.mean(cendata),np.mean(input_rate - 0.7), "a = "+str(a)+"\nb = "+str(b),fontsize = 14.5,color='r')
		plt.show()

	def Simulation (self, number_of_sample, mu):
		sigma = np.sqrt(mu)
		sim_array = np.zeros((number_of_sample,self.TTimeCh ))
		for i in range (number_of_sample):
			os = np.around(np.random.normal(mu, sigma,self.TTimeCh)) 
			sim_array[i,:] = os
		
		fig, ax = plt.subplots ()
		ax.hist(sim_array[1,:], 50, facecolor='y', histtype = 'step')
		ax.set_title ("chi square distribution")
		return sim_array


	def SimPlot (self, chi_sim, chi_exp, sig_sim, sig_exp):
		fig1, (ax1, ax2) = plt.subplots (2)
		ax1.hist (chi_sim, 50, facecolor='y', histtype = 'step', label= "simulation chi/dof")
		ax1.vlines(chi_exp, 0, 50, colors = 'r', label="experimental chi/dof")
		ax1.set_title ("chi square distribution")
		legend = ax1.legend(loc='upper right', shadow=False, fontsize='14')
		ax2.hist (sig_sim, 50, facecolor='y', histtype = 'step', label="simulation stdev")
		ax2.vlines (sig_exp, 0, 50, colors = 'r', label= "experimental stdev")
		ax2.set_title ("standard deviation distribution")
		legend = ax2.legend(loc='upper right', shadow=False, fontsize='14')
		plt.show ()
