# BNRQ
Basic Nuke Render Queue


Description:
	Basic Nuke Render Queue is a side coding project developed by Andrew Owen that aims to provide a simple
	render queue for Foundry Nuke. It is run outside of nuke so there is no need to launch nuke to use the
	application. The code is open for anyone to see for not only clarity purposes but hopefully learning
	purposes as well. 

	
	Brief file descriptions:
		RenderQ.py is the application script

		RenderScript.py is the script that the application loads with nuke on renders to actually render the files.

		setup.py is for executable creation (using pyinstaller).

Installation:
	The application is the RenderQ.exe located in the dist folder on the project's github. Clone the github repository
	to have access to the application. You can move the executable file to any location you deem fit and the program 
	will still work. 


	The render queue will boot up a console, this is where nuke will be used. The initial bootup may take a second
	as the software is finding where the latest version of nuke is on your machine. 
		Unfortunatly at the moment, there is no settings save file so this process will need to happen every time
		you relaunch the application. You may change the version of nuke the software uses in the preferences tab
		by selecting the version of nuke that you want to use executable in the finder or typing out its path.
	
