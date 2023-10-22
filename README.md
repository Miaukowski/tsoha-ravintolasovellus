# A little app for reviewing restaurants.
- Reviews include the restaurants name, a grade from 0-5, a text section and a hashtags section.
- Searching for them based on name or associated hashtag.
- User profile management and deletion.
- The front page displays the top 5 restaurants (based on average rating)
- ***Requires registering/logging in for full "enjoyment".*** 

# How to try it out: 
Make a folder where you'd like to try the app.

Clone this repository and all its content to that folder. In the root directory create a ```.env``` file and define its content as the following: 
```
DATABASE_URL=<the adress of the local database>
SECRET_KEY=<secret-key>
```
In a terminal window you go to the root directory. Install the python virtual-environment: 
```
python3 -m venv venv
```
Start the virtual-environment:
```
source venv/bin/activate
```
Install the required dependecies:
```
pip install -r requirements.txt
```

In a ***separate terminal window***, start a database: 
```
start-pg.sh
```
In the first terminal window, download the database scheme: 
```
psql < schema.sql
```

Start the app:
```
flask run
```
