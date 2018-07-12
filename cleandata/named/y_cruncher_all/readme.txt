data index of iteration experiment on c4 dedicated host:

##begin with 16VMs end with 1
16*c4.large 25m10runs   y_cruncher_dedicated_2ndrun_labeled.csv
8*c4.xlarge 25m100runs  y_cruncher_8*c4.xlarge_25m100runs_labeled.csv
4*c4.2xlarge 25m100runs null
2*c4.4xlarge 25m100runs null

4*c4.2xlarge 25m1runs   y_cruncher_4*c4.2xlarge_25m1runs.csv
2*c4.4xlarge 2.5b1runs 	y_cruncher_2*c4.4xlarge2.5b1runs.csv

Note:
VMs involved
		|VM15|
		 ...
      |VM1| ... |VM1|
|VM0| |VM0| ... |VM0|
--------------------------> Time line
exp1  exp2  ... exp16.      Experiment name 


============================================================================


##reverse sequence, begin with 1VM end with 16VMs
16*c4.large 25m10runs y_cruncher_16*c4.large_25m10runs_reverse

Note:
VMs involved
		|VM15|
		 ...
      |VM1| ... |VM1|
|VM0| |VM0| ... |VM0|
--------------------------> Time line
exp1  exp2  ... exp16.      Experiment name   


============================================================================
About labeled data
'set' means the experiment which that entry is belongs to.
'vmId' is the sequence number of that instance(VM)
   	  