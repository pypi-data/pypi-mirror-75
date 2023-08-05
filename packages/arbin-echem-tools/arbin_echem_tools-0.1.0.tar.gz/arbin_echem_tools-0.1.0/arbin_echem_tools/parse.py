import pandas as pd
import pyodbc
import numpy as np
if __name__ == "__main__":
    import matplotlib.pyplot as plt
else:
    import matplotlib
    matplotlib.use('Qt5Agg')
    
import os.path
import tkinter as tk
from tkinter import filedialog
import csv
import re
from pkg_resources import parse_version
import requests
from requests.exceptions import HTTPError
import json
import os

from modules.utils import safeRound, compareVersion, getActiveMass
import modules.errors as errors


class ElectrochemData:
    def __init__(self, discharge_capacity, charge_capacity, power, average_voltage, efficiency, empty=False):
        self.discharge_capacity = discharge_capacity
        self.charge_capacity = charge_capacity
        self.power = power
        self.average_voltage = average_voltage
        self.efficiency = efficiency
        self.empty = empty
    def __repr__(self):
        string = 'discharge_capacity: %s\ncharge capacity: %s\npower: %s\naverage voltage: %s\nefficiency: \
%s\n'%(self.discharge_capacity, self.charge_capacity, self.power, self.average_voltage, self.efficiency)
        return string

class System:
    def __init__(self, mass, echem_df):
        self.mass = mass
        self.echem_df = echem_df
        self.properties = {}
    def addProperty(self, name, value):
        self.properties[name] = value

class ExtractedData:
    def __init__(self, firstCycleData, averageData, voltageRange):
        self.firstCycleData = firstCycleData
        self.averageData = averageData
        self.voltageRange = voltageRange

