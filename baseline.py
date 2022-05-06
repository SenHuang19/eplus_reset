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
        with open("run.config") as f:
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
            # if i % 10 and y and resets and numiter == 0:
                # for cls in resets:
                    # cls.update(y)
                    # r = cls.check_requests(y)
                    # cls.reset(r)
                    # u[cls.control] = cls.current_sp
# #                    print("Control: {}".format(u))
            y = case.advance(u)

        # print(case.get_results()['y']['PCWPum'])
        y = pd.DataFrame.from_dict(case.get_results()['y'])
        y.to_csv('result_{}_{}.csv'.format(config['name'], numiter))
        u = pd.DataFrame.from_dict(case.get_results()['u'])
        u.to_csv('input_{}_{}.csv'.format(config['name'], numiter))


if __name__ == '__main__':

    config={
        'fmupath':"LargeOffice_tampa.fmu",
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
    main(config)