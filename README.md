# Nuclear data analysis
Code for analyzing JAM histogram data from nuclear counting experiment using Sr-90 source.
The main purpose is to calculate the counting chi square and proporation variation.

# Motivation
The He6 experiment located at the North Physics Lab aims to reach sensitivity 10-3 in searching 
beyond standard model tensor currents that violates chairality. The Fierz interference coefficient (little b) 
is linearly depended on tensor couplings and can be experimentally extracted by precisely measuring the He6 
beta decay spectrum. The technique of cyclotron radiation emission spectroscopy from Project 8 will be used to
reconstruct He6 beta spectrum by measuring the cyclotron radiation frequency of the He6 beta decay. 
Each piece of the energy spectrum will be measured seperately by varying the magnetic field strength before 
combining into a complete spectrum. Since the total number of He6 atoms entering the decay volume can vary 
with accelerator current, each piece of the energy spectra needs to be normalized to the same scale before combination. 
This requires a monitoring system to be put on the path way of the He6 pipe that counts the total number of He6 atoms 
over each period of data taking. As one part of the effort to prepare for the upcoming He6 experimental run, 
this project is to develop this monitoring system so that it maintains a level of stability of 10-3.
The test was carried out on three experimental setups including pair of gas counter plus silicon detector, 
a pair of scintillators and a single silicon detector under vacuum. The NIM electronics modules and JAM software were 
used to handle the data acquistiation. Of the three setups, the single scilicon detector was able to reach desired 
sensitivity on the most recent experimental run. A successfuly setup of the monitoring system will help the experiment 
to reach desired sensitivity with spectrum normalization. And the detection of tensor currents implies the existance 
of symmetry breaking with chairality in beyond standard model theories.

# Requirements
Make sure that Numpy and Matplotlib are installed

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

# Usage (may vary depending on the python version)installed:

Make sure the /Data is present like in the repo;

Object oriented style (linked with nuclear class) (recommended):
    
    python oo_main.py

    
