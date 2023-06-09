# BNRQ (Basic Nuke Render Queue)


## Description
Basic Nuke Render Queue (BNRQ) is a side coding project developed by Andrew Owen that aims to provide a simple
render queue for Foundry Nuke. It is run outside of Nuke so there is no need to launch nuke to use the
application. The code is open for anyone to see for not only clarity purposes but hopefully learning
purposes as well. 

## Content Description
Assets: *A folder that contains any image, video, or audio assets for the project*
<br>BNRQ Builds : *The build folders for each exe build. See the bottom of [Notes](https://github.com/Andr3w0w3n/BNRQ#notes) for detailed information on each of the builds*
<br>HelperScripts : *Folder that contains any scripts used to help development*
<br>CodecLookup.py : *This is a simple class that is one massive dictionary for easy codec lookup and translation*
<br>ErrorCodes.py : *This is a class that makes it easier to access and read any error codes*
<br>FourCharacter-Codes.json : *A list of the character codes that the code references* 
<br>LaunchSplashScreen.py : *This class launches the splash screen in a separate thread*
<br>LICENSE : *The license for BNRQ*
<br>MainWindowTab.py : *This is the class that holds the code for the Main Window Tab. This includes functionality and look*
<br>PreferencesTab.py : *This is the class that holds the code for the Preferences Tab. This includes functionality and look*
<br>RenderQ.py : *This is the class that holds the main function and launches the pyside application*
<br>RenderScript.py : *This is a python script built for the program to run in Nuke. It opens a designated project and renders it.
<br>		&#9;Returning an exit code that the program may use to display errors if any occur.*
<br>RenderScriptList.py : *This python script renders the scripts all in 1 instance of nuke*
<br>SeparateBootupThread.py : *This script is unused but was originally to be used for booting up the program in a separate thread*
<br>SeparateThread.py: *This script houses all the methods that are used in a separate thread for easier access*
<br>Settings.py : *This is the class that runs and manages settings for the pyside application.*
<br>setup.py : *This is for construction of the executable. It is used to make the .spec file*
<br>SplashScreen.py : *a class script that makes the splash screen*

<br>

## Installation
The application is available as an executable located in the Builds folder on the project's github. Clone the github repository
to have access to the application. Different builds will be stored in different folders inside the builds folder, so you can choose the build that you
would like to run. **As of build v1.0, you can move the executable file to any location you deem fit and the program will still work.**
You do not need the .spec file associated with the build for the executable to run. 
This is for anyone that would like to use the spec file to build the code again.

<br>

## Use
The Basic Nuke Render Queue (BNRQ) will hopefully be as easy to use as its own name implies. Allowing easy to read pages and basic functionality for a nuke render queue.
Designed to allow you to work on multiple projects without wasting time rendering. Then, at the end of the day, adding all those projects to the queue and hitting render.

<br>

### Main Page

![MainPage](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/MainPage.png)

To the top left you have the Preferences button and the Help button. These buttons bring you to the settings page and this ReadMe respectively. 
<br>In the center of the application you have the section where the list of files to be rendered will be displayed.
<br>On the right you have buttons to navigate and do basic modifications to this list. 
<br>Below the buttons you have a list of details about the selected file. While you can select multiple files, no more than the first file selected will show the details in this section.

<br>

![RenderList](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/RenderList.png)

This list will show the files that have been added to it, in order that they have been added. It is also the list referenced for rendering and will be rendered in the order on the list.

<br>

![ListButtons](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/ListButtons.png)

The buttons to the right of list are *+*, *-*, *Render*, and *Clear*. 
<br>The *+* button prompts a file selector where you can select any .nk file to add to the list. 
<br>The *-* button removes any file(s) that you have selected.
<br>The *Render* button begins rendering all the files in the list. 
<br>The *Clear* button will clear the entire list of any projects.

<br>

![Descriptions](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/FileDescriptions.png)

File descriptions provide basic information on the selected file. As previously mentioned, if multiple files are selected, only the first file selected will show up in the details section.
The details can change depending on the information available. The detail section will also show prompts if there are no write nodes found in the nuke script. 

<br>

### Preferences

![Preferences](https://github.com/Andr3w0w3n/BNRQ/blob/main/Assets/ReadMe/PreferencesDialog.png)

The Preferences dialog will show up when the Preferences button on the main page is clicked. You cannot do any actions on the main page until you have closed the dialog.

**Nuke Executable Path** is the setting of what nuke executable is used for rendering. This path can be entered manually in the text editor. It can also be entered via a visual path finder by clicking the buton *File Explorer*.
The button *Find Nuke* will search through the path C:/ProgramFiles/ for the nuke exectuable with the latest version. When BNRQ boots up for the first time, this action will be performed automatically.
If no nuke executable is found, this section will appear blank. A very small black box will appear (bug, it is supposed to be a loading gif), this is the program loading, please do not click anything while doing so as it may backup the program.
<br>**File Search Start** is a setting that allows you to select the start point for all file searches (including the folder searches for settings). This can be changed manually in the text editor. it can also be changed via clicking
the *File Explorer* button and selecting the folder you want to start at.
<br>**Write Node Name** is the name of the write node that BNRQ will look for to render out of. This is for the fact that nuke scripts can have multiple write nodes. This setting allows you to change the name to the name of the write node
that you want nuke to render out of. You can change the write node name by manually entering the name in the text editor. **THIS NAME IS CASE SENSITIVE**
<br>**Full Path Filenames** is a checkbox where you can either have the entire filepath of the nuke scripts in the list displayed, or you can have just the project name displayed. Checking the box turns on the full paths labeling.
Unchecking the box turns the labels to just the project names
<br>**Render without closing Nuke (Beta)** is a checkbox that enables/disables the closing of nuke for each script rendered. When enabled, nuke will open in only 1 instance, making the rendering faster. the downside is the error handling is 
not as robust as rendering with a new instance each time (at this point in time). So any errors with the files may not be handled correctly. This will not corrupt any renders or the sort, but BNRQ itself may behave strangely or crash is errors
were to happen during the render process.

The *Save* Button is required to be clicked to save any changes. It will be available to be clicked once any changes to the settings are made, even if you change them back to what they originally were. If you were to close the 
Preferences dialog without saving, no settings will be saved and they will be set back to their previous values.
<br>The *Cancel* button discards all non-saved changes without closing the Preferences dialog.
<br>the *Delete Save File* button will delete the save file from where the program references it currently. The save file will be re-created if the settings are saved again. Deleting the save file resets all settings to default for next launch.
The settings file will get re-created on next launch.

A prompt will appear when the user has made changes that have not been saved.

## Notes 

### Build v1.0
- The *Render* button does not provide any additional prompts or confirmation and will just begin rendering. You can click cancel on the progress bar to terminate rendering.<br>
             However, it will always render the script that it is currently rendering to completion before cancelling any further renders.
- The *Clear* button will prompt the user if they would like to continue clearing the list of nuke scripts only if the number of files exceeds 5. 
- Details of a project will only give information of the project that is available. Only details beyond basic ones are Codec for mov's.
- All file searches will start at where **File Search Start** is selected to start. It is not dynamic or keeps memory of previous locations.
- There is no way to specify different write node names for different projects yet.
- Any saved settings will **not** be saved for next launch of the application, and any files listed in the render list will **not** be saved.
- There is no "Reset to default" functionality for settings.
- There is no prompt to ask the user if they would like to close settings without the changed settings being saved.
- The program may not respond occasionally while the files are being rendered. This is normal behavior.

### Build v2.0
- Added single nuke instance rendering functionality, this creatly improves render times (In Beta, will not be able to handle every render error).
- Added Splash Screen. The splash screen will display loading information when the program launches without any save information. To show the user the program is doing something behind the scenes.
- Added delete save file button. This button removes the save files for BNRQ until a new save file is created.
- Added slight cancel functionality (can cancel when scripts are first loading, still cannot cancel while rendering is happening)


## Library references
### PySide
This application uses [PySide2](https://pypi.org/project/PySide2/) with no modifications to it. 

### Pyinstaller
This application was packaged using [pyinstaller](https://pyinstaller.org/en/stable/installation.html) with no modifications to it. It was also not packaged with the application.

