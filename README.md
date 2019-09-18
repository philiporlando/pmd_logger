# pmd_logger

## Description

Data logging script for Measurement Computing PMD-1208FS. It was designed to capture analog outputs from a variety of air quality instruments for the [Sustainable Atmospheres Research Lab](https://star.research.pdx.edu/).
The digital value from the PMD is converted back to the original analog signal.
This analog signal can then be converted into a measurement concentration from a variety of federal reference methods.
The script samples on the order of milliseconds, and aggregates based on the `time_resolution` variable. 

## Instructions

This script is dependent on Measurement Computing's InstaCal software to assign a board number to the PMD. 
After configuring the board number in InstaCal, change the hard-coded `board_num` variable accordingly. 
Be sure to assign the correct `fullscale` and `upper_limit` parameters depending on the instrument you are measuring from. 


