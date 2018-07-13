# nuclear_data_analysis
Code for analyzing JAM histogram data from nuclear counting experiment using Sr-90 source.
The main purpose is to calculate the counting chi square and proporation variation.

There are two small scintillator paddles used in the experiment; triggering is on the coincidence counts of these two scintillators. Two data sets are generated labeled as ch2(thin and small) and ch3(thick and large) corresponding to each scintillator and they are analyzed the same way separately.

# input file format
The input file consists of purely text data, each represents a count recored by JAM program,
One example looks like the following

  ------> Energy channel
| 1 2 3 4 5 6 ...
| 1 2 3 4 5 6
| ...
∨
time channel

Matplotlib is the used for plotting, the file responsible for plotting is linked with N_data.py

Usage (may vary depending on the python version)installed:

    python3 N_data.py


