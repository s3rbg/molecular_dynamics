The data file must be a CSV (comma separated values) file. In the first column should appear the keywords of the parameters, in the second one the values, in the third the units (if they are required) and, in the following ones, there can be written as many comments as desired.

There is some error testing implemented in the module to read the file. In the case that an error in the input is detected, a personalized message is displayed, with hints to correct the error. The implemented checks are:
    - Spelling of keywords: checks if the keyword is correctly spelled.
    - Missing keyword: checks if there is any missing keyword.
    - Values types: checks if the values provided are of the expected type.
    - Valid unit: checks if the provided unit is included in the accepted ones.
    - Missing colum: checks if one of the compulsory columns is missing, i.e, keywords, values and units.
    
There are also some flexibilities implemented:
    - The keywords, values and units can be written using uppercase letters
    - The order of the keywords is irrelevant
    - There is no need to write the header row, i.e., the keywords can be directly written in the first row
    
Accepted keywords are: 
    - density: number density (particles/volume) of the material. Valid units are 'm**-3' and 'cm**-3'.
    - number_of_units: number of unit cells in one direction, used to create the supercell.
    - temperature: temperature of the material. Accepted units are "K" (or "Kelvin"), "C" (or "Celsius") and "F" (or "Fahrenheit").
    - epsilon: epsilon parameter of the Lennard-Jones potential. Accepted units are "J", "erg", "eV" and "cal".
    - sigma: sigma parameter of the Lennard-Jones potential. Accepted units are "nm", "m", "mm", "cm", "microm", "Angstrom" and "Bohr rad".
    - cutoff_distance: distance in which the potential is shifted, in units of sigma.
    - cutoff_list: maximum distance from one atom to another one in order to consider them neighbours, in units of sigma.
    - CELL_type: type of unitary cell. Currently, the only accepted option is FCC.
    - potential_type: type of potential used to calculate the forces. Accepted potentials are "lennard-jones" and "lennard-jones double shifted". Using "lennard-jones double shifted" is recommended.
    - algo_ode: ODE solving algorithm. Currently developed options are "velocity-verlet", "leap-frog" and "verlet". Using "velocity-verlet" is recommended.
    - tot_t: total number of iterations.
    - delta_t: reduced time step.
    - velocities_dist: velocities distribution used to initialize the velocities. Currently, "M-B" (maxwell-boltzmann distribution) is the only developed option.
    - directory: route to the directory to save the output files. It is recommended to use "output", which will save the files in the output folder of the project.

NOTE: if the path to the file is incorrect, the program will execute with the data of the example file ('data_file_example.txt')

