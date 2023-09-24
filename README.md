Disclaimer: Sorry I switched to English, I realised my Finish is not good enough for all this explaining I am about to do. 

# Features that are currently implemented and working:
- A front page with login and register option, and the page also displays restaurants that have been reviewed as a little "teaser". 
- A login page.
- A register page. 
- A dashboard, that displays the restaurants that have been reviewed, as well as their average score. This also comes with an option of clicking a "view information" button.
- A separate "restaurant details" page, this is where the user gets redirected when they click the "view information" button,  where the text part of the review and hashtags are displayed.
- The dashboard also features an option to add a new restaurant, or review an existing one, giving it a grade from 0-5, writing a little text about the restaurant and also adding hashtags. 
- The dashboard features a search option, where the user currently can search for restaurants (currently only!) by name.
- The search button takes you to a separate page, that shows the user the search results. This then gives the users information about said restaurant (average score & name ). 

# Features that need to be implemented:
- A log out button. 
- Security measures needs to be reviewed. 
- The option to search for restaurants based on hashtags. 
- Administrator rights and options. 
- An option for the user to remove their account. 
- More options for information about the restaurant, such as opening hours etc. 
- Unsure if I only want users with admin rights to classify restaurants, I like that the user has the freedom to do so. Maybe only save admin rights for "censorship". 
- A better looking layout, it's horribly ugly at the moment. 
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


---------------
# Previous description
## Ravintolasovellus
### Keskeiset Toiminnot
- Käyttäjä ja ylläpitäjä mahdollisuudet.
- Käyttäjä pystyy hakemaan ravintoloita (myös jonkun tietyn haku sanan perusteella - ns. "filtteröidä" hakutulokset). 
- Käyttäjä voi kirjautua sisään ja ulos, ja myös luoda uuden tunnuksen tai poistaa vanhan (tietoturvaa myös huomioiden).
- käyttäjä voi hakea tietoa ravintolasta (aukiooloajat, arvostelut yms). 
- käyttäjä voi arvostella ravintolaa.
- ylläpitäjä voi poistaa arvostelut (jos on epäsopivia kommentteja yms). 
- ylläpitäjä voi luokitella ravintolaa (esim: sushi, kebab, salaatti yms), ja käyttäjä voi sitten valita tätä "haku vaihtoehtoa". 
- ylläpitäjällä saa myös dataa suosituista ravintoloista, ja voi vaikka kertoa tästä käyttäjille, esim "suositut nyt".

