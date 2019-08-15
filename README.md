# DFRUN
### gadget for dl experiments

##### What it does:

1. create a folder to copy all the code in the current directory to freeze one training process
2. switch to the working path to the folder created, and run the command

##### Dependencies:

​	Code is tested on python 3.4 and it's supposed to run in python 3 environment.

##### Install:

```python
pip install dfrun
```

or clone this repository and run:

```
python setup.py install
```



##### Usage:

```python
dfrun -d [experiment folder] -n [experiment name] [command]
```

##### What does the project folder look like:

Proj

   |__ [CODE FILES]

   |__ .dfignore (contains the files/folders ignored in the copy process)

   |__ Experiment Folder (--exp-dir -d)

​                         |__ Experiment Name (--exp-name -n)

​                         |                     |__ [CODE FILES COPIED]

​                         | Other Exp Names....                        

##### Contact: 

mayeoliver@163.com