def read_arbin(source_path, save_path=None, table_name='Channel_Normal_Table'):
    #table_name = 'Channel_Normal_Table'
    # set up some constants
    MDB = source_path
    DRV = '{Microsoft Access Driver (*.mdb)}'
    PWD = 'pw'

    # connect to db
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()
    header_row = []
    for r in cur.columns(table=table_name):
        header_row.append(r.column_name)
        
    # run a query and get the results 
    SQL = 'SELECT * FROM %s;'%(table_name) # your query goes here
    rows = cur.execute(SQL).fetchall()
    rows.insert(0, header_row)
    cur.close()
    con.close()

    if save_path:
        with open(save_path, 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(rows)

# Description: parsed the excel file for Arbin cycler and extracts raw data into a Pandas dataframe
# Charge capacity data for cycle 'i' can be retrieved by:
# partitioned_data[i]['charge']['Charge_Capacity']
# Discharge capacity data for cycle 'i' can be retrieved by: 
# partitioned_data[i]['discharge']['Discharge_Capacity']
# Charge voltage data for cycle 'i' can be retrieved by: partitioned_data[i]['charge']['Voltage']
# Discharge voltage data for cycle 'i' can be retrieved by: partitioned_data[i]['discharge']['Voltage']
def to_dataframe(path, active_mass):
    try:
        extension = os.path.splitext(path)[1]
        if extension == '.csv':
            echem_df = pd.read_csv(path)
        elif extension == '.xls':
            # Read excel file
            echem_df = pd.read_excel(path, sheet_name=1)
            # change column names for excel
            echem_df = echem_df.rename(columns={
                'Current(A)': 'Current', 
                'Charge_Capacity(Ah)': 'Charge_Capacity', 
                'Discharge_Capacity(Ah)': 'Discharge_Capacity',
                'Voltage(V)': 'Voltage',
                'Charge_Energy(Wh)': 'Charge_Energy',
                'Discharge_Energy(Wh)': 'Discharge_Energy',
                'dV/dt(V/s)': 'dV/dt',
                'Internal_Resistance(Ohm)': 'Internal_Resistance',
                'AC_Impedance(Ohm)': 'AC_Impedance',
                'ACI_Phase_Angle(Deg)': 'ACI_Phase_Angle',
                })
        echem_df = echem_df.sort_values(by=['Data_Point'])
        # Convert capacities into mAh/g
        echem_df['Charge_Capacity'] = echem_df['Charge_Capacity']*1000*1000/active_mass
        echem_df['Discharge_Capacity'] = echem_df['Discharge_Capacity']*1000*1000/active_mass
        # Parse data
        maxIndex = echem_df['Cycle_Index'].iloc[-1]
        partitioned_data = []
        for i in range(1, maxIndex+1):
            # Split data by Cycle Index
            df = echem_df[echem_df['Cycle_Index'] == i]
            # Remove soaking data
            df = df[df['Step_Index'] != 1] 
            # Remove tail data
            df = df[df['Step_Index'] != 4] 
            # Split data by charge
            charge_df = df[df['Current'] >= 0]
            # Split data by discharge
            discharge_df = df[df['Current'] < 0] 
            # Add data to list as a dictionary specifying charge/discharge  
            partitioned_data.append({'charge':charge_df, 'discharge':discharge_df})
    except OSError:
        raise errors.rawDataError()
    return partitioned_data

# Description: calculates electrochemical data on the first charge/ discharge curve.
def extract_single_cycle_properties(charge_voltage_data, charge_capacity_data,
    discharge_voltage_data, discharge_capacity_data):
    echemData = ElectrochemData(None, None, None, None, None, empty=True)
    if not discharge_capacity_data.empty:
        discharge_capacity = discharge_capacity_data.iloc[-1]
        power = np.trapz(discharge_voltage_data, discharge_capacity_data, dx=0.01)
        average_voltage = power/discharge_capacity
        if not charge_capacity_data.empty:
            charge_capacity = charge_capacity_data.iloc[-1]
            efficiency = discharge_capacity/charge_capacity*100
        else:
            charge_capacity = None
            efficiency = None
        echemData = ElectrochemData(discharge_capacity, charge_capacity, power, average_voltage, efficiency)
    return echemData

# Description: extracts the cycling voltage range
def extract_voltage_range(charge_voltage_data, discharge_voltage_data):
    if not charge_voltage_data.empty and not discharge_voltage_data.empty:
        min = discharge_voltage_data.iloc[-1]
        max = charge_voltage_data.iloc[-1]
    else:
        min = 'n/a'
        max = 'n/a'
    return [min, max]

def extract_properties(partitioned_data):
    avg_voltage = []
    avg_discharge_cap = []
    avg_charge_cap = []
    avg_power = []
    first_data = None
    # Calculate single curve echem data for each cycle, then average out
    for i in range(len(partitioned_data)):
        charge_capacity_data = partitioned_data[i]['charge']['Charge_Capacity']
        charge_voltage_data = partitioned_data[i]['charge']['Voltage']
        discharge_capacity_data = partitioned_data[i]['discharge']['Discharge_Capacity']
        discharge_voltage_data = partitioned_data[i]['discharge']['Voltage']
        data = extract_single_cycle_properties(charge_voltage_data, charge_capacity_data,
        discharge_voltage_data, discharge_capacity_data)
        if not data.empty:
            avg_voltage.append(data.average_voltage)
            avg_discharge_cap.append(data.discharge_capacity)
            avg_charge_cap.append(data.charge_capacity)
            avg_power.append(data.power)
        if i == 0:
            first_data = data
    avg_efficiency = np.mean(avg_discharge_cap)/np.mean(avg_charge_cap)*100
    voltage_range = extract_voltage_range(partitioned_data[0]['charge']['Voltage'],
    partitioned_data[0]['discharge']['Voltage'])
    avg_data = ElectrochemData(np.mean(avg_discharge_cap), np.mean(avg_charge_cap), np.mean(avg_power), 
    np.mean(avg_voltage), avg_efficiency)
    if __name__ == "__main__":
        print('\nArbin excel file data parsed successfully!\n')
        print('--------------------------------------------------------------------')
        print('***Data for first charge and discharge: ***')
        print('Charge Capacity [mAh/g]: %s'%(safeRound(first_data.charge_capacity,2)))
        print('Discharge Capacity [mAh/g]: %s'%(safeRound(first_data.discharge_capacity,2)))
        print('Average Discharge Voltage [V]: %s'%(safeRound(first_data.average_voltage,2)))
        print('Discharge Power [Wh/kg]: %s'%(safeRound(first_data.power,2)))
        print('Coulombic Efficiency: %s%%'%(safeRound(first_data.efficiency,4)))
        print('--------------------------------------------------------------------')
        print('***Average Electrochemical Data: ***')
        print('Charge Capacity [mAh/g]: %s'%(safeRound(avg_data.charge_capacity,2)))
        print('Discharge Capacity [mAh/g]: %s'%(safeRound(avg_data.discharge_capacity,2)))
        print('Average Discharge Voltage [V]: %s'%(safeRound(avg_data.average_voltage,2)))
        print('Discharge Power [Wh/kg]: %s'%(safeRound(avg_data.power,2)))
        print('Coulombic Efficiency: %s%%'%(safeRound(avg_data.efficiency,4)))
        print('--------------------------------------------------------------------')
    return ExtractedData(first_data, avg_data, voltage_range)

def plot_CV(partitioned_data, figurePath, system, cycleList, show=True):
    plt.rcParams.update({'font.size': 25})
    plt.rcParams.update({'font.family':'Arial'})
    plt.figure(figsize=(8,6))
    plt.gcf().subplots_adjust(bottom=0.15)
    fsize = 25  
    if not __name__ == "__main__":
        return
    ax = plt.gca()
    # For each cycle, plot both charge and discharge curves with the same color
    for index in cycleList:
        if index < len(partitioned_data) and index >= 0:
            x1_data = partitioned_data[index]['charge']['Charge_Capacity']
            y1_data = partitioned_data[index]['charge']['Voltage']
            x2_data = partitioned_data[index]['discharge']['Discharge_Capacity']
            y2_data = partitioned_data[index]['discharge']['Voltage']
            color = next(ax._get_lines.prop_cycler)['color']
            plt.plot(x1_data, y1_data, '-', color=color,  linewidth=4, label='Cycle %s'%(index))
            plt.plot(x2_data, y2_data, '-', color=color, linewidth=4)
    plt.xlabel('Capacity [mAh/g]', fontsize=fsize)
    plt.ylabel('Voltage [V]', fontsize=fsize)
    #plt.title('Cycling Data for ' + system)
    #plt.title('Cycling Data for ' + 'Cathode A')
    plt.legend().set_draggable(True)
    # Save matplotlib figure as png
    try:
        if figurePath:
            plt.savefig(figurePath + system + '.png')
            if __name__ == "__main__":
                print('Plot saved to ', figurePath + system + '.png')
                print('--------------------------------------------------------------------')
    except PermissionError:
        raise errors.figurePermissionError
    if __name__ == "__main__":
        if show:
            plt.show()

def create_summary(dataSystem, tablePath):
    return

def generate_summary(system, tablePath, firstCycleData=None, averageData=None, voltageRange=None, mass=None, 
    ratio=None, rate=None, cellType=None, anode=None, comments=None):
    try:
        with open(tablePath + '/' + system + '.csv', mode='w', newline='') as csvfile:
            if not tablePath:
                return
            dec = 3
            if isinstance(voltageRange[0], float):
                range = [safeRound(voltageRange[0], dec), safeRound(voltageRange[1], dec)]
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Sample', system])
            csv_writer.writerow(['Cathode Mass [mg]', mass])
            csv_writer.writerow(['Active: C: Binder', ratio])
            csv_writer.writerow(['Cycling Rate', rate])
            csv_writer.writerow(['Voltage Range [V]', str(range[0]) + '-' + str(range[1])])
            csv_writer.writerow(['Avg. Charge Cap. [mAh/g]', safeRound(averageData.charge_capacity, dec)])
            csv_writer.writerow(['Avg. Discharge Cap. [mAh/g]', safeRound(averageData.discharge_capacity, dec)])
            csv_writer.writerow(['Avg. Voltage [V]', safeRound(averageData.average_voltage, dec)])
            csv_writer.writerow(['Avg. Power [Wh/kg]',safeRound(averageData.power, dec)])
            csv_writer.writerow(['Avg. Coulombic Efficiency',str(safeRound(averageData.efficiency, dec))+'%'])
            csv_writer.writerow(['First Charge Cap. [mAh/g]',safeRound(firstCycleData.charge_capacity, dec)])
            csv_writer.writerow(['First Discharge Cap. [mAh/g]',safeRound(firstCycleData.discharge_capacity,dec)])
            csv_writer.writerow(['First Discharge Volt. [V]',safeRound(firstCycleData.average_voltage, dec)])
            csv_writer.writerow(['First Discharge Power [Wh/kg]',safeRound(firstCycleData.power, dec)])
            csv_writer.writerow(['First Discharge Efficiency',str(safeRound(firstCycleData.efficiency, dec))+'%'])
            csv_writer.writerow(['Cell Type', cellType])
            csv_writer.writerow(['Anode Material', anode])
            csv_writer.writerow(['Comments', comments])
            if __name__ == "__main__":
                print('Successfully saved data table!')
            return 1
    except PermissionError:
        raise errors.tablePermissionError
            
        

# Description: main function 
def runTasks(filepath, choosefile, figurePath, tablePath, cycleList, mass, 
    ACBratio, rate, cellType, anode, comments):
    # Get system name
    filename = os.path.splitext(os.path.basename(filepath))[0]
    system = filename.replace('.xls', '').replace('VW-', '')
    # Get path
    if choosefile:
        # Prompt File Selection
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename()
    else:
        path = filepath
    extension = os.path.splitext(filepath)[1]
    if extension == '.res':
        read_arbin(path, 'data.csv', 'Channel_Normal_Table')
        path = 'data.csv'
    elif extension == '.csv' or '.xls':
        pass
    # Get active mass
    activeMass = getActiveMass(mass, ACBratio)
    # Parse data from excel file
    partitioned_data = to_dataframe(path, activeMass)
    # Extract electrochem data
    extractedData = extract_properties(partitioned_data)
    # Generate CSV summary file
    generate_summary(system, tablePath, extractedData.firstCycleData, extractedData.averageData, 
    extractedData.voltageRange, mass, ACBratio, rate, cellType, anode, comments)
    # Plot data
    plot_CV(partitioned_data, figurePath, system, cycleList)

if __name__ == "__main__":
    runTasks(
        filepath = 'd:/Clement Research/Electrochem/VW-PVMnMn-B01-S01-E1.xls', # the name of you raw excel file
        choosefile = False, # whether or not to choose your file directly (will ignore filepath, filename if true)
        figurePath = 'd:/Clement Research/Electrochem/Figures/', # the directory to save your plot in
        tablePath = 'd:/Clement Research/Electrochem/Summaries/', # the directory to save your table in
        cycleList = range(30),
        mass = 18.8, # mass of entire cathode (do not multiply by active mass ratio)
        ACBratio = '70:20:10', # active:carbon:binder ratio
        rate = 'C/20', # rate
        cellType = 'Swagelok', # cell type
        anode = 'Na', # anode material
        comments = None # comments
        )
