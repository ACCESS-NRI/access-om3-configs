#!/usr/bin/env python3
# Copyright 2023 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

# Contact: Ezhilsabareesh Kannadasan
# To run:
#   python generate_xml_datm.py <year_first> <year_last>
# To generate IAF xml file, set year_first and year_last to the forcing period
# To generate RYF xml file, set year_first==year_last

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import sys

if len(sys.argv) != 3:
    print("Usage: python generate_xml_drof.py year_first year_last year_align")
    sys.exit(1)

try:
    year_first = int(sys.argv[1])
    year_last = int(sys.argv[2])
except ValueError:
    print("Year values must be integers")
    sys.exit(1)

year_align = year_first

# Create the root element
root = Element("file", id="stream", version="2.0")

# Define the stream info names and corresponding var names
stream_info_data = [
    ("rof.iaf_jra", "friver", "Forr_rofl"),
    ("rof.iaf_jra", "licalvf", "Forr_rofi"),
]

# Generate stream info elements with changing years
for stream_name, var_prefix, var_suffix in stream_info_data:
    stream_info = SubElement(root, "stream_info", name=stream_name)
    if year_first == year_last:
        SubElement(stream_info, "taxmode").text = "cycle"
    else:
        SubElement(stream_info, "taxmode").text = "limit"
    SubElement(stream_info, "tintalgo").text = "upper"
    SubElement(stream_info, "readmode").text = "single"
    SubElement(stream_info, "mapalgo").text = "bilinear"
    SubElement(stream_info, "dtlimit").text = "3.0"
    SubElement(stream_info, "year_first").text = str(year_first)
    SubElement(stream_info, "year_last").text = str(year_last)
    SubElement(stream_info, "year_align").text = str(year_align)
    SubElement(stream_info, "vectors").text = "null"
    SubElement(stream_info, "meshfile").text = "./input/JRA55do-ESMFmesh.nc"
    SubElement(stream_info, "lev_dimname").text = "null"

    datafiles = SubElement(stream_info, "datafiles")
    datavars = SubElement(stream_info, "datavars")
    SubElement(
        stream_info, "offset"
    ).text = "-43200"  # shift backwards from noon to midnight to match RYF

    var_element = SubElement(datavars, "var")
    var_element.text = f"{var_prefix} {var_suffix}"

    for year in range(year_first, year_last + 1):
        if year_first == year_last:
            file_element = SubElement(datafiles, "file")
            file_element.text = f"./input/RYF.{var_prefix}.{year+90}_{year + 90 + 1}.nc"
        else:
            file_element = SubElement(datafiles, "file")
            if var_prefix == "friver":
                if year != 2019:
                    file_element.text = f"./input/land/day/{var_prefix}/gr/v20190429/friver_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_{year}0101-{year}1231.nc"
                else:
                    file_element.text = f"./input/land/day/{var_prefix}/gr/v20190429/friver_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_{year}0101-{year}0105.nc"
            else:
                if year != 2019:
                    file_element.text = f"./input/landIce/day/{var_prefix}/gr/v20190429/licalvf_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_{year}0101-{year}1231.nc"
                else:
                    file_element.text = f"./input/landIce/day/{var_prefix}/gr/v20190429/licalvf_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_{year}0101-{year}0105.nc"

# Convert the XML to a nicely formatted string
xml_str = minidom.parseString(tostring(root)).toprettyxml(indent="  ")

# Write the XML content to a file
with open("drof.streams.xml", "w") as xml_file:
    xml_file.write(xml_str)
