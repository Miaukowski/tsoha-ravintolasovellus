A little app for reviewing restaurants, searching for them based on name or associated hashtag, user profile management and such. 
Requires registering/logging in for full "enjoyment". 

# Features that are currently implemented and working:
- A front page with login and register option, and the page also displays The top 5 restaurants as a little "teaser". 
- A login page & a register page. 
- A dashboard, that displays the top 5 restaurants that have been reviewed, as well as their average score. This also comes with an option of clicking a "view information" button.
- A separate "restaurant details" page, this is where the user gets redirected when they click the "view information" button,here the average score, text part of the reviews and hashtags are displayed.
- The dashboard also features an option to review a restaurant(does not matter if it existts or not, the system checks that), giving it a grade from 0-5, writing a little text about the restaurant and also adding hashtags. 
- The dashboard features a search option, where the user search for restaurants by name or hastags (basically the system automatically searches both options).
- The search button takes you to a separate page, that shows the user the search results. This then gives the users information about said restaurant (average score & name ).
- Log out buttons are now everywhere.
- security measures are in place.
- A user profile page, where the user can also remove their profile.
- A better look. 

# Features that need to be implemented:
- Administrator rights and options (censorship)
- Splitting the app.py into more managable chunks. 

# How to try it out: 
1. Make a folder where you'd like to try the app. In that folder create a .env file and define its content as the following: 
```DATABASE_URL=<the adress of the local database>```
```SECRET_KEY=<secret-key>```

2. Open three (separate) terminal windows. Execute the following in the precise order given below.

3. In the first terminal window you go to a folder where you'd like to run the program. Install the python virtual-environment there by inputting the following in the command line: 
```python3 -m venv venv```.
Then input 
```source venv/bin/activate```.
Now you are in the virtual environment (This might actually be useless if you already have admin rights in your computer... anyhow).  Install the required dependecies from the requirements.txt file using the following command line 
```pip install -r requirements.txt```.
No need to close this window, we use it later in (4).  

4. In the second one you open the database with the following command line 
```start-pg.sh```.
Do not do anything else in this terminal window. This is simply for running the database. Do not close this window. 

5. In the second terminal you write $psql, this open the PostgreSQL interpreter. Then you create the tables by writing 
```psql < schema.sql```.
The schema.sql contains all the tables you will need. This window can be closed after creating the tables if you want.

6. Return to the first terminal window, write 
```flask run```.
This should now give you a URL page to visit. Click on that and voilá. Explore.

7. When you feel like you have explored enough, do terminate the database (second terminal window) by ctrl-c, otherwise your computer might become a bit slow after a day or two.

8. You may also close the flask environment in terminal window 1. by ctrl-c. 
