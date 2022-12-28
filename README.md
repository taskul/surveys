# surveys
A simple survey made with flask, CSS and HTML
![image of surveys home page with two available surveys displayed](static/surveys.png)

<!-- ABOUT THE PROJECT -->
## About The Project
This is a simple survey built with Flask, HTML and CSS.
Home page displays available suveys which are two instances of Survey class imported from surveys.py.
Clicking on a "Start Survey" button starts the survey with first question at index zero. 
User is unable to skip questions, and any attempts redirect user back to the current questions they should be answering. 
User's progress is stored in cookies with the help of flask session. This survey is not using any databases to store user progress. 
When survey is complete survey name is added to cookies list of "completed_surveys" which is then checked for when user tried to take the survey again.
If the survey has been completed user is redirected to a complete.html page telling user that they have already completed this survey. 


### surveys.py
contains two classes Question and Survey which are used to build a structure of survey instances. 
Two survey instances are included in a surveys dictionary, which has been imported to app.py 

### app.py
required imports
```Python 
from flask import Flask, render_template, redirect, flash, request, session
import surveys
from flask_debugtoolbar import DebugToolbarExtension
```
DebugToolbarExtension is used for debugging. 

**Routes:**
```Python
# home page
@app.route("/")

# starting a new survey
@app.route("/new_survey", methods=['POST'])

# checking if user has correct question
@app.route('/check-question')

# rendering the current survey question
@app.route("/question/<int:question_number>")

# recording answer in flask session and checking if current question is the last question
@app.route("/record-answer", methods=["POST"])

# displaying survey completion page
@app.route("/thanks")
```

### HTML pages
- base.html - *contains navbar, footer and error messages that can be extended to other pages using jinja templating*
- complete.html - *displays the survey has been completed message*
- index.html - *main page that displays available surveys*
- questions.html - *shows current question which id rendered dynamically based on user progress with current survey*
- thanks.html - *survey completion page that shows summary of user answers*
