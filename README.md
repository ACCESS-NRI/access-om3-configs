# CESM GMOM_JRA payu configuration
CESM GMOM_JRA (MOM6-CICE6-DATM-DROF-SLND-SWAV-SGLC) payu configuration. By default, this configuration will advance 1 month per model run.

Note, this is an untested porting (to payu) of an untested CESM configuration. You're welcome to use this, but do so at your own risk. Note also that no effort has (yet) been put into optimising the PE layout of this configuration on Gadi - currently each model component simply runs sequentially and is allocated an entire node.
