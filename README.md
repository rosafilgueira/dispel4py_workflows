# dispel4py_workflows
This repository is dedicated to store different workflows that we have done for different scientific communities ( e.g., Seismologists, Astrophysics, etc) .

# dispel4py
dispel4py is a free and open-source Python library for describing abstract stream-based workflows for distributed data-intensive applications. It enables users to focus on their scientific methods, avoiding distracting details and retaining flexibility over the computing infrastructure they use. It delivers mappings to diverse computing infrastructures, including cloud technologies, HPC architectures and specialised data-intensive machines, to move seamlessly into production with large-scale data loads. The dispel4py system maps workflows dynamically onto multiple enactment systems, such as MPI, STORM and Multiprocessing, without users having to modify their workflows.

# Installation

Visit the [dispel4py GitHub repository](https://github.com/dispel4py/dispel4py), which contains the instructions for installing it. 

# Training Material

For learning about dispel4py, visit the [dispel4py training GitHub repository](), which contains several tutorial and simple workflows for starting with dispel4py

## Seismology:  Seismic Noise Cross Correlation
	
	
Earthquakes and volcanic eruptions are sometimes preceded or accompanied by changes in the geophysical properties of the Earth, 
such as wave velocities or event rates. The development of reliable risk assessment methods for these hazards requires real-time analysis of seismic data 
and truly prospective forecasting and testing to reduce bias. However, potential techniques, including seismic interferometry and 
earthquake "repeater" analysis, require a large number of waveform cross-correlations, which is computationally intensive, and is particularly challenging in real-time. 

With dispel4py we have developed the *Seismic Ambient Noise Cross-Correlation* workflow (also called the *xcorr* workflow) 
as part of the [VERCE project](http://www.verce.eu) project, which preprocesses and cross-correlates traces from several stations in real-time. 
The *xcorr workflow consists of two main phases:

- Phase 1 -- Preprocess: Each continuous time series from a given seismic station (called a *trace*), is subject to a series of treatments. 
		The processing of each trace is independent from other traces, making this phase "embarrassingly" parallel (complexity O(n), where n is the number of stations
- Phase 2 -- Cross-Correlation  Pairs all of the stations and calculates the cross-correlation for each pair (complexity O(n2)).



Recently the [Pegasus team](https://pegasus.isi.edu/) and  the [dispel4py team](https://github.com/dispel4py/dispel4py) 
have  collaborated  to  enable  automated the *xcorr* workflow, across different computing resources (MPI cluster and Storm cluster)
collecting data from [IRIS](http://ds.iris.edu/ds/nodes/dmc/earthscope/usarray/_US-TA-operational/). For this work, we have
submitted the preprocess part to a MPI cluster, and the cross-corelation to a Storm cluster. 
 
The streaming and the mapping to different enactment systems, such as MPI or Storm,  are managed by dispel4py, 
while the data movement between different execution computing resources (MPI cluster and Storm cluster), 
and the coordination of the workflow execution are automatically managed by Pegasus. 
And we adopted Docker containers, because they can substantially improve computational research reproducibility.

More information about this work can be fout [at](https://www.iris.edu/hq/files/agendas/2016/iris_workshop/FerreiraDaSilvaRafael.pdf)
and [pegasus_dispel4py GitHub repository](https://github.com/dispel4py/pegasus_dispel4py)	

## 

