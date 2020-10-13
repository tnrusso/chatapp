# CS490 Project 2 Milestone 1

# Description
Project 2 is a web application created using Flask, HTML, CSS, React, SQLAlchemy (PostgreSQL), and Socket.IO. It is a chatroom application similiar to Google Hangouts, WhatsApp, and Slack, along with a chatbot that will respond to user inputted commands. It is deployed on Heroku and can be found [here](https://project2-m1-tnr24.herokuapp.com/)

# Overview
[Installation](#installation)

[Built With](#built-with)

[Project Status](#project-status)

# Installation

### 0. Clone the project
```bash
cd ~/environment && git clone https://github.com/NJIT-CS490/project2-m1-tnr24 && cd project2-m1-tnr24
```
### 1. Install React packages
- If you're not already in project directory `cd project2-m1-tnr24`
- In your terminal, type:
```
npm install
pip install flask-socketio
pip install eventlet
npm install -g webpack
npm install --save-dev webpack
npm install socket.io-client --save
```

### 2. Get PSQL to work with Python
- To update yum (enter 'yes' to all promps) `sudo yum update`

- To upgrade Pip `sudo /usr/local/bin/pip install --upgrade pip`

- To install psycopg2 `sudo /usr/local/bin/pip install psycopg2-binary`

- To install SQLAlchemy `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`


### 3. Set up PSQL
- Install PostGreSQL `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`

- Initialize PSQL database `sudo service postgresql initdb`

- Start PSQL: `sudo service postgresql start`

- Create new superuser `sudo -u postgres createuser --superuser $USER`

- Create new database `sudo -u postgres createdb $USER`

### 4. Create a new user
- Open PSQL in terminal `psql`

- Create user - fill in brackets with your username/password (Save these somewhere!) `create user [USERNAME] superuser password '[PASSWORD]';`

- Exit out of PSQL `\q`
- Create a new file called `sql.env` in the project directory
- Inside `sql.env`, enter `DATABASE_URL='postgresql://[USERNAME]:[PASSWORD]@localhost/postgres'` where [USERNAME] and [PASSWORD] are the same values used to create your user, and save these changes

### 5. Enable read/write from SQLAlchemy
- Open the file in your terminal by typing `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
- Type `:%s/ident/md5/g` This will replace all values of 'ident' with 'md5' in the file
- Restart PSQL to enable these changes `sudo service postgresql restart`

### 6. Setting up the database
- Open the Python interactive shell `python`
- Once inside your shell, type 
```bash
import models
models.db.create_all()
models.db.session.commit()
exit()
```

### 7. Running the app on Cloud9
- Start PSQL `sudo service postgresql start`
- Open 2 terminals and `cd project2-m1-tnr24` in both
- In one terminal, type `npm run watch` and `python app.py` in the other
- Click 'Preview' --> 'Preview Running Application' to view the app

### 8. Deploy to Heroku
- Sign up for a Heroku account on their website [https://www.heroku.com/](https://www.heroku.com/)

- In the project directory in your terminal, create a new Heroku app `npm install -g heroku`
- Login to your Heroku account `heroku login -i`
- Create a new Heroku app `heroku create`
- Set up the database
```
heroku addons:create heroku-postgresql:hobby-dev
heroku pg:wait
PGUSER=[USERNAME] heroku pg:push postgres DATABASE_URL
--> (IF THIS DOES NOT WORK): heroku pg:push postgres DATABASE_URL
heroku pg:psql
select * from users;
select * from chatlog;
\q
```
- Push to Heroku `git push heroku master`

- Go to your [dashboard](https://dashboard.heroku.com/apps) on Heroku's website and click on your new app, and then click the 'Open App' button.

- If you ever want to reset the database, click on your application, and then go to `Configure Add-ons` --> `Heroku Postgres` --> `Settings` --> `Reset Database`
# Built with
[Flask](https://palletsprojects.com/p/flask/)

[HTML](https://www.w3schools.com/html/)

[CSS](https://www.w3schools.com/css/)

[React](https://reactjs.org/docs/getting-started.html)

[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

[Flask-Socket.IO](https://flask-socketio.readthedocs.io/en/latest/)

[PostGreSQL](https://www.postgresql.org/)


Deployed on [Heroku](https://www.heroku.com/)

# Project Status
### Technical Issues and how they were solved
1. When setting a count state in React that would update when a user connected or disconnected, the app couldn't differentiate users and therefore could not track how many users were connected to the chat (how many clients are opened). This was fixed by setting a global variable in `app.py` to count how many times a client connects and disconnects and emitting the value to the client rather than updating a count state in React. 
2. In order to differentiate messages from a normal user and the chatbot, the message for each list item in `UnorderList.jsx` was set to have conditional statements to determine if the message being displayed was from the bot or a normal user. The conditional result determines the class name assigned to the message, and therefore which styling to follow from `style.css`
3. If the length of a message was longer than the set length allowed in the Chatlog model (1000), the message would not be added to the database and not be displayed. This was fixed by setting a limit on how many characters can be inputted into the input text box, and incase the chatbot returned a translation longer than 1000 characters, it will now send a message saying the translation message, and therefore the text to be translated, is too long. 
4. If the message text was longer than the width of the chatbox div, it would extend out of the list item and the text would continue outside of the chatbot rather than making a new line to display the text. This was fixed by displaying the text in paragraph tags `<p></p>` and setting each chat message to `word-wrap:break-word;` in CSS. This will make the text go to the next line if the message is too long for one line.


### Known Problems and Possible Improvements
1. Currently the chat will display all messages saved into the database, which could be a problem if the chat was to get filled with hundreds of messages. A fix would be to set a limit on how many messages to display at once, and as the user scrolls up in the chat, a button/message will display with the option to display older messages if clicked. 
2. A user has no limit on how many messages they can send in a set amount of time, meaning users are allowed to send hundreds of messages per minute if they can. A possible fix for this would be to set a limit on how many messages a user can send within a given time, and if the limit it hit, the user will be "muted" and be unable to send messages for a set amount of time. 
3. A new list that can display the names of the users currently connected to the chat can be implemented by creating a new useState in React. The state will hold an array of names and would update as users connect and/or disconnect, similar to how the number of connected of users is being tracked. The div that will hold the list 
 of usernames could be set to be next to the chat with a button that will show/hide users in the chat when clicked. 
