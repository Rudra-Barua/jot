## Project Title: Jot
## By: Rudra Barua
Course: CS50 @ Harvard

Assignment: Final Project

Contact: rudrabarua@college.harvard.edu

## Description:
Jot is a web application that makes it convenient for users to write some notes that pertain to the content of a specific website. They can simply use this web app to open a link to website and jot down their notes. The web app also allows for users to create tasks or reminders for themselves for a specific website.
Users will also have access to these collections of notes to organize them as a single session. This is perfect for the person with hundreds of tabs open or someone who just wants to jot quick/short notes without having to tab through sites.

## Key Features:

1. Pull up the website alonside the note taking area
2. Change the website while taking notes  
3. View all the notes taken on a specific website as notebook
4. Create todo lists with tasks, specific websites, and due dates 
5. View all the todos grouped by their respective sites

## Details of Implementation:
The Python framework Flask was used to create this web application.
One of the main reasons I choose to use Flask was because I would get to use the powerful tools and libraries I am already familiar with in Python.
Flask also allowed me to constantly build and deploy. This was especially helpful when I was coming across bug after bug. Quickly deployment allowed for quick debugging.
Flask is also works very well with the Jinja2 framework template which I heavily used through the project. 
Overall the framework allowed me to go fast and experiment without much worry.

## Breakdown of Files:  

1. So lets start with our database jot.db. It consists of three tables:

a. users: the users table keeps track of all the user's ids, users, and hashed passwords

b. history: the history tables has columns to keep track of the user id that created the note, the date/time of when the note was taken, the text of the note itself,
whether or not the note has been deleted (in case of future implementation of recovering trashed notes), 
the url of the website being noted on, and the unique id for the record itself

c. todos: the todo table has columns to keep track of the user id that created the todo, the text of the todo, the url of the site, the date/time of the due date, 
completion of the todo (not implement but kept in case), if the todo was delete or not, and a unique id for the todo itself

2. The static folder just contains the favicon, the app's logo, and css file
3. The templates folder contains all the HTML of each of the pages, the index, apology page, and the layout
4. helpers.py was adapted from the CS50 Finance PSET, to implement features such as login and creating unique apology pages 
5. requirements.txt is there to ensure the correct libraries are being installed
6. Finally, the application.py is keeping everything running by handling the operations of the app from taking in user input and putting it into the SQL DB
and back from the SQL DB to the UI.
