########## INSTALLATION ##########
VERY IMPORTANT NOTE: the package "tqdm" must be installed for the program to execute correctly. In recent versions of Anaconda is already included, but if is not installed just type: "conda install -c conda-forge tqdm" in the shell. The program is prepared to show a warning if it is not installed. In the case of having problems with the installation, the files of the folder "examples" can  be checked. This are the files obtained by the execution of the code in my computer with the default data.  

Instructions to execute the program in Windows:
- Download and unzip the file in a folder of your desire
- Using command-line:
    - Open anaconda-prompt
    - Move to the project folder (molecular_dynamics_simulator) using "cd" command
    - Type: 
        - "python run_simulation.py" to deploy the GUI
            - The information about the parameters can be seen by placing the cursor in the GUI (in the text of the keyword).
            
        - "python run_simulation.py --data_file=<route_to_data_file>" to read a data file. A data file named data.txt is available.
            - For more information about how to do the data file, check the README_data_file.txt, in the "examples" folder.

- Using executable file: Download the executable file from the link which is provided in the "links_to_download_exe_files.txt" file (it is a very big sized file, so it can not be provided in the zip file). Save it in the folder of the project (molecular_dynamics_simulator) and double click on the "executable_for_windows.exe" file. Changing the files in the project won't affect the execution with this method. A new executable must be created in order to see the changes. IMPORTANT: the executable file must be saved on the "molecular_dynamics_simulator" folder in order to work.

########## MODELS ##########
Some UML diagrams are contained in the models folder, with a text file briefly describing them.

########## OUTPUT FILES ##########
Output files (saved by default in the "output" folder) include initial positions, velocities, energy for every time step, a plot with the energy for every step (to check energy conservation) and positions for every time step in a .axsf format file (which can be provided to XcrySDen to visualize the movement of the particles).

NOTE: There are also videos of the simulation, done with XCrySDen, in the "xcrysden_movies" folder (for some reason, the recording tool wasn't working as expected, so the videos are simply screen recordings, with worse quality unfortunately).
