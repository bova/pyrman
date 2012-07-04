#!/bin/bash
# Main file for pybackup execution

export PYBKP_HOME=/home/oracle/pybkp
export PYTHONPATH=$PYBKP_HOME/classes:$PYBKP_HOME/pyrman:$PYTHONPATH

# check availability of configuration file's variable
if [ -n $1 ]
    then
        python $PYBKP_HOME/pyrman/pybkp.py $1
else
    echo "Usage: $0 {pybkp_conf_file}"
fi
