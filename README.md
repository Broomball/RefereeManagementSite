# BroomballBogaloo
The Broomball Bogaloo

# Setup
Install python3 and pip3 using your operating system's installer, then navigate to the 
directory containing the files and run '''pip3 install -r ./requirements.txt'''
Follow Directions in DBsetup.txt to set up MySQL Database

# Run
To use and run this program, run '''python3 pages.py''' from the directory containing 
the project.


# Website Layout
MAIN Landing page (a login prompt) 
	after logging in, it will go to the schedule on the current day
	the front page will always be a login screen

they do not want game schedule on here
	Users/refs going here instead of official schedule 

permission levels: Base, Ref, ref supervisor, committee, head ref
Each catagory shows what pages that user will be able to access
Also shows what notifications they will be recieving and how 


Base
	BASE		User Page
	Emails: Approved
	Popups: None

Ref Pages 
	REF			Schedule 
	REF			2 Weeks Form 
	REF			Swap Shifts Form
	REF			Open Shifts Page
	BASE		User Page
	
	Popups: Canceled Shift, Shift Changes, 2 Week form due within 5 days
	Emails: Change to Schedule 

Supervisor 
	REF			Schedule 
	REF			2 Weeks Form 
	REF			Swap Shifts Form
	REF 		Open Shifts Page
	BASE		User Page
	SUPER		Ranking Page (only submit)
	
	Popups: Canceled Shift, Shift Changes, 2 Week form due within 5 days
	Emails: Change to Schedule, Rankings to do 

Chairs  
	REF			Schedule  
	BASE		User Page
	COMMITTEE	Site Wide Settings 
	COMMITTEE	Ranking Page (see per user, supervisor, date, etc...)
	COMMITTEE	Aprove User (Give ref #)
	HEAD REF 	ALL
	
	Popups: Approve User
	Emails: Approve User

Head Ref
	REF			Schedule 
	HEAD REF	Approve Rankings
		automate email
	HEAD REF	Approve Shift Swap
		AUtomate email
	COMMITTEE	Ranking Page (View)
	SUPER		Ranking Page (Submit)
	BASE		User Page

	Popups: Approve Rankings, Approve Shifts
	Emails: Approve Rankings, Approve Shifts

Admin
	Everything

	Popups: None
	Emails: None
