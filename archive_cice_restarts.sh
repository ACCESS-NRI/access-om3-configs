#!/bin/bash
# clean up cice_restarts.sh

if [ -f archive/output*/GMOM_JRA.cice.r.* ] 
then
rm archive/output*/GMOM_JRA.cice.r.*
fi

if [ -f archive/output*/input/iced.1900-01-01-10800.nc ] 
then
rm archive/output*/input/iced.1900-01-01-10800.nc
fi