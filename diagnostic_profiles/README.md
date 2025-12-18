### Preset `diag_table` files for MOM6 diagnostic requests

The `diag_table_<preset>` files in this directory are generated from the corresponding 
`diag_table_source/diag_table_<preset>_source.yaml` files using the `make_diag_table.py` script.
To create and use a custom diag_table:

1. Copy a `diag_table_<preset>_source.yaml` file to a new file named `diag_table_source.yaml`
2. Make the required modifications to the new `diag_table_source.yaml`
3. In the directory containing your new `diag_table_source.yaml` file, run:
   ```
   module use /g/data/vk83/modules
   module load payu
   python /g/data/vk83/apps/make_diag_table/make_diag_table.py
   ```
   This will produce a new diagnostic table `diag_table` based on `diag_table_source.yaml`.
5. Place the new `diag_table` file in the `diagnostic_profiles` directory, and provide an informative name.
6. Modify the `<control_directory>/diag_table` symlink to point to the new diagnostic table.
