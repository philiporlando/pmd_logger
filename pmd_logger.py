# Created by Philip Orlando
# Sustainable Atmospheres Research Lab, Portland State University
# Dr. Linda George
# 2018-04-03
# Description:
# Data logging script written for use with Measurement Computing PMD-1208FS
# The script converts from digital value, to original analog signal, and ultimately to a measurement concentration

# source dependencies
from __future__ import print_function
from mcculw import ul
from mcculw.enums import ULRange
from mcculw.ul import ULError
import time, os, csv, datetime
#import pylab
import pandas as pd

# print current working directory to console
print("Current working dir: %s" % os.getcwd())

##### Specify PMD settings: #####
################################################################################
board_num = 0 # Board Number assigned by InstaCal configuration
ai_range = ULRange.BIP5VOLTS # Set analog input range (usually 0-5V)
channel = 0 # Set the channel number (see PMD-1208FS manual for pinout)
fullscale = 5.0 # specific to each instrument (DustTrak is set to 5V)
upper_limit = 1000.0 # max instrument reading at fullscale (DustTrak is set to 1 mg/m3)
time_resolution = 1 # time resolution in seconds
################################################################################

## Create an empty dataframe for logging our PMD data:
df = pd.DataFrame(columns=['datetime'
                           ,'conc'
                           ,'bit_value'
                           ,'volts'
						   ])

## Determine filename based on the date:
t_start = time.time()
start_day = datetime.datetime.fromtimestamp(t_start).strftime("%Y-%m-%d")
print("Date: " + str(start_day))
file_name = str(start_day) + "_pmd_output.txt"
dir_name = "pmd_data"
full_path =  os.getcwd() + "\\" + dir_name
print("Writing output file to: %s" % full_path)

## Create a new directory for output data if it doesn't exist
if not os.path.isdir(full_path):
	os.mkdir(full_path)

## change to this directory
os.chdir(full_path)

## index for our dataframe / dictionary
row = 0

# define a simple averaging function for later use
def avg(x):
	average = sum(x)/len(x)
	return(average)


print("########################## LOG START ##########################")


## infinite loop
while True:

    # re-assign the current_day variable during each loop
    current_day = datetime.datetime.fromtimestamp(t_start).strftime("%Y-%m-%d")
    file_name = str(current_day) + "_pmd_output.txt"

    ## Append to exisitng file or write to a new file per day:
    if os.path.isfile(file_name):
    	f = open(file_name, 'a')
    	print("Appending to existing file: " + file_name)
    else:
    	f = open(file_name, 'w')
    	print("Writing to new file: " +  file_name)


	# determines averaging window based on time resolution
	t_end = time.time() + time_resolution

	# sample loops until time resolution is met
	while time.time() < t_end:

		ts = time.time()

		# store live values into an empty list
		bit_values = []
		eng_units_values = []
		conc_values = []

		# convert from analog to digital value
		bit_value = ul.a_in(board_num
	                        ,channel
	                        ,ai_range
	                        )

		# append to our list
		bit_values.append(bit_value)

		# convert from digital back to analog
		eng_units_value = ul.to_eng_units(board_num
	                                          ,ai_range
	                                          ,bit_value
	                                          )
		# append to its list
		eng_units_values.append(eng_units_value)

		# determine our concentration value based on the V_reference, V_fullscale, and our upper detection limit at fullscale
		conc_value = (eng_units_value/fullscale)*upper_limit

		# append these to our list
		conc_values.append(conc_value)

		# force system to sleep for a millisecond
		time.sleep(.001)

	# calculate averages for each parameter throughout the sampling window
	bit_avg = avg(bit_values)
	eng_avg = avg(eng_units_values)
	conc_avg = avg(conc_values)

	# append each averaged value to our dataframe
	df.loc[row] = pd.Series(
                dict(
                        datetime = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                        ,conc = conc_avg
			,bit_value = bit_avg
                        ,volts = eng_avg
                        )
                )

	# print each row of our dataframe to console
	print(df.loc[[row]]) ## If you add extra [] around 'counter' the console will print in wide format instead of long format! I still haven't figured out how to get ride of those pesky headers though...

	# increment our dataframe index (row number)
	row += 1

	# append each row to our output file
	df.to_csv(file_name
                  ,sep = ','
                  ,index = False
                  ,encoding = 'utf-8'
				  )
