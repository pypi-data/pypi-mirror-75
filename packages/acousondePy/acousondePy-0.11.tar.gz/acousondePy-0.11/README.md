# acousondePy
 Translate Acousonde MT files
 
 This software lets you load any Acousonde produced MT files and convert them into easier to use formats.
- Acoustic data files are converted into wav files
- Header information is stored as csv file
- Auxiliary data if present is concatenated into one csv file

For more information on Acousonde visit the (Acousonde website)[http://www.acousonde.com/]

Currently there are 4 functions available:

- MTread() to read one MT file
- spec_plot(p,HEADER,INFO) to create a spectrogram plot
- read_multiple_MT() to read a list of MT files
- acousonde() starts a GUI which allows you to convert slected MT files

For some minimal examples have a look at the notebook subfolder.  

A single Windows executable file of acousonde() which can be used without the need of any programming/scripting and does not require the user to have Python isnstalled can be obtained from (Sourceforge)[https://sourceforge.net/projects/acousonde2wav/].

This software is free to use.
