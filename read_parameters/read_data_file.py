#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 13:20:12 2021

@author: dgiron
"""


from common_modules.imports import *
from common_modules.units_dicts import *
from common_modules.errors import InputError
from read_parameters.check_input_errors import remove_comments, check_keywords, check_str
    

def read_data_txt(data_file):
    """
    Reads the data file, transforming the keywords, values and units in a DataFrame structure,
    with the keyword as the column name

    Parameters
    ----------
    data_file : str
        route to the data file.

    Returns
    -------
    pandas.DataFrame
        dataframe with the data.

    """
    # Check if file exists. If not, uses default values
    if os.path.exists(data_file):
        pd.options.display.float_format = '{:e}'.format
        df = pd.read_csv(data_file, delimiter=',', skipinitialspace=True)
        df = df.T
        # Set first row as header, if needed

        if len(df.iloc[0]) == 14:
            
            df.columns = df.iloc[0]
            df = df[1:]
            
        elif df.index[0].lower() in keywords:
            # If no header is provided rewrites the dataframe with param. header = None
            df = pd.read_csv(data_file, delimiter=',', skipinitialspace=True, header=None)
            df = df.T
            df.columns = df.iloc[0]
            df = df[1:]
        else:
            df.columns = df.iloc[0]
            df = df[1:]

        df.columns = [i.lower() for i in df.columns]
        
        # ------> Change all the data into lower case <-----
        df = df.applymap(lambda s: s.lower() if type(s) == str else s)    
        
        # Remove comments rows (if there are). If there is any column missing, raises an error
        df = remove_comments(df)
        
        # Check if keywords used in the input file are valid
        check_keywords(df)
                
        # Saves parameters in a list, according to the order selected in the
        # list "keywords". If not output file is provided or file path is wrong 
        # it saves the files in the output folder
        parameters = []
        aux = 0

        for i in keywords[:-4]:
            if i == 'directory':
                if i not in df.columns:
                    print('Using default directory')
                    df['directory'] = 'output'

            if i not in list(df.columns):
                raise InputError('Missing parameter "{}" in the text file'.format(i))
            
            if i == 'directory':                       
                if type(df['directory'].iloc[0]) != str:
                    print('Using default directory')
                    df['directory'].iloc[0] = 'output'
                if not os.path.exists(df['directory'].iloc[0]):
                    print('Wrong path, using default value')
                    df['directory'].iloc[0] = 'output'                    
            parameters.append(df[i].iloc[0])
            
        # Add the units of needed parameters, checking if they are valid.
        check_str(density_units.keys(), df['density'].iloc[1], 'Invalid density unit selected. "{}" is not a valid unit'.format(df['density'].iloc[1]))
        check_str(temperature_units, df['temperature'].iloc[1], 'Invalid temperature unit selected. "{}" is not a valid unit'.format(df['temperature'].iloc[1]))
        check_str(distance_units.keys(), df['sigma'].iloc[1], 'Invalid distance unit selected. "{}" is not a valid unit'.format(df['sigma'].iloc[1]))
        check_str(energy_units.keys(), df['epsilon'].iloc[1], 'Invalid energy unit selected. "{}" is not a valid unit'.format(df['epsilon'].iloc[1]))
       
        # Checks if string parameters are valid
        check_str(number_atoms_cell.keys(), df['cell_type'].iloc[0], 'Invalid cell type selected. "{}" is not a valid cell type'.format(df['cell_type'].iloc[0]))
        check_str(potential_types, df['potential_type'].iloc[0], 'Invalid potential type selected. "{}" is not a valid potential'.format(df['potential_type'].iloc[0]))
        check_str(ode_algos, df['algo_ode'].iloc[0], 'Invalid ODE solving algorithm selected. "{}" is not a valid algorithm'.format(df['algo_ode'].iloc[0]))
        check_str(vels_dist, df['velocities_dist'].iloc[0], 'Invalid velocities distribution selected. "{}" is not a valid distribution'.format(df['velocities_dist'].iloc[0]))
        


        parameters.append(df['density'].iloc[1]) # Density units
        
        if df['potential_type'].iloc[0] == 'lennard-jones double shifted' or df['potential_type'].iloc[0] == 'lennard-jones':
            parameters.append(df['sigma'].iloc[1]) # Sigma units
            parameters.append(df['epsilon'].iloc[1]) # Epsilon units
        
        parameters.append(df['temperature'].iloc[1]) # Temperature units
        
        parameters = np.array(parameters)
        
        # Returns the values in a pandas dataframe
        df_units_at_end = pd.DataFrame(parameters, index=keywords)
        df_units_at_end = df_units_at_end.T
        
        return df_units_at_end
        
            
    else:
       
        print('Wrong file name/path, using default values')
        df = pd.DataFrame(default_data, index=keywords)
        df = df.T
                
        return df