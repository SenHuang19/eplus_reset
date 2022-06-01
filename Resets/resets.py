# -*- coding: utf-8 -*-
"""
This module is an example python-based testing interface.  It uses the
``requests`` package to make REST API calls to the test case container,
which mus already be running.  A controller is tested, which is 
imported from a different module.
  
"""

import os
import sys

import numpy as np
import json
import importlib
import csv
from datetime import datetime, timedelta


def setup_resets(config, measurements):
    resets = []
    device_resets = config.get('resets')
    for name, config in device_resets.items():
        path = config
        with open(path) as f:
            reset_config = json.load(f)
        try:
            class_name = reset_config.pop("class")
            cls = factory(class_name)
            resets.append(cls(measurements, reset_config))
        except KeyError:
            print("Missing class definition for {}".format(name))
            continue
    return resets


def factory(classname):
    base_module = "Resets.resets"
    module = importlib.import_module(base_module)
    cls = getattr(module, classname)
    return cls


class Reset:
    def __init__(self, config):
        self.validate_config(config)
        self.min_sp = config.pop("min_sp")
        self.max_sp = config.pop("max_sp")
        self.trim = config.pop("trim")
        self.respond = config.pop("respond")
        self.occupancy = 0
        try:
            self.max_respond = config.pop("max_respond")
        except KeyError:
            self.max_respond = 2*self.respond
        self.default_setpoint = config.pop("default_sp")
        try:
            self.ignored_requests = config.pop("ignored_requests")
        except KeyError:
            self.ignored_requests = 1
        self.current_sp = float(self.default_setpoint)

    def validate_config(self, config):
        config_error = False
        config_keys = list(config.keys())
        if "min_sp" not in config_keys:
            print("Missing min_sp from config!")
            config_error = True
        if "max_sp" not in config_keys:
            print("Missing max_sp from config!")
            config_error = True
        if "trim" not in config_keys:
            print("Missing trim from config!")
            config_error = True
        if "respond" not in config_keys:
            print("Missing respond from config!")
            config_error = True
        if "default_sp" not in config_keys:
            print("Missing default_setpoint from config!")
            config_error = True
        if config_error:
            sys.exit()

    def reset(self, _requests):
        if not self.occupancy:
            self.current_sp = self.default_setpoint
            return

        if _requests > self.ignored_requests:
            sp = self.current_sp - min((_requests - self.ignored_requests) * self.respond, self.max_respond)
        else:
            sp = self.current_sp + self.trim
        self.current_sp = min(self.max_sp, max(sp, self.min_sp))


class DatReset(Reset):
    def __init__(self, measurements, config):
        """
        Trim and respond DAT Reset
        """
        super().__init__(config)
        self.name = config.pop('name', "reset")
        try:
            oat_low = config.pop("oat_low")
        except KeyError:
            oat_low = 15.56
        try:
            oat_high = config.pop("oat_high")
        except KeyError:
            oat_high = 21.11
        try:
            self.request1 = config.pop("request1")
        except KeyError:
            self.request1 = 1.5
        try:
            self.request2 = config.pop("request2")
        except KeyError:
            self.request2 = 2.0
        try:
            self.clg_request_thr = config.pop("clg_request_thr")
        except KeyError:
            self.clg_request_thr = 0.95
        try:
            self.htg_request_thr = config.pop("htg_request_thr")
        except KeyError:
            self.htg_request_thr = 0.95
        try:
            self.oat_name = config.pop("oat_name")
        except KeyError:
            self.oat_name = 'TOutDryBul'
        try:
            self.occupancy_name = config.pop("occupancy_name")
        except KeyError:
            self.occupancy_name = 'occ'

        self.csp = {}
        self.hsp = {}
        self.zt = {}
        self.zclg = {}
        self.zhtg = {}
        self.rated_htg_flow = {}
        self.zone_list = []
        self.zone_clg_req = {}
        self.zone_htg_req = {}
        self.control = None
        self.validate(measurements, config)
        self.max_sat_bounds = np.linspace(18.34, 12.78, 100)
        self.oat_bounds = np.linspace(oat_low, oat_high, 100)

    def validate(self, measurements, config):
        self.control = config.pop('control')
        self.zone_list = list(config.keys())
        self.zone_clg_req = dict.fromkeys(self.zone_list, False)
        self.zone_htg_req = dict.fromkeys(self.zone_list, False)
        for zone, zone_info in config.items():
            for name, point in zone_info.items():
                #if point not in measurements:
                #    print("DAT RESET cannot be implemented check configuration mapping! -- {}".format(point))
                if name == "temperature":
                    self.zt[zone] = point
                elif name == "cooling_setpoint":
                    self.csp[zone] = point
                elif name == "heating_setpoint":
                    self.hsp[zone] = point
                elif name == "cooling_signal":
                    self.zclg[zone] = point
                elif name == "heating_signal":
                    self.zhtg[zone] = point
                elif name == "rated_htg_flow":
                    print(point)
                    self.rated_htg_flow[zone] = point

    def generate_clg_request(self, zone_name, clg_signal, zt, csp):
        clg_requests = 0
        if zt - csp > self.request2:
            clg_requests = 3
        elif zt - csp > self.request1:
            clg_requests = 2
        elif clg_signal > self.clg_request_thr:
            clg_requests = 1
            self.zone_clg_req[zone_name] = True
        elif self.zone_clg_req[zone_name] and clg_signal > self.clg_request_thr - 0.1:
            clg_requests = 1
        else:
            self.zone_clg_req[zone_name] = False
        return clg_requests

    def generate_htg_request(self, zone_name, htg_signal, zt, hsp):
        htg_requests = 0
        if hsp - zt > self.request2:
            htg_requests = 3
        elif hsp - zt > self.request1:
            htg_requests = 2
        elif htg_signal > self.htg_request_thr:
            htg_requests = 1
            self.zone_htg_req[zone_name] = True
        elif self.zone_htg_req[zone_name] and htg_signal > self.htg_request_thr - 0.1:
            htg_requests = 1
        else:
            self.zone_htg_req[zone_name] = False
        return htg_requests

    def check_requests(self, measurements, i):
        clg_requests = 0
        htg_requests = 0

        for zone in self.zone_list:
            temp = 0
            zt = measurements[self.zt[zone]]
            csp = measurements[self.csp[zone]]
            hsp = measurements[self.hsp[zone]]
            clg_signal = measurements[self.zclg[zone]]
            if self.rated_htg_flow[zone]:
                htg_signal = measurements[self.zhtg[zone]]/self.rated_htg_flow[zone]
            else:
                htg_signal = 0.0
            print("name: {} - zone {} -- occ {} -- max_sp: {} -- zt: {} -- cps: {} -- clg: {} -- htg: {}".format(self.name, zone, self.occupancy, self.max_sp, zt, csp, clg_signal, htg_signal))
            clg_temp = self.generate_clg_request(zone, clg_signal, zt, csp)
            htg_temp = self.generate_htg_request(zone, htg_signal, zt, hsp)

            clg_requests += clg_temp
            htg_requests += htg_temp
        _requests = max(0, clg_requests - htg_requests)
        print("request: {} -- : {}".format(_requests, temp))
        return _requests

    def update(self, measurements):
        oat = measurements[self.oat_name]
        self.occupancy = int(measurements[self.occupancy_name])
        self.max_sp = np.interp(oat, self.oat_bounds, self.max_sat_bounds)


