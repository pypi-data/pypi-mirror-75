# Installation
### Setting the Path
After setting up a repo on your computer from GitHub, you should then export the repo to your python path. In your .bashrc (or similar), add something along the lines of:

```
export PYTHONPATH="/home/user/path/to/repo/MEDIS:$PYTHONPATH"
```

### The Conda Environment
As of yet, a (mostly) untested .yaml file of a conda environment can be found medis2.yml. Information on how to set up a conda environment from a .yml file can be found here: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file

```
$conda env create -f medis2.yml
```

This will create an environment called medis (which you could change by editing the first line of the .yml file to be whatever you want). When you are done, activate the environment with

`$conda activate medis`
or 
`$conda activate your_name`

The version here may change as the code continues to be tested. If you notice that a package is missing while testing MEDIS, please contact user:KristinaDavis. Once we are confident the .yml contains all relevant info, we can try to make this a pip editable install, that will be updated through github.

### Setting IDE to Use the Conda Environment
Depending on which IDE you use to run Python, there are different methods to ensure that you use the medis environment when you run the code. If you open python from the command line and run everything in the terminal (or base-python PyPy) this is as simple as running 
`$ conda activate medis`
before running 
`$ python`
However, if you are using a more sophisticated IDE, you may need to link the env to the project settings. For example, in PyCharm, you can create a MEDIS project to contain all the medis code. You then need to go into the project settings, and set Project Interpreter to */path/to/anaconda3/envs/medis/bin/python3.6*. PyCharm then automatically uses the version of numpy, scipy, etc located in the same env folder. 

### Installing PROPER
You will also have to install PROPER separately. First download from https://sourceforge.net/projects/proper-library/files/ and after activating the environment run

```
python setup.py install --prefix=/path/to/anaconda3/envs/medis/lib/python3.6/site-packages/
````


### Setting the Save Directory
To change the location of the saved data for the simulation run, edit the iop params at the top of the run_telescope.py file you are starting. For example, from run_SCExAO.py, put the following somewhere in the configuration part of the file:

testname = 'SCExAO-DM-test'
iop.update_datadir(f"/home/captainkay/mazinlab/MKIDSim/CDIsim_data/")
iop.update_testname(testname)
iop.makedir()


# Documentation
The documentation for `MEDIS` can be found at https://medis.readthedocs.io
