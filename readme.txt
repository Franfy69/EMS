this project was made with python 3.10.8 64-bit windows version. for compatibility reasons it is recomended to have the same version or
similar python 3 version

all libraries used were:
cmath
fileinput
pickletools
math
numpy
geneticalgorithm
csv

please install them by using "pip install" in cmd (recomended to "run as administrator")

this program doesn't need any arguments but after running it needs the input file name and directory.

this project reads a single csv file, so it's necessary to compile all the information in seperate
lines. As an example, case2.csv has the template one must use.

the program has 3 racing methods, '1' is for the maximum velocity strategy without energy concerns, '0' as a low power method
that the mantains the same speed along the whole track.
the third , '2', is the optimized velocity to finish a endurance race (20 laps) in less time without running out of battery.

The optimizacion tool is a genetical algorithm that only defines new maximum velocities and has a cost function the time took
to finish a lap. If for any reason the GA will output new velocities that don't made the 20 lap race, please redo the
optimization tool.

to make the program read a file the user needs to write the directory plus its name without file extension 
(ex: C:/user/you/desktop/project/case2) (you don't write ."csv")

then the program will print 8 options to interact with:
1- the program outputs all the data that as read
2- the programs "races" a single lap with the defined strategy, giving all the indicators in each section
3- this functions allows to change strategy: 1 for maximum velocity; 0 for low and steady velocity
4- the program "races" the endurance 20 lap race, output all the indicators in each section and lap
5- optimizacion tool that runs the GA ovewriting the defined strategy
6- exit option, ending user loop
h- "help" function, outputing a message about all the options to interact

functions 2 and 4 will output all its indicators in a .csv file (result2.csv and result4.csv, respecfuly) in order to organize all data.
To do that, the user needs to input a directory to insert that file.

good racing!!