class ChwReset(Reset):
    def __init__(self, measurements, config):
        """
        Trim and respond DAT Reset
        """
        super().__init__(config)
        self.name = config.pop('name', "reset")
        try:
            oat_low = config.pop("oat_low")
        except KeyError:
            oat_low = 15.56
        try:
            oat_high = config.pop("oat_high")
        except KeyError:
            oat_high = 21.11
        try:
            self.request1 = config.pop("request1")
        except KeyError:
            self.request1 = 2.0
        try:
            self.request2 = config.pop("request2")
        except KeyError:
            self.request2 = 3.0
        try:
            self.clg_request_thr = config.pop("clg_request_thr")
        except KeyError:
            self.clg_request_thr = 0.95
        try:
            self.htg_request_thr = config.pop("htg_request_thr")
        except KeyError:
            self.htg_request_thr = 0.95
        try:
            self.oat_name = config.pop("oat_name")
        except KeyError:
            self.oat_name = 'TOutDryBul'
        try:
            self.occupancy_name = config.pop("occupancy_name")
        except KeyError:
            self.occupancy_name = 'occ'

        self.sat_sp = {}
        self.clg_signal = {}
        self.sat = {}
        self.rated_clg_flow = {}
        self.device_list = []
        self.control = None
        self.validate(measurements, config)
        #self.device_clg_req = {}
        self.max_chw_bounds = np.linspace(10, 6.67, 100)
        self.oat_bounds = np.linspace(oat_low, oat_high, 100)

    def validate(self, measurements, config):
        self.control = config.pop('control')
        self.device_list = list(config.keys())
        self.device_clg_req = dict.fromkeys(self.device_list, False)
        for device, device_info in config.items():
            for name, point in device_info.items():
                #if point not in measurements:
                #    print("DAT RESET cannot be implemented check configuration mapping! -- {}".format(point))
                if name == "cooling_signal":
                    self.clg_signal[device] = point
                elif name == "supply_temperature_setpoint":
                    self.sat_sp[device] = point
                elif name == "supply_temperature":
                    self.sat[device] = point
                elif name == "rated_clg_flow":
                    self.rated_clg_flow[device] = point

    def generate_clg_requests(self, device_name, clg_signal, sat, sat_sp):
        clg_requests = 0
        if sat - sat_sp > self.request2:
            clg_requests = 3
        elif sat - sat_sp > self.request1:
            clg_requests = 2
        elif clg_signal > self.clg_request_thr:
            clg_requests = 1
            self.device_clg_req[device_name] = True
        elif self.device_clg_req[device_name] and clg_signal > self.clg_request_thr - 0.1:
            clg_requests = 1
        else:
            self.device_clg_req[device_name] = False
        return clg_requests

    def check_requests(self, measurements, zt=None):
        clg_requests = 0
        for device in self.device_list:
            clg_temp = 0
            sat = measurements[self.sat[device]]
            sat_sp = measurements[self.sat_sp[device]]
            clg_signal = measurements[self.clg_signal[device]]
            if self.rated_clg_flow[device]:
                clg_signal = clg_signal/self.rated_clg_flow[device]
            else:
                clg_signal = 0.0

            print("name: {} - device {} -- occ {} -- max_sp: {} -- sat: {} -- sat_sp: {} -- clg: {}".format(self.name, device, self.occupancy, self.max_sp, sat, sat_sp, clg_signal))
            clg_temp = self.generate_clg_requests(device, clg_signal, sat, sat_sp)
            print("AHU: {} -- requests: {}".format(device, clg_temp))
            clg_requests += clg_temp
        _requests = clg_requests
        print("total requests: {}".format(_requests))
        return _requests

    def update(self, measurements):
        oat = measurements[self.oat_name]
        self.occupancy = int(measurements[self.occupancy_name])
        self.max_sp = np.interp(oat, self.oat_bounds, self.max_chw_bounds)