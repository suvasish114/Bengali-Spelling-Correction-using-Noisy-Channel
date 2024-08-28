# driving code
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from lib.correction import Correction
from nltk.tokenize import word_tokenize 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string' 

# forms
class SubmitForm(FlaskForm):
    textAreaField = TextAreaField("textarea", validators=[DataRequired()])
    submitField = SubmitField("Process")

# route index.html
@app.route("/", methods=['GET', 'POST'])
def index():
    output= ""
    submitform = SubmitForm()
    model = Correction()
    if submitform.validate_on_submit():
        input = submitform.textAreaField.data 
        output = model.correct_text(input)
        submitform.textAreaField.data = input
        redirect(url_for("index"))
    return render_template("index.html", submitform = submitform, data=output)

@app.route("/test", methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        data = request.form
        print(data)
        # return render_template("test.html", data=data)
    return render_template("test.html")

# gateway
if __name__ == "__main__":
    app.run(debug = True)