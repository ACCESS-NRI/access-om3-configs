#!/usr/bin/env bash
set -euo pipefail

# Submit/run this DICE case with the current prerelease payu without modifying
# the installed module. PAYU_PATH points the queued job at local payu entrypoints
# that add the missing "dice" component metadata in memory.

case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${case_dir}"

module use /g/data/vk83/prerelease/modules
module load payu

export PAYU_PATH="${case_dir}/payu-dice-bin"

exe="$(
    python3 - <<'PY'
from pathlib import Path
import re

match = re.search(r"^\s*exe:\s*(\S+)", Path("config.yaml").read_text(), re.M)
print(match.group(1) if match else "")
PY
)"

if [[ "${exe}" == *CICE6* ]]; then
    cat >&2 <<EOF
Refusing to submit: config.yaml has exe: ${exe}

This executable links the CICE cap at build time, so ICE_model=dice will still
start CICE and fail looking for ice_in. Use/build an ACCESS-OM3 executable whose
configuration includes WW3 but does not include CICE6, for example:

  access-om3-WW3
  access-om3-MOM6-WW3

Then update config.yaml exe and rerun setup/run.
EOF
    exit 1
fi

payu run "$@"
