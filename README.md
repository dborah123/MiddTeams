## Middteams
### Middlebury College, Computer Science CSCI 701 (Fall 2021)

### about
MiddTeams is a web applications that is meant to handle scheduling for the athletics department at Middlebury. Our aim is to facilitate an easier time for both athletes and
coaches in scheduling. Thus, MiddTeams provides teams not only provides workout scheduling, but also the ability to look at the class schedules of other teammates. Lastly, there
are also scheduling tools, that with just one click, provide users with the ability to see when the optimal time to schedule is. in scheduling. Thus, MiddTeams provides teams not
only provides workout scheduling, but also the ability to look at the class schedules of other teammates. Lastly, there are also scheduling tools, that with just one click,
provide users with the ability to see when the optimal time to schedule is.

view MiddTeams [here](https://middteams.herokuapp.com/)
view our project website [here](https://dborah123.github.io/MiddTeams/)

### building
1. Create a python virtual environment and enter it
2. Create new directory in same folder and git clone the repo
3. pip install the libraries with the command `pip install -r requirements.txt`
4. Create a PostgreSQL database and connect it to the app in the settings.py file
5. Run the command `python manage.py migrate` to set the database
6. Run the command `python manage.py runserver` to run on localhost

### usage
- Scheduling workouts and seeing those attending
- Adding you class schedule as well as seeing others'
- Viewing team rosters
- Scheduling tools used for finding the best time to schedule meetings
- RSVP'ing and recording absences for workouts

### limitations
- Schedule is unflexible as singular events aren't possible are necessary for users at this stage
- There aren't different types of workouts (ie. mandatory, optional, offseason, captain's practices)
- No informal ways of communications through this app
