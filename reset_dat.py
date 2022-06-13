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
import postprocess
import shutil


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
            if not i % 5 and y and resets and numiter == 0:
                for cls in resets:
                    cls.update(y)
                    r = cls.check_requests(y, i)
                    cls.reset(r)
                    u[cls.control] = cls.current_sp
#                    print("Control: {}".format(u))
            y = case.advance(u)

        # print(case.get_results()['y']['PCWPum'])
        y = pd.DataFrame.from_dict(case.get_results()['y'])
        y.to_csv('result_{}_{}_{}.csv'.format(config['name'], numiter, config['location']))
        u = pd.DataFrame.from_dict(case.get_results()['u'])
        u.to_csv('input_{}_{}_{}.csv'.format(config['name'], numiter, config['location']))

    
def run(location, param):
    
    if(param=='clg_request_thr'):
        min_val = 0.5
        max_val = 1
        incr = 0.05
        cases = 10
        ind = 13
    elif(param=='oat_high'):
        min_val = 15.56
        max_val = 24.96
        incr = 0.2
        cases = 27
        ind = 5
    elif(param=='max_sp'):
        min_val = 12.78
        max_val = 18.38
        incr = 0.2
        cases = 27
        ind = 9
    elif(param=='ignored_requests'):
        min_val = 0
        max_val = 5
        incr = 1
        cases = 5
        ind = 15
    elif(param=='htg_request_th'):
        min_val = 0.25
        max_val = 1
        incr = 0.05
        cases = 15
        ind = 14

    for a in range(cases+1):
        
        val = (a/(cases))*(max_val-min_val)+min_val
        val = str(val)
        print('parameter, iter, val: ', param,a+1,val)
            
        with open('configs/'+location+'/floor1_dat_reset_default.config', 'r') as f:
            data = f.readlines()
            
        data[ind] = '    "'+param+'": '+val+',\n'
        
        with open('configs/'+location+'/floor1_dat_reset.config', 'w') as f:
            f.writelines(data)
            
        with open('configs/'+location+'/floor2_dat_reset_default.config', 'r') as f:
            data = f.readlines()
            
        data[ind] = '    "'+param+'": '+val+',\n'
        
        with open('configs/'+location+'/floor2_dat_reset.config', 'w') as f:
            f.writelines(data)
            
        with open('configs/'+location+'/floor3_dat_reset_default.config', 'r') as f:
            data = f.readlines()
            
        data[ind] = '    "'+param+'": '+val+',\n'
        
        with open('configs/'+location+'/floor3_dat_reset.config', 'w') as f:
            f.writelines(data)
    
            
        fmuname = "../LargeOffice_"+location+".fmu"
                
        config={  
            'fmupath':fmuname,
            'location':location,
            'iter':a+1,
            'param':param,
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
        data[5] = '       "chws": "../configs/'+location+'/chw_reset_default.config"\n'


        with open('run_'+location+'.config', 'w') as f:
            f.writelines(data)
        
        os.mkdir('reset_'+location+'_'+param+'_'+str(a+1))
        os.chdir('reset_'+location+'_'+param+'_'+str(a+1))
        main(config)
        postprocess.plot_main(location)
        shutil.rmtree('Output_EPExport_0')
        shutil.rmtree('Output_EPExport_Slave')
        os.chdir('../')
        
    return