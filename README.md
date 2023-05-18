# BNRQ (Basic Nuke Render Queue)


## Description
Basic Nuke Render Queue (BNRQ) is a side coding project developed by Andrew Owen that aims to provide a simple
render queue for Foundry Nuke. It is run outside of Nuke so there is no need to launch nuke to use the
application. The code is open for anyone to see for not only clarity purposes but hopefully learning
purposes as well. 

## Content Description
RenderQueue Builds : *The build folders for each exe build. See installation for information on each of the builds*
- Build0.1
- Build0.2

CodecLookup.py : *This is a simple class that is one massive dictionary for easy codec lookup and translation*

LICENSE : *The license for BNRQ*

MainWindowTab.py : *This is the class that holds the code for the Main Window Tab. This includes functionality and look*

PreferencesTab.py : *This is the class that holds the code for the Preferences Tab. This includes functionality and look*

RenderQ.py : *This is the class that holds the main function and launches the pyqt application*

RenderScript.py : *This is a python script built for the program to run in Nuke. It opens a designated project and renders it.
		Returning an exit code that the program may use to display errors if any occur.*
		
Settings.py : *This is the class that runs and manages settings for the pyqt application.*
	***Note***:*Settings are not saved in an file, so the application basically only has temporary settings at the moment*

setup.py : *This is for construction of the executable. It is used to make the .spec file*

## Installation
The application is available as an executable located in the Builds folder on the project's github. Clone the github repository
to have access to the application. Different builds will be stored in different folders so you can choose the build that you
would like to run. **You can move the executable file to any location you deem fit and the program will still work.**
You do not need the .spec file associated with the build for the executable to run. 
This is for anyone that would like to use the spec file to build.

***Build0.1***: This is a very early version of the render queue. Its rendering capacity is limited and is as bare functional as you 
	can get.

***Build0.2***: This is a more functional version of the render queue. The rendering is done by a built in script and is more controllable.
	There are also more errors caught and more information displayed for the user. 
	
## Use


## Licensing references
### PyQt License

This application uses PyQt, which is licensed under the GNU General Public License (GPL) or a commercial license. 
Please refer to the [PyQt License](https://riverbankcomputing.com/software/pyqt/license) for more details.

