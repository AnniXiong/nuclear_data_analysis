import N_data
import matplotlib.pyplot as plt
import numpy as np

# Plotting nuclear data from scintillators

plt.style.use('seaborn-ticks')
	
#----------Two scintillator channels-------#

fig1,(ax1,ax2) = plt.subplots(2) 

x = np.array(list(range(len(N_data.count_list2)))) + 1
ax1.plot(x, N_data.ch2rate ,color='b',marker="o",linestyle="-",markersize=4)
ax2.plot(x, N_data.ch3rate,color='b',marker="o", linestyle="-",markersize=4)
ax1.set_title("Scintillator counting rate")

ax1.legend(["ch2 Count rate"],shadow=True);
ax1.set_ylabel('counts / sec')
ye2 = ((np.array(N_data.count_list2))**0.5) / N_data.t1
ax1.errorbar(x, N_data.ch2rate, yerr = ye2, xerr = None, ecolor = 'r')

ye3 = ((np.array(N_data.count_list3))**0.5) / N_data.t1
ax2.legend(["ch3 Count rate"],shadow=True);
ax2.errorbar(x, N_data.ch3rate, yerr = ye3 , xerr = None, ecolor = 'r' )

ax2.set_xlabel('Time/Trials')
#plt.show()
#plt.savefig('scintillator.png')

#/////////////////////////////////////////////////////////////////////////////////////////
# Residuals
fig2,(ax1,ax2) = plt.subplots(2) 

ax1.scatter(x, N_data.chi2[2] , s = 4)
#ax1.hlines(N_data.chi2[3], 0, 25, colors = 'r', linestyle = "solid")
ax2.scatter(x, N_data.chi3[2], s = 4)
#ax2.hlines(N_data.chi3[3], 0, 25, colors = 'r', linestyle = "solid")


ax1.set_title("Scintillator counting residual plots")
ax1.legend(["ch2 Count rate residual"],shadow=True);
ax1.set_ylabel('(rate - mean)/sigma_rate')
ax2.legend(["ch3 Count rate residual"],shadow=True);
ax2.set_xlabel('Time/Trials')
plt.show()
#plt.savefig('scintillator_cen2.png')

#/////////////////////////////////////////////////////////////////////////////////////////


#-----------1st Title-------#
third_plot = N_data.cen_list3
plot_title1 = "channel count rate pulser and fraction alive"
third_legend_title = "ch3 Centroid"
figure_title = "triple_plot"
#---------------------------#

fig,(ax1,ax2,ax3) = plt.subplots(3) 

x = np.array(list(range(len(N_data.count_list2)))) + 1
ax1.plot(x, N_data.ch2rate ,color='g',marker="o",linestyle="-",markersize=5)
ax2.plot(x, N_data.ch3rate,color='g',marker="o", linestyle="-",markersize=5)
ax3.plot(x, N_data.frac_alive, color='r',marker="o",linestyle="-",markersize=5)

ax1.set_title(plot_title1)
ax3.set_xlabel('Time')
fig.subplots_adjust(hspace=0.10)

plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
ax2.get_yaxis().get_major_formatter().set_useOffset(False)

ax1.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
ax2.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
ax3.ticklabel_format(style='sci',axis='y',scilimits=(0,0))

ax1.legend(["ch2 Count rate"],shadow=True);
ax2.legend(["ch3 Count rate"],shadow=True);
ax3.legend(["frac_alive"],shadow=True);

#ax1.set_ylabel('count rate')
#ax2.set_ylabel('count rate')
#ax3.set_ylabel('count rate')
#plt.savefig(figure_title)
plt.show()

#/////////////////////////////////////cen///corrleation/////////////////////////////////////////////////


#------------2nd Title------------	
centroid_data = N_data.cen_list3
figure_title2 = "corrlation3.png"
a2 = N_data.linear_fit2[0][0]
b2 = N_data.linear_fit2[0][1]

a3 = N_data.linear_fit3[0][0]
b3 = N_data.linear_fit3[0][1]
#---------------------------------

fig1,ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 5.5))
ax[0].plot(N_data.cen_list2, N_data.ch2rate, color='g',marker="o",linestyle="None",markersize=5)
ax[0].plot(N_data.cen_list2, (np.array(N_data.cen_list2) * a2) + b2,color='r')
ax[1].plot(N_data.cen_list3, N_data.ch3rate, color='g',marker="o",linestyle="None",markersize=5)
ax[1].plot(N_data.cen_list3, (np.array(N_data.cen_list3) * a3) + b3,color='r')
ax[1].ticklabel_format(useOffset=False)

