#!/usr/bin/env bash
set -euo pipefail

# Temporary workaround for payu versions whose ACCESS-OM3 component table does
# not yet include CDEPS DICE. The control and work runconfigs are restored to
# ICE_model=dice before this script exits successfully.

case_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${case_dir}"

runconfig="nuopc.runconfig"
backup="${runconfig}.payu-dice.bak"

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
Refusing to setup: config.yaml has exe: ${exe}

This executable links the CICE cap at build time, so ICE_model=dice will still
start CICE and fail looking for ice_in. Use/build an ACCESS-OM3 executable whose
configuration includes WW3 but does not include CICE6, for example:

  access-om3-WW3
  access-om3-MOM6-WW3

Then update config.yaml exe and rerun setup.
EOF
    exit 1
fi

replace_ice_model() {
    local file="$1"
    local model="$2"

    python3 - "$file" "$model" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
model = sys.argv[2]
text = path.read_text()
new, count = re.subn(r"(^\s*ICE_model\s*=\s*)\S+", rf"\1{model}", text, count=1, flags=re.M)
if count != 1:
    raise SystemExit(f"Could not find exactly one ICE_model entry in {path}")
path.write_text(new)
PY
}

restore_control() {
    if [[ -f "${backup}" ]]; then
        mv "${backup}" "${runconfig}"
    fi
}

trap restore_control EXIT

if [[ -f "${backup}" ]]; then
    echo "Refusing to overwrite existing backup: ${backup}" >&2
    exit 1
fi

cp "${runconfig}" "${backup}"
replace_ice_model "${runconfig}" cice

module use /g/data/vk83/prerelease/modules
module load payu

payu sweep
payu setup "$@"

restore_control
trap - EXIT

work_dir="work"
if [[ -L "${work_dir}" ]]; then
    work_dir="$(readlink "${work_dir}")"
fi

if [[ ! -d "${work_dir}" ]]; then
    echo "payu setup completed, but work directory was not found" >&2
    exit 1
fi

replace_ice_model "${work_dir}/${runconfig}" dice
cp dice_in dice.streams.xml "${work_dir}/"

echo "payu setup completed with DICE restored in control and work runconfigs."
