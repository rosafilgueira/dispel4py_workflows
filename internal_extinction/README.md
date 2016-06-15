# Astrophysics: Internal Extinction of Galaxies workflow' codes

- This workflow uses requests and astropy Python libraries for downloading and parsing the VO tables. 

	pip install requests
	pip install astropy

- This is the command for running the workflow with the 'multi' mapping:

	dispel4py multi int_ext_graph.py -d '{"read" : [ {"input" : "coordinates.txt"} ]}' -n 4 -s

- The ‘coordinates.txt’ file is the workflow's input data with the coordinates of the galaxies.

- By using -n 4, the workflow runs by using 4 processes (-n 4). 

- You can also submit this workflow with other mappings:

	Sequential mapping: 
	dispel4py simple int_ext_graph.py -d '{"read" : [ {"input" : "coordinates.txt"} ]}’ 

	MPI mapping: 
	mpiexec -n 4 dispel4py mpi  int_ext_graph.py -d '{"read" : [ {"input" : "coordinates.txt"} ]}’

**Note**: For using mpi mapping you should have mpi4py Python library and MPICH or OpenMPI installed before. More information at [here](https://pypi.python.org/pypi/mpi4py). 
