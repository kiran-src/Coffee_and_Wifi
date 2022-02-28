from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import URLField, TimeField
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Google Maps Location Link', validators=[DataRequired('URL is required')])
    opening = TimeField('Opening Time', validators=[DataRequired()])
    closing = TimeField('Closing Time', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', validators=[DataRequired()], choices=[("☕", "☕"), ("☕☕", "☕☕"), ("☕☕☕", "☕☕☕"), ("☕☕☕☕", "☕☕☕☕"), ("☕☕☕☕☕", "☕☕☕☕☕")])
    wifi = SelectField('WiFi Strength Rating', validators=[DataRequired()], choices=[("✘", "No WiFi"), ("💪", "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"), ("💪💪💪💪", "💪💪💪💪"), ("💪💪💪💪💪", "💪💪💪💪💪")])
    power = SelectField('Laptop Charging Speed Rating', validators=[DataRequired()], choices=[("✘", "No Power"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌"), ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

def time_format(time):
    time = f"{time}"[:-3]
    if time[-2:] == "00":
        time = time[:-3]
    if int(time[:2]) > 11:
        time = time + "PM"
    else:
        time = time + "AM"
    if time[0] == '0':
        time = time[1:]

    return time


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open ('cafe-data.csv', 'a', encoding="utf8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([form.cafe.data,form.location.data,time_format(form.opening.data),time_format(form.closing.data),form.coffee.data,form.wifi.data,form.power.data])
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    list_of_rows = []
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
