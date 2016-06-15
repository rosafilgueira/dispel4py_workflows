# Seismic Noise Cross-Correlation codes

You need to install obspy library

	pip install obspy

More information for installing obspy can be found [at](https://github.com/obspy/obspy/wiki/Installation-via-PyPi-from-source)

For running the preprocess (realtime_prep.py) and cross-correlation (realtime_xcorr.py or realtime_xcorr_storm.py) workflows, the next information is provided:

- The first workflow (realtime_prep.py) stores the results in a directory called OUTPUT/DATA. 
- The second one (realtime_xcorr.py or realtime_xcorr_storm.py) stores the results in OUTPUT/XCORR directory. 
- This is our script for executing both workflows: 
	
	#!/bin/bash
	#log="log"
	set -x


    	export DISPEL4PY_XCORR_STARTTIME=2015-04-06T06:00:00.000
    	export DISPEL4PY_XCORR_ENDTIME=2015-04-06T07:00:00.000



    	rm -rf ./tc_cross_correlation/OUTPUT/DATA
    	rm -rf ./tc_cross_correlation/OUTPUT/XCORR
    	mkdir  ./tc_cross_correlation/OUTPUT/DATA
    	mkdir ./tc_cross_correlation/OUTPUT/XCORR

    	dispel4py multi tc_cross_correlation/realtime_prep.py -f tc_cross_correlation/realtime_xcorr_input.jsn -n 4

    	dispel4py multi tc_cross_correlation/realtime_xcorr.py -n 4



- The last step is to open the file " tc_cross_correlation/realtime_xcorr_input.jsn”. 
   You need to change the path of the file Copy-Uniq-OpStationList-NetworkStation.txt
	“xxx/tc_cross_correlation/Copy-Uniq-OpStationList-NetworkStation.txt”  

	Explanation: The realtime_xcorr_input.jsn has the file’s path of the stations' name that realtime_prep.py workflow needs as input. 
	The  Copy-Uniq-OpStationList-NetworkStation.txt file only have a few, but you also have a file called "Uniq-OpStationList-NetworkStation.txt” with all the stations. 


- You could change the realtime_xcorr_input.jsn for using Uniq-OpStationList-NetworkStation.txt instead of Copy-Uniq-OpStationList-NetworkStation.txt . 

	{
    	"streamProducer" : [ { "input" : “/xxxxxxxxx/tc_cross_correlation/Uniq-OpStationList-NetworkStation.txt" } ]
	}


- It is important that you delete DATA and XCORR directories every time before starting to run your workflows. 