#ax1.plot(centroid_data, 4.8004 * np.array(centroid_data) + 1572.197, color='r', linestyle='-')
ax[0].set_title("ch2rate and centroid correlation")
ax[1].set_title("ch3rate and centroid correlation")
ax[0].set_xlabel('ch2 centroid')
ax[0].set_ylabel('ch2 count rate (counts/(unit time)')
ax[1].set_xlabel('ch3 centroid')
ax[1].set_ylabel('ch3 count rate (counts/(unit time)')	
ax[0].text(18.466,1821.5, "Count rate = a * Centroid + b ",fontsize=14,color='r')
ax[0].text(18.466, 1819.4, "a = "+str(a2)+"\nb = "+str(b2),fontsize = 13.5,color='r')
ax[1].text(178.7,1893, "Count rate = a * Centroid + b ",fontsize=14,color='r')
ax[1].text(178.7,1891.1, "a = "+str(a3)+"\nb = "+str(b3),fontsize = 13.5,color='r')

#41.3,2198
#141.3,2196.4
#257.35,2812.3
#257.35,2811.4

#ax1.set_xlim(257,258)
#ax1.set_ylim(2804,2815)
#plt.savefig("centroid_rate_corr.png")
#plt.show()



# ///////// Histogram plotting /////////////////////////////////////////////////////////
fig3,(ax0,ax1) = plt.subplots(nrows=1, ncols=2, figsize=(12, 5.5))
ax0.hist(N_data.ch2rate,10,facecolor='g')
ax0.set_title("ch2 counting rate")
ax1.hist(N_data.ch3rate,10,facecolor='g')
ax1.set_title("ch3 counting rate")
#plt.show()


# ////////////////////////////////////////////////////////////////////////////////////////////

#-------3rd Title-----------------
plot_title3 = "Rescaled rates"
figure_title3 = "rescale.png"
#---------------------------------

fig2,ax2 = plt.subplots()
x = np.array(list(range(len(N_data.count_list2)))) + 1

fig1,axx = plt.subplots(nrows=1, ncols=2, figsize=(12, 5.5))

axx[0].plot(x, N_data.cen_list2,color='g',marker="o",linestyle="None",markersize=5)

axx[0].plot(x, [np.mean(N_data.cen_list2)]*N_data.trial,color='r',linestyle="-")

axx[1].plot(x, N_data.cen_list3,color='g',marker="o",linestyle="None",markersize=5)

axx[1].plot(x, [np.mean(N_data.cen_list3)]*N_data.trial)

axx[0].ticklabel_format(useOffset=False)
axx[1].ticklabel_format(useOffset=False)

# 15 141.7
# 15 257.625
axx[0].text(15, 18.46, str(np.round(np.mean(N_data.cen_list2), decimals=2)) ,fontsize = 13.5,color='r')
axx[1].text(15, 178.91, str(np.round(np.mean(N_data.cen_list3),decimals=2)) ,fontsize = 13.5,color='r')

axx[0].set_xlabel('trials by time inerval')
axx[1].set_xlabel('trials by time inerval')

axx[0].set_ylabel('ch2 centroid')
axx[1].set_ylabel('ch3 centroid')
axx[0].set_title('ch2 centroid shifting')
axx[1].set_title('ch3 centroid shifting')
#plt.savefig('centroid_shift.png')
#plt.show()


#-----------tst for interval influence on chi
fig,(ax1,ax2) = plt.subplots(2) 

x = np.array(list(range(len(N_data.count_list2)))) + 1
d1 = (N_data.ch2rate - np.mean(N_data.ch2rate))/ np.sqrt(N_data.ch2rate)
d2 = (N_data.ch3rate - np.mean(N_data.ch3rate))/ np.sqrt(N_data.ch3rate)

ax1.plot(x, d1 ,color='g',marker="o",linestyle="-",markersize=5)
ax2.plot(x, N_data.ch3rate,color='g',marker="o", linestyle="-",markersize=5)

ax1.set_title("100")
plt.show()
#tripleplot()
#corrlation()


