from flask import Flask, render_template, redirect, flash, request, session
import surveys
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)

# we need to turn app debug mode on. 
app.debug = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# works with render_templates so we could pass into html to debugger. 
debug = DebugToolbarExtension(app)
# if we have a flask_debugtoolbar turned on it will intercept redirect and we can turn that off.
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route("/")
def home():
    '''Display available surveys'''
    # get a dictionary contanting availble surveys.
    list_of_surveys = surveys.surveys
    return render_template("index.html", surveys=list_of_surveys)


@app.route("/new_survey", methods=['POST'])
def new_survey():
    '''Creating new survey and session for current survey'''
    # check if this is the first time user came to the page and add completed_surveys to session if does not exist
    survey_name = request.form['title']
    if len(session) == 0:
        session['completed_surveys'] = []
    # check if the survey has been already completed 
    if survey_name in session['completed_surveys']:
        return render_template('complete.html')
    else:
        # initiate new object in session for current survey
        session['current_survey'] = {'title':survey_name, 'responses':[]}
        # get the length of survey which is zero and pass that as a starting question index
        current_question = len(session['current_survey']['responses'])
        return redirect(f"/question/{current_question}")

@app.route('/check-question')
def check_question():
    '''check if user is on a correct question'''
    # check if user answered any questions and based on that redirect user
    # to the question they should be answering. 
    number_of_user_responses = len(session['current_survey']['responses'])
    return redirect(f'/question/{number_of_user_responses}')


@app.route("/question/<int:question_number>")
def survey_page(question_number):
    '''Get quesion from the surveys instance using question_number as index'''
    number_of_user_responses = len(session['current_survey']['responses'])
    if question_number == number_of_user_responses:
        survey = surveys.surveys[session['current_survey']['title']]
        survey_question = survey.questions[question_number]
        return render_template("questions.html", question=survey_question)
    else:
        # redirect user if user is trying to skip questions
        flash("You can not access that right now.", "error")
        return redirect("/check-question")

@app.route("/record-answer", methods=["POST"])
def record_answer():
    '''If user answered, record the answer'''
    response = request.form.get("answer")
    comment = request.form.get('comment', '')
    current_survey_name = session['current_survey']['title']
    # if there is an answer, record it
    if response:
        user_responses = session['current_survey']['responses']
        user_responses.append({'answer':response,'comment':comment})
        # session['current_survey']['responses'] = user_responses
        session['current_survey'] = {'title':current_survey_name, 'responses':user_responses}
    else:
        flash("Please choose an answer", "error")
    # check if current question is the last question
    number_of_user_responses = len(session['current_survey']['responses'])
    number_of_total_questions = len(surveys.surveys[current_survey_name].questions)
    if  number_of_user_responses == number_of_total_questions:
        # that means the survey is over
        completed_survey = session['current_survey']['title']
        completed_surveys_list = session['completed_surveys']
        completed_surveys_list.append(completed_survey)
        session['completed_surveys'] = completed_surveys_list
        return redirect("/thanks")
    else:
        # otherwise keep going
        return redirect("/check-question")

@app.route("/thanks")
def survey_complete():
    '''check if there is a current survey active and display user answers.'''
    there_a_current_survey = session.get('current_survey')
    if there_a_current_survey:
        user_responses = session['current_survey']['responses']
    return render_template("thanks.html", user_responses=user_responses)


if __name__ == "__main__":
    app.run(debug=True)
