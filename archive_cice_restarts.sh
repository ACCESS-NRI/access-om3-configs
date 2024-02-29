#!/bin/bash
# clean up cice_restarts.sh

if [ -f archive/output*/access-om3.cice.r.* ]
then
rm archive/output*/access-om3.cice.r.*
fi

if [ -f archive/output*/input/iced.1900-01-01-10800.nc ] 
then
rm archive/output*/input/iced.1900-01-01-10800.nc
fi
