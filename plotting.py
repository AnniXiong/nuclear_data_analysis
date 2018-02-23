import N_data
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-ticks')

def tripleplot ():
	
	# choose to compare with trigger counts or pulser counts
	third_plot = N_data.count_trig
	plot_title = "channel counts and trigger"
	third_title = "trigger counts"
	figure_title = ""
	
	fig,(ax1,ax2,ax3) = plt.subplots(3) 

	x = np.array(list(range(len(N_data.count_list2)))) + 1
	ax1.plot(x, N_data.ch2rate ,color='g',marker="o",linestyle="-",markersize=5)
	ax2.plot(x, N_data.ch3rate,color='g',marker="o", linestyle="-",markersize=5)
	ax3.plot(x, third_plot,color='r',marker="o", linestyle="-",markersize=5)

	ax1.set_title(plot_title)
	ax3.set_xlabel('Trials by time interval')
	fig.subplots_adjust(hspace=0.10)

	plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
	#ax2.get_yaxis().get_major_formatter().set_useOffset(False)

	ax1.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
	ax2.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
	ax3.ticklabel_format(style='sci',axis='y',scilimits=(0,0))

	ax1.legend(["ch2 Counts"],shadow=True);
	ax2.legend(["ch3 Counts"],shadow=True);
	ax3.legend([third_title],shadow=True);

	ax1.set_ylabel('counts')
	ax2.set_ylabel('counts')
	ax3.set_ylabel('counts')
	plt.savefig(figure_title)
	plt.show()


def corrlation():
	
	centroid_data = N_data.cen_list2
	figure_title = "ch1 count rate and centroid corrlation"
	
	fig1,ax1 = plt.subplots()
	x = np.array(list(range(len(N_data.count_list2)))) + 1
	ax1.plot(centroid_data, N_data.ch2rate ,color='g',marker="o",linestyle="None",markersize=5)
	ax1.set_title("ch2 rate and centroid corrlation")
	ax1.set_xlabel('centroid')
	ax1.set_ylabel('counts')
	plt.text(142.2,2184, "Counts = a * Centroid + b ",fontsize=14)
	plt.text(142.2,2182.3, "a = 4.545,\nb = 1531.26",fontsize = 13.5)
	plt.savefig(figure_title)

def plot_rescale():
	fig1,ax2 = plt.subplots()
	x = np.array(list(range(len(N_data.count_list2)))) + 1
	ax2.plot(x, N_data.corrected_rate,color='g',marker="o",linestyle="None",markersize=5)
	plt.show()
	




tripleplot()
corrlation()


