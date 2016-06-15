A dispel4py for the internal extinction workflow that you sent us. 
At the moment it just prints out the results to stdout but we can change that to something more useful.
To run the example you only need to install dispel4py:

 $ pip install dispel4py   ///// or $ pip install update dispel4py

This workflow also uses requests and astropy for downloading and parsing the VO tables. In case you don’t have those installed you need to do:

$ pip install requests
$ pip install astropy

Then you can run 

$ dispel4py multi int_ext_graph.py -d '{"read" : [ {"input" : "coordinates.txt"} ]}' -n 4 -s

where ‘coordinates.txt’ is the input text file with the coordinates.
This runs the workflow on your local machine using 4 processes (-n 4). Similarly you can run it on a bigger shared memory machine with more processes, or even using MPI for distributed memory.

The workflow itself is defined at the bottom of the python file. First the coordinates are read line by line, then the corresponding VOTable is downloaded from the web service. From the VOTable the columns MType and logR25 are retrieved and these are the input for the calculation of the internal extinction.


You can also submit this workflow with other mappings:

* Sequential mapping: dispel4py simple int_ext_graph.py -d '{"read" : [ {"input" : "coordinates.txt"} ]}’ 

* MPI (important you should have mpi4py and MPICH or OpenMPI installed before): mpiexec -n 4 dispel4py mpi  int_ext_graph.py -d '{"read" : [ {"input" : "coordinates.txt"} ]}’  multi Even_Odd_workflow.py -i 20 -n 4

