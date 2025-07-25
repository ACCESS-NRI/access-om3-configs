#!/usr/bin/bash

logfile='resubmit.log'
counterfile='resubmit.count'
outfile='access-om3.err'

MAX_RESUBMISSIONS=3
date >> ${logfile}

# Define errors from which a resubmit is appropriate
declare -a errors=(
                   "Segmentation fault: address not mapped to object"
                   "Segmentation fault: invalid permissions for mapped object"
                   "Transport retry count exceeded"
                   "atmosphere/input.nml"
                   "ORTE has lost communication with a remote daemon"
                   "MPI_ERRORS_ARE_FATAL"
		  )

resub=false
for error in "${errors[@]}"
do
  if grep -q "${error}" ${outfile}
  then
     echo "Error found: ${error}" >> ${logfile}
     resub=true
     break
  else
     echo "Error not found: ${error}" >> ${logfile}
  fi
done

if ! ${resub}
then
  echo "Error not eligible for resubmission" >> ${logfile}
  exit 0
fi

if [ -f "${counterfile}" ]
then
  PAYU_N_RESUB=$(cat ${counterfile})
else
  echo "Reset resubmission counter" >> ${logfile}
  PAYU_N_RESUB=${MAX_RESUBMISSIONS}
fi

echo "Resubmission counter: ${PAYU_N_RESUB}" >> ${logfile}

if [[ "${PAYU_N_RESUB}" -gt 0 ]]
then
  # Sweep and re-run
  ${PAYU_PATH}/payu sweep >> ${logfile}
  ${PAYU_PATH}/payu run -n ${PAYU_N_RUNS} >> ${logfile}
  # Decrement resub counter and save to counter file
  ((PAYU_N_RESUB=PAYU_N_RESUB-1))
  echo "${PAYU_N_RESUB}" > ${counterfile}
else
  echo "Resubmit limit reached ... " >> ${logfile}
  rm ${counterfile}
fi

echo "" >> ${logfile}
