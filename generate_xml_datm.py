# Copyright 2023 ACCESS-NRI and contributors. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: Apache-2.0

# Contact: Ezhilsabareesh Kannadasan
# To run:
#   python generate_xml_datm.py <year_first> <year_last> 
# if year_first == year_last, then RYF xml file will be generated,
# otherwise IAF xml file will be generated

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import sys

if len(sys.argv) != 3:
    print("Usage: python script_name.py year_first year_last")
    sys.exit(1)

try:
    year_first = int(sys.argv[1])
    year_last = int(sys.argv[2])
except ValueError:
    print("Year values must be integers")
    sys.exit(1)

# Create the root element
root = Element("file", id="stream", version="2.0")

# Define the stream info names and corresponding var names
stream_info_names = [
    "CORE_IAF_JRA55do.PRSN",
    "CORE_IAF_JRA55do.PRRN",
    "CORE_IAF_JRA55do.LWDN",
    "CORE_IAF_JRA55do.SWDN",
    "CORE_IAF_JRA55do.Q_10",
    "CORE_IAF_JRA55do.SLP_10",
    "CORE_IAF_JRA55do.T_10",
    "CORE_IAF_JRA55do.U_10",
    "CORE_IAF_JRA55do.V_10",
]

var_names = {
    "CORE_IAF_JRA55do.PRSN": ("prsn", "Faxa_prsn"),
    "CORE_IAF_JRA55do.PRRN": ("prra", "Faxa_prrn"),
    "CORE_IAF_JRA55do.LWDN": ("rlds", "Faxa_lwdn"),
    "CORE_IAF_JRA55do.SWDN": ("rsds", "Faxa_swdn"),
    "CORE_IAF_JRA55do.Q_10": ("huss", "Sa_shum"),
    "CORE_IAF_JRA55do.SLP_10": ("psl", "Sa_pslv"),
    "CORE_IAF_JRA55do.T_10": ("tas", "Sa_tbot"),
    "CORE_IAF_JRA55do.U_10": ("uas", "Sa_u"),
    "CORE_IAF_JRA55do.V_10": ("vas", "Sa_v"),
}

# Generate stream info elements with changing years
for stream_name in stream_info_names:
    stream_info = SubElement(root, "stream_info", name=stream_name)
    SubElement(stream_info, "taxmode").text = "cycle"
    SubElement(stream_info, "readmode").text = "single"
    SubElement(stream_info, "mapalgo").text = "bilinear"
    SubElement(stream_info, "dtlimit").text = "1.5"
    SubElement(stream_info, "year_first").text = str(year_first)
    SubElement(stream_info, "year_last").text = str(year_last)
    SubElement(stream_info, "year_align").text = "1"
    SubElement(stream_info, "vectors").text = "null"
    SubElement(stream_info, "meshfile").text = "./input/JRA55do-ESMFmesh.nc"
    SubElement(stream_info, "lev_dimname").text = "null"

    datafiles = SubElement(stream_info, "datafiles")
    datavars = SubElement(stream_info, "datavars")
    
    if stream_name not in ["CORE_IAF_JRA55do.SLP_10","CORE_IAF_JRA55do.T_10","CORE_IAF_JRA55do.Q_10", "CORE_IAF_JRA55do.U_10","CORE_IAF_JRA55do.V_10"]:
     SubElement(stream_info, "offset").text = "0" 
    else:
     SubElement(stream_info, "offset").text = "5400" #an offset of 5400 is required since the day starts at 00:00hrs

    var_name_parts = var_names.get(stream_name, (stream_name.split('.')[-1].lower(), f"Faxa_{stream_name.split('.')[-1].lower()}"))
    var_element = SubElement(datavars, "var")
    var_element.text = f"{var_name_parts[0]}  {var_name_parts[1]}"

    if stream_name == "CORE_IAF_JRA55do.SWDN":
        SubElement(stream_info, "tintalgo").text = "coszen"
    else:
        SubElement(stream_info, "tintalgo").text = "linear"
    
 
    for year in range(year_first, year_last + 1):

        if year_first == year_last:
            file_element = SubElement(datafiles, "file")
            file_element.text = f"./input/RYF.{var_name_parts[0]}.{year+90}_{year + 90 + 1}.nc"
        else:
            file_element = SubElement(datafiles, "file")
            if stream_name not in ["CORE_IAF_JRA55do.SLP_10","CORE_IAF_JRA55do.T_10","CORE_IAF_JRA55do.Q_10", "CORE_IAF_JRA55do.U_10","CORE_IAF_JRA55do.V_10"]:
                if year != 2019: 
                    file_element.text = f"./input/atmos/3hr/{var_name_parts[0]}/gr/v20190429/{var_name_parts[0]}_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_{year}01010130-{year}12312230.nc"
                else:
                    file_element.text = f"./input/atmos/3hr/{var_name_parts[0]}/gr/v20190429/{var_name_parts[0]}_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_{year}01010130-{year}01052230.nc"
            else:
                if year != 2019:
                    file_element.text = f"./input/atmos/3hrPt/{var_name_parts[0]}/gr/v20190429/{var_name_parts[0]}_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_{year}01010000-{year}12312100.nc"
                else:
                    file_element.text = f"./input/atmos/3hrPt/{var_name_parts[0]}/gr/v20190429/{var_name_parts[0]}_input4MIPs_atmosphericState_OMIP_MRI-JRA55-do-1-4-0_gr_{year}01010000-{year}01052100.nc"


# Convert the XML to a nicely formatted string
xml_str = minidom.parseString(tostring(root)).toprettyxml(indent="  ")

# Write the XML content to a file
with open("datm.streams.xml", "w") as xml_file:
    xml_file.write(xml_str)
