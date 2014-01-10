#! /usr/bin/env python
# ==========================================================================
# This script converts the background rates in Konrad's performance files
# into a column separated file function table. The table is automatically
# named "bkg_XXX.txt" where "XXX" is for example "kb_E_50h_v3".
#
# Copyright (C) 2011 Jurgen Knodlseder
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ==========================================================================
from gammalib import *
import math
import sys


# ================================= #
# Generate file function from model #
# ================================= #
def make_file_function(irfname, filename):
	"""
	Generate file function from model.
	
	Parameters:
	 irfname  - IRF filename
	 filename - File function filename
	"""
	# Open performance file and file function
	irf  = open(irfname, "r")
	file = open(filename, "w")
	
	# Read data
	for row in irf:
	
		# Skip header and trailer
		if row.find("log(E)") != -1:
			continue
		if row.find("--------") != -1:
			break
			
		# Extract data
		fields = row.replace(" ",",").replace(",,",",").rstrip("\n").split(",")
		logE   = float(fields[0])
		aeff   = float(fields[1])
		r68    = float(fields[2])
		r80    = float(fields[3])
		eres   = float(fields[4])
		bgd    = float(fields[5])
		sens   = float(fields[6])
		
		# Compute energy (in MeV)
		energy = math.pow(10.0, logE)*1.0e6
		emin   = math.pow(10.0, logE-0.1)*1.0e6
		emax   = math.pow(10.0, logE+0.1)*1.0e6
		ewidth = emax-emin
		
		# Compute solid angle of r80 region in sr
		solidangle = 2.0 * math.pi * (1.0 - math.cos(math.radians(r80)))
		
		# Compute background rate per steradian and MeV
		bkg_rate = bgd/solidangle/ewidth

		# Write
		file.write(str(energy)+" "+str(bkg_rate)+"\n")
	
	# Close files
	irf.close()
	file.close()
	
	# Return
	return


# ================ #
# Main entry point #
# ================ #
if __name__ == '__main__':
	"""
	Main entry point
	"""
	# Get IRF from command line argument
	if (len(sys.argv) > 1):
		irf = sys.argv[1]
	else:
		irf = "kb_E_50h_v3"

	# Set parameters
	caldb    = "/usr/local/gamma/share/caldb/cta"
	
	# Set filenames
	irfname  = caldb+"/"+irf+".dat"
	filename = "bkg_"+irf+".txt"
	
	# Read 
	make_file_function(irfname, filename)
