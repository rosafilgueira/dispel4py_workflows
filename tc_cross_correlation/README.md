# Seismic Noise Cross-Correlation codes

You need to install obspy library

	pip install obspy

More information for installing obspy can be found [here](https://github.com/obspy/obspy/wiki/Installation-via-PyPi-from-source).

For running the preprocess (realtime_prep.py) and cross-correlation (realtime_xcorr.py or realtime_xcorr_storm.py) workflows, the next information is provided:

- The first workflow (realtime_prep.py) stores the results in a directory called OUTPUT/DATA. 
- The second one (realtime_xcorr.py or realtime_xcorr_storm.py) stores the results in OUTPUT/XCORR directory. 
- This is our script for executing both workflows with multi mapping: 
	

    	export DISPEL4PY_XCORR_STARTTIME=2015-04-06T06:00:00.000
    	export DISPEL4PY_XCORR_ENDTIME=2015-04-06T07:00:00.000
    	rm -rf ./tc_cross_correlation/OUTPUT/DATA
    	rm -rf ./tc_cross_correlation/OUTPUT/XCORR
    	mkdir  ./tc_cross_correlation/OUTPUT/DATA
    	mkdir ./tc_cross_correlation/OUTPUT/XCORR

    	dispel4py multi tc_cross_correlation/realtime_prep.py -f tc_cross_correlation/realtime_xcorr_input.jsn -n 4
    	dispel4py multi tc_cross_correlation/realtime_xcorr.py -n 4

	
- Note: Other mappings can be used like, [simple](https://github.com/dispel4py/pegasus_dispel4py/blob/master/simple_experiment/command-job1.sh), [mpi](https://github.com/dispel4py/docker.openmpi/blob/master/command-postprocess.sh) or [storm](https://github.com/dispel4py/pegasus_dispel4py/blob/master/storm_experiment/command-job.sh).

- The last step is to open the file " tc_cross_correlation/realtime_xcorr_input.jsn” and change the path of the file Copy-Uniq-OpStationList-NetworkStation.txt

		xxx/tc_cross_correlation/Copy-Uniq-OpStationList-NetworkStation.txt  


- You could change the realtime_xcorr_input.jsn for using Uniq-OpStationList-NetworkStation.txt (it contains all the stations) instead of Copy-Uniq-OpStationList-NetworkStation.txt (it contains only a few of stations for testing the workflow). This data has been obtained from the [IRIS](http://ds.iris.edu/ds/nodes/dmc/earthscope/usarray/_US-TA-operational/) website. 

		{
    		"streamProducer" : [ { "input" : “/xxxxxxxxx/tc_cross_correlation/Uniq-OpStationList-NetworkStation.txt" } ]
		}


- It is important that you delete DATA and XCORR directories every time before starting to run your workflows. 
