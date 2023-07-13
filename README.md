# pyswitches
A test project to create network based switch configs.

 ![License-MIT](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

  # Title: Pyswitch configurator

  ![Text-Editor](./images/configurator.jpg)
  
  # This is a work in progress!
  
  ## Description: This Project is a python based app that uses pyqt5 for a GUI and is used for creating network based switch configs, in an interactive way.

  ## Usage:  To use the app, the user must have the template they desire for the switch model they want to use in the templates folder, the user then executes the pyswitch.py and a GUI will load. From here the user is presented with two options 1: Fill out the feilds and click generate single config, or 2: click batch mode. If the user wants to create a single config, The user will select the template, fill in the blanks and hit generate single config. When the user clicks generate single config, a popup will appear and tell them the name of the file and where it was saved.(in the output folder with a .txt of the hostname) If using batch mode, the user will be asked to select a .csv file(an example is in the repo) the .csv file will have all the info for the batch of configs. The app will then generate them and place them in the output folder.

  ## Questions: johndesgarennes@gmail.com

  ## Github username: jdesgarennes

  ## https://github.com/jdesgarennes/pyswitch

 # Features to add: 
 ## I want to eventually add an option to make the app interactive with a INFOBLOX API, this will allow it to take or find available IP's on the network and even add A records for easy DNS managment. 

  ## License type: MIT

