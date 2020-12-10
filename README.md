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

## Tools:
This web application was created using Python, Flask, HTML/CSS, JavaScript, and SQL

## Project Video:


## Implementation:
(Initial steps can be skipped in using CS50 IDE)
1. Install Python
2. Install pip
3. Install virtualenv
4. Download the project
5. Open the terminal and change the directory such that it is where the main project folder is
6. pip install -r requirements.txt  (On the CS50 IDE, I think I only had to get Beautiful Soup and )
7. flask run (This is all that is needed in the CS50 IDE)
8. The web app is now good to go and use

## Basic User Guide:
The web app will look pretty empty at first, but the user needs to go write some notes. First, when the user goes to "Write," the web page has Wikipedia's main page
displayed. This web app does a great job displaying static webpages like wikipedias and YouTube videos (embedded links only), however it will not work with pages that are
always refresing (like Amazon or Facebook). 

Now, paste in a link (wikipedia pages work nice) next to the green "Update" button and click "Update". You can repeat this to visit other sites. 

In order to take notes, just type in the text field to the right of the page and click the blue "Note" button. Congratulation! You have taken your first note.

Now, you can either continue to add more notes for this page or paste in another link to go to a new page and take notes for it.

Now, to see your notes, just click on "Notebooks" and you will see thumbnails of all the sites you have taken notes on (It can take a hot second though because of Beautiful Soup). Click on the thumbail and you will a popup of all the notes and an option to delete them all. 

For the sake of convenience, the web app will remember the last website you took notes on and automatically fill in after each note or session.

Finally, by clicking on "Todos" you will be taken to a todo list where you input a task, the website it needs to be done on, and any date of matter to it. Then, by pressing add, the task will be added and categorized on the site it was for. If there are multiple task for a site, it will make it so the tasks are underneath the url of the website. These can also be easily deleted or completed by clicking on the closing buttons. Similarly, for the sake of convenience, the web app will remember the last website you wrote a task on and automatically fill in after a task is submitted.
