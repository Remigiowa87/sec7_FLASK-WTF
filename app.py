import os
from datetime import date

from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import BooleanField, DateField, IntegerField, StringField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length, ValidationError

app =Flask(__name__)
app.config['SECRET_KEY'] = '.'

class Book():

    def __init__(self, title, amount, available, email, offer_date):
        self.title = title
        self.amount = amount
        self.available = available
        self.email = email
        self.offer_date = offer_date


class BookForm(FlaskForm):
    class Meta:
        csrf = True

    def validate_amount_even(form,field):
        if field.data % 2 !=1:
            raise(ValidationError("This number must be odd!"))

    title = StringField('Book title', validators=[DataRequired('Enter book title'),
                                                  Length(min=5, max=50, message='The title must have 5-50 characters')],  default='Unknow')
    amount = IntegerField('Amount', validators=[DataRequired(message='Enter amount',),validate_amount_even],  default=101)
    available = BooleanField('Available')
    cover = FileField("Book cover", validators=[FileRequired(),
                                                FileAllowed(['jpg', 'png'], "Sorry, we accept only png and jpg.")])
    # offer_date = DateField('Offer date', format='%Y-%m-%d')
    offer_date = DateField('Offer date',) # , format='%Y-%m-%d')
    # offer_date = DateTimeLocalField('Offer date',format='%Y-%m-%d')



class BookFormEmail(BookForm):
    email = StringField("e-mail", validators=[Email()])


@app.route('/', methods=['GET','POST'])
def index():

    book = Book(title="How to take a nice photo", amount=11, available=True,email='', offer_date=date.today())
    # form = BookForm(csrf_enabled  = False)
    # form = BookForm( title="European Kings", amount=99, available=True)
    form = BookFormEmail( obj=book)
    # form = BookForm( obj=book)

    del form.available

    if form.validate_on_submit():

        f = form.cover.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.root_path,'static', 'covers', filename))

        form.populate_obj(book)
        return f'''<h1>Hello</h1>
                    <ul>
                        <li>{form.title.label}: {book.title}</li>
                        <li>{form.amount.label}: {book.amount}</li>
                        <li>available: {book.available}</li>
                        <li>email:  {book.email}</li>
                        <li>offer date:  {book.offer_date}</li>
                        <li><img src="{url_for('static', filename='covers/{}'.format(filename))}"></li>
                    </ul>'''



    return render_template('index.html', form=form)

if __name__ =='__main__':
    app.run()