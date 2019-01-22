import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

class Nuclear_data(object):
	
	def __init__ (self,inputfile, interval, E_range, timeoffset, timemax):
		self.inputfile = inputfile
		self.interval = interval
		self.time = (interval /137) * 3600
		self.E_range = E_range
		self.timeoffset = timeoffset
		self.timemax = timemax
		self.trial = int((timemax - timeoffset)/interval)

	def PrintInfo (self):
		print("input file", self.inputfile)
		print("the interval", self.interval)
		print("real time is", self.time)
		print("Energy range is", self.E_range)
		print("time max", self.timemax, "trial", self.trial)
	
	def DatatoArray (self):
		DataA = np.genfromtxt(self.inputfile,dtype=int, delimiter="\t")
		print ("Dimension of data file", DataA.shape)
		return DataA

	def InitialSelection(self, inputfile):
		time_range = inputfile[self.timeoffset: self.timemax]     
		#Choose column from Emin to Emax
		data_choosen = time_range[ : ,self.E_range[0]:self.E_range[1] + 1]
		return data_choosen

	def SumECh(self, inputarray):
		S_array = inputarray.sum(axis = 1)
		return S_array

	def OnedTimeArray (self, inputlist):
		sc = inputlist.reshape(self.trial, self.interval)
		time_array = sc.sum(axis = 1)
		return time_array
	def Sigma (self, inputcount):
		sig = np.sqrt(inputcount)/self.time
		return sig

	def chisquare_std (self, input_sigma, inputcount):
		input_rate = inputcount /self.time
		num = sum(input_rate/(input_sigma**2))
		dem = sum(1/input_sigma**2)
		mean = num/dem
		res = (input_rate - mean)/input_sigma
		chi_s = res**2
		chisquare = sum(chi_s)/(self.trial - 1)
			
		std = np.sqrt(sum((input_rate - mean)**2)/(self.trial-1))
		return [chisquare,std/mean, mean]  
	'''
	def centroid (In_count, Emin, Emax):
		erange = np.arange(Emin, Emax + 1)
		numerator = [x * y for x, y in zip (erange, In_count)]
		Centroid = sum(numerator) / sum(In_count)
		# centroid error
		eps_n = ((sum(np.array(In_count)*erange**2))**0.5)/sum(numerator)
		eps_d = ((sum(In_count))**0.5)/sum(In_count)
		c_eps = (eps_n**2 + eps_d**2)**0.5
		c_std = Centroid * c_eps
		c = [Centroid, c_std]
		return c
		'''