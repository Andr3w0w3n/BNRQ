# BNRQ (Basic Nuke Render Queue)


## Description
Basic Nuke Render Queue (BNRQ) is a side coding project developed by Andrew Owen that aims to provide a simple
render queue for Foundry Nuke. It is run outside of Nuke so there is no need to launch nuke to use the
application. The code is open for anyone to see for not only clarity purposes but hopefully learning
purposes as well. 

## Content Description
RenderQueue Builds : *The build folders for each exe build. See installation for information on each of the builds*

CodecLookup.py : *This is a simple class that is one massive dictionary for easy codec lookup and translation*

LICENSE : *The license for BNRQ*

MainWindowTab.py : *This is the class that holds the code for the Main Window Tab. This includes functionality and look*

PreferencesTab.py : *This is the class that holds the code for the Preferences Tab. This includes functionality and look*

RenderQ.py : *This is the class that holds the main function and launches the pyside application*

RenderScript.py : *This is a python script built for the program to run in Nuke. It opens a designated project and renders it.
		Returning an exit code that the program may use to display errors if any occur.*
		
Settings.py : *This is the class that runs and manages settings for the pyside application.*
	***Note***:*Settings are not saved in an file, so the application basically only has temporary settings at the moment*

setup.py : *This is for construction of the executable. It is used to make the .spec file*

## Installation
The application is available as an executable located in the Builds folder on the project's github. Clone the github repository
to have access to the application. Different builds will be stored in different folders so you can choose the build that you
would like to run. **You can move the executable file to any location you deem fit and the program will still work.**
You do not need the .spec file associated with the build for the executable to run. 
This is for anyone that would like to use the spec file to build.

	
## Use
The Basic Nuke Render Queue (BNRQ) will hopefully be as easy to use as its own name implies. 

### Main Page

![MainPage](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/MainPage.png)

To the top left you have the Preferences button and the Help button. These buttons bring you to the settings page and this ReadMe respectively. 
\nIn the center of the application you have the section where the list of files to be rendered will be displayed.
\nOn the right you have buttons to navigate and do basic modifications to this list. 
\nBelow the buttons you have a list of details about the selected file. While you can select multiple files, no more than the first file selected will show the details in this section.

![RenderList](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/RenderList.png)

This list will show the files that have been added to it, in order that they have been added. It is also the list referenced for rendering and will be rendered in the order on the list.

![](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/ListButtons.png)

The buttons to the right of list are *+*, *-*, *Render*, and *Clear*. The *+* button prompts a file selector where you can select any .nk file to add to the list. The *-* button removes any file(s) that you have selected.
The *Render* button begins rendering all the files in the list. The *Clear* button will clear the entire list of any projects.



###Notes Build v1.0***
- The *Render* button does not provide any additional prompts or confirmation and will just begin rendering. You can click cancel on the progress bar to terminate rendering.\n
      However, it will always render the script that it is currently rendering to completion before cancelling any further renders.
- The *Clear* button will prompt the user if they would like to clear the list of nuke scripts only if the number of files exceeds 5. 


## Library references
### PySide
This application uses [PySide2](https://pypi.org/project/PySide2/) with no modifications to it. 

### Pyinstaller
This application was packaged using [pyinstaller](https://pyinstaller.org/en/stable/installation.html) with no modifications to it. It was also not packaged with the application.

