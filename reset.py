# -*- coding: utf-8 -*-
"""
This module implements the REST API used to interact with the test case.  
The API is implemented using the ``flask`` package.  

"""

# GENERAL PACKAGE IMPORT
# ----------------------
from testcase import EmulatorSetup
import pandas as pd
import time
import csv
import os
import pandas as pd
import numpy as np
import json
import Resets.resets as reset


def main(config):
    for numiter in range(1):
        config['name'] =str(numiter)  
        case = EmulatorSetup(config)
        # Set simulation step    
        case.step = config['step']
        measurements = case.get_measurements()
        print(measurements)
        with open("../run_" + config['location'] + ".config") as f:
            config_reset = json.load(f)
        resets = reset.setup_resets(config_reset, measurements)
        u = {}
        for cls in resets:
            u[cls.control] = cls.default_setpoint
        # Initialize u
        # Simulation Loop
        y = False
        occ = 0
        oat = 21.11
        for i in range(int((int(config['end_time'])-int(config['start_time']))/int(config['step']))):
            # Adjust u based on your ML method
            if i % 10 and y and resets and numiter == 0:
                for cls in resets:
                    cls.update(y)
                    r = cls.check_requests(y)
                    cls.reset(r)
                    u[cls.control] = cls.current_sp
#                    print("Control: {}".format(u))
            y = case.advance(u)

        # print(case.get_results()['y']['PCWPum'])
        y = pd.DataFrame.from_dict(case.get_results()['y'])
        y.to_csv('result_{}_{}_{}.csv'.format(config['name'], numiter, config['location']))
        u = pd.DataFrame.from_dict(case.get_results()['u'])
        u.to_csv('input_{}_{}_{}.csv'.format(config['name'], numiter, config['location']))


if __name__ == '__main__':

    for a in range(6):
    
        if (a == 0):
            location="atlanta"
        elif (a==1):
            location="El_Paso"
        elif (a==2):
            location="newyork"
        elif (a==3):
            location="sandiego"
        elif (a==4):
            location="seattle"
        else :
            location="tampa"
            
        fmuname = "../LargeOffice_"+location+".fmu"
                
        config={  
            'fmupath':fmuname,
            'location':location,
            'start_time':0*86400,
            'end_time':365*86400,
            'step': 60,
            'default':{
                'SupCHWTSet':6.7,
                'SupTSetBot':12.88,
                'SupTSetMid':12.88,
                'SupTSetTop':12.88
            }
        }
        
        with open('run.config', 'r') as f:
            data = f.readlines()
        
        data[2] = '       "dat1": "../configs/'+location+'/floor1_dat_reset.config",\n'
        data[3] = '       "dat2": "../configs/'+location+'/floor2_dat_reset.config",\n'
        data[4] = '       "dat3": "../configs/'+location+'/floor3_dat_reset.config",\n'
        data[5] = '       "chws": "../configs/'+location+'/chw_reset.config"\n'


        with open('run_'+location+'.config', 'w') as f:
            f.writelines(data)
        
        os.mkdir('reset_'+location)
        os.chdir('reset_'+location)
        main(config)
        os.chdir('../')