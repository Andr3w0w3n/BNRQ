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

![ListButtons](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/ListButtons.png)

The buttons to the right of list are *+*, *-*, *Render*, and *Clear*. The *+* button prompts a file selector where you can select any .nk file to add to the list. The *-* button removes any file(s) that you have selected.
The *Render* button begins rendering all the files in the list. The *Clear* button will clear the entire list of any projects.

![Descriptions](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/FileDescriptions.png)

File descriptions provide basic information on the selected file. As previously mentioned, if multiple files are selected, only the first file selected will show up in the details section.
The details can change depending on the information available. The detail section will also show prompts if there are no write nodes found in the nuke script. 

###Preferences

![Preferences](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/PreferencesDialog.png)

The Preferences dialog will show up when the Preferences button on the main page is clicked. You cannot do any actions on the main page until you have closed the dialog.

**Nuke Executable Path** is the setting of what nuke executable is used for rendering. This path can be entered manually in the text editor. It can also be entered via a visual path finder by clicking the buton *File Explorer*.
The button *Find Nuke* will search through the path C:/ProgramFiles/ for the nuke exectuable with the latest version. When BNRQ boots up for the first time, this action will be performed automatically.
If no nuke executable is found, this section will appear blank.
\n**File Search Start** is a setting that allows you to select the start point for all file searches (including the folder searches for settings). This can be changed manually in the text editor. it can also be changed via clicking
the *File Explorer* button and selecting the folder you want to start at.
\n**Write Node Name** is the name of the write node that BNRQ will look for to render out of. This is for the fact that nuke scripts can have multiple write nodes. This setting allows you to change the name to the name of the write node
that you want nuke to render out of. You can change the write node name by manually entering the name in the text editor. **THIS NAME IS CASE SENSITIVE**
\n**Full Path Filenames** is a checkbox where you can either have the entire filepath of the nuke scripts in the list displayed, or you can have just the project name displayed. Checking the box turns on the full paths labeling.
Unchecking the box turns the labels to just the project names

The *Save* Button is required to be clicked to save any changes. It will be available to be clicked once any changes to the settings are made, even if you change them back to what they originally were. If you were to close the 
Preferences dialog without saving, no settings will be saved and they will be set back to their previous values.
\nThe *Cancel* button discards all non-saved changes without closing the Preferences dialog. 

A prompt will appear when the user has made changes that have not been saved.

###Notes Build v1.0\n
- The *Render* button does not provide any additional prompts or confirmation and will just begin rendering. You can click cancel on the progress bar to terminate rendering.\n
      However, it will always render the script that it is currently rendering to completion before cancelling any further renders.
- The *Clear* button will prompt the user if they would like to continue clearing the list of nuke scripts only if the number of files exceeds 5. 
- Details of a project will only give information of the project that is available. Only details beyond basic ones are Codec for mov's.
- All file searches will start at where **File Search Start** is selected to start. It is not dynamic or keeps memory of previous locations.
- There is no way to specify different write node names for different projects yet.
- Any saved settings will be saved for next launch of the application, but any files listed in the render list will **not** be saved.
- There is no "Reset to default" functionality for settings.
- There is no prompt to ask the user if they would like to close settings without being saved.


## Library references
### PySide
This application uses [PySide2](https://pypi.org/project/PySide2/) with no modifications to it. 

### Pyinstaller
This application was packaged using [pyinstaller](https://pyinstaller.org/en/stable/installation.html) with no modifications to it. It was also not packaged with the application.

