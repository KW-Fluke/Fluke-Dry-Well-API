# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 15:21:10 2020

@author: Kevin Williamson
        <kevin.williamson@flukecal.com>
        Fluke Calibration
        
Creates an active graph that may be continuously updated 
Plots the following information with time as the x-axis:
        Plot 1
            - Set Point Temperature in °C
            - Measured Temperature in °C
        Plot 2
            - Measured Ramp Speed in Kelvin/minute
        Plot 3 
            - Measured Stability in Kelvin 

This software is not supported by Fluke. Users are welcome to clone this 
repository for their own use.

This program has only been tested with Windows 10 and a Fluke 9173 dry well. 
Users with a variety of connected COM ports and/or a different operating 
system, should adjust the __init__ function for their circumstances. 

------------------------------------------------------------------------------
Copyright 2020 Fluke
Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to deal 
in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
------------------------------------------------------------------------------

Dependencies:
- python            3.7.7
- pyserial          3.4
- vs2015_runtime    14.16.27012      
- dpython-dateutil  2.8.1
- matplotlib        3.1.3
 
"""

from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from dry_well_API import dry_well

# Asking user for input data, makes sure set points are above 24 and below 700
set_points = None
while set_points == None:
    print('Please enter dry well temperature set points in order.\n' +
          'Use commas to seperate values. Only allows Temperatures between ' + 
          '24°C and 700°C.\n' +
          'Or just press "Enter" to read the script in the same directory.')
    set_points = input()
    if set_points == '':
        set_points = []
        break
    set_points = list(map(float,set_points.split(',')))
    if (min(set_points) < 24) or (max(set_points) > 700):
        set_points = None
        print('\nPlease enter values between 24°C and 700°C.\n')
# Requires that there are a matching number of soak times as there are set points
soak_times = []
while len(set_points) != len(soak_times):
    print('\nPlease enter soak times in minutes for each set point in order.\n' +
          'Use commas to seperate values. There are ' + str(len(set_points)) + 
          ' set points.')
    soak_times = list(map(float,input().split(',')))
# Requires that user enters the correct number of ramp speeds
ramp_speeds = []
while len(set_points) != len(ramp_speeds):
    print('\nPlease enter dry well ramp speeds to each set point in order.\n' +
          'Use commas to seperate values. There are ' + str(len(set_points)) + 
          ' set points.')
    ramp_speeds = list(map(float,input().split(',')))

# Requires user to enter Y or N
end_point = None
while (end_point != 'Y') and (end_point != 'N'): 
    print('\nWould you like the dry well to remain at the final set point?\n' +
          'If no, the dry well will return to 25°C. [Y\\N]')
    end_point = input().upper()
# Translates the end status to true or false. The default if not Y is to return to 25°C
if end_point == 'Y':
    end_point = True
else:
    end_point = False

if not len(ramp_speeds):
    import csv
    with open(r'temp_profile.txt', mode='r') as temp_profile:
        reader = csv.reader(temp_profile, delimiter=',')
        next(reader)
        for row in reader:
            if len(row):
                set_points.append(float(row[0]))
                soak_times.append(float(row[1]))
                ramp_speeds.append(float(row[2]))

# Creating the dry_well object! This should automatically check serial connections.
fluke9173 = dry_well()
# Setting the heating element to active
fluke9173.set_output(1)
# Generating data log
fluke9173.create_data()
fluke9173.update_data()
fluke9173.update_data()

# Creating first plot of temperature over time
fig1 = plt.figure(figsize=(4,3),dpi=150)
ax1 = fig1.add_subplot(3,1,1)
temp_line, = ax1.plot(fluke9173.t, fluke9173.temperature, 'r.', 
                      label='Measured Temperature')
target_line, = ax1.plot(fluke9173.t, fluke9173.target, 'b--', 
                        label='Control Set Point')
ax1.set_xlim(fluke9173.t[0] - timedelta(seconds=30),
             fluke9173.t[-1] + timedelta(seconds=30))
ax1.legend()
ax1.set_title("Dry Well Temperature")
ax1.set_ylabel("Temperature [°C]")

# Creating second plot of ramp speed over time
ax2 = fig1.add_subplot(3,1,2)
ramp_line, = ax2.plot(fluke9173.t, fluke9173.ramp, 'k.',label='Measured Ramp Speed')
ax2.set_xlim(fluke9173.t[0] - timedelta(seconds=30),
             fluke9173.t[-1] + timedelta(seconds=30))
ax2.set_ylabel("Ramp Speed [°C\\min]")

# Creating third plot of stability over time
ax3 = fig1.add_subplot(3,1,3)
stability_line, = ax3.plot(fluke9173.t, fluke9173.stability, 'k.',
                           label='Measured Stabilty')
ax3.set_xlim(fluke9173.t[0] - timedelta(seconds=30),
             fluke9173.t[-1] + timedelta(seconds=30))
ax3.set_xlabel("Time (Date then hour)")
ax3.set_ylabel("Measured Stability [K]")
ax3.set_ylim( 0, 1 )


def update_graph():
    fluke9173.update_data()
    temp_line.set_xdata(fluke9173.t)
    temp_line.set_ydata(fluke9173.temperature)
    target_line.set_xdata(fluke9173.t)
    target_line.set_ydata(fluke9173.target)
    ramp_line.set_xdata(fluke9173.t)
    ramp_line.set_ydata(fluke9173.ramp)
    stability_line.set_xdata(fluke9173.t)
    stability_line.set_ydata(fluke9173.stability)
    ax1.set_xlim(fluke9173.t[0] - timedelta(seconds=30),
                 fluke9173.t[-1] + timedelta(seconds=30))
    ax1.set_ylim(round(min(fluke9173.temperature) - 1),
                 round(max(fluke9173.temperature) + 1))
    ax2.set_xlim(fluke9173.t[0] - timedelta(seconds=30),
                 fluke9173.t[-1] + timedelta(seconds=30))
    ax2.set_ylim(round(min(fluke9173.ramp) - 1),
                 round(max(fluke9173.ramp) + 1))
    ax3.set_xlim(fluke9173.t[0] - timedelta(seconds=30),
                 fluke9173.t[-1] + timedelta(seconds=30))

    try:
        plt.draw()
        plt.pause(1)
    except:
        print("Error updateing graph.")
        print("Time points: " + str(len(fluke9173.t)))
        print("Targ points: " + str(len(fluke9173.target)))
        print("Temp points: " + str(len(fluke9173.temperature)))
        print("Ramp points: " + str(len(fluke9173.ramp)))
        print("Stab points: " + str(len(fluke9173.stability)))

fluke9173.create_data()    
# 1 Sets temperature and ramp speed
# 2 Logic plots data until stability is reached at set point
# 3 Logic plots data until soak time is reached finished
for i in range(len(set_points)):
    fluke9173.set_temp(set_points[i])
    fluke9173.set_rate(ramp_speeds[i])
    while not fluke9173.read_stability_status():
        update_graph()
    run_start = datetime.now()
    run_length = timedelta(0)
    run_time = timedelta(minutes=soak_times[i])
    while run_length < run_time:
        update_graph()
        run_length = datetime.now() - run_start

# If the dry well is not supposed to stay at the end point, it returns to 25°C
if not end_point:
    fluke9173.set_temp(25)
    fluke9173.set_rate(10)
    fluke9173.set_output(0)

# Optionally saves graph
save = None
while (save != 'Y') and (save != 'N'): 
    print('\nWould you like to save the graph?\n' +
          '[Y\\N]')
    save = input().upper()

# Translates the save status to true or false.
if save == 'N':
    print("Not saving the graph.")
else:
    plt.savefig(str(fluke9173.t[0])[0:10] + 'dry_well_log.png')

# Optionally saves data
save = None
while (save != 'Y') and (save != 'N'): 
    print('\nWould you like to save the data?\n' +
          '[Y\\N]')
    save = input().upper()
# Translates the save status to true or false.
if save == 'N':
    print("Not saving the data.")
else:
    # Saves the data
    fluke9173.save_data()

# Ends communication with dry well
fluke9173.close()