from flask import Flask, render_template, request, redirect, url_for
from forms import CreateEventForm
from pony.orm import db_session, commit, Database, Required
from datetime import datetime

app = Flask(__name__)
app.config.update(dict(
    DATABASE="postgres://pachay:@localhost/chipin",
    DEBUG=True,
))
db = Database('postgres', app.config['DATABASE'])


class Events(db.Entity):
    description = Required(unicode)
    amount = Required(int)
    card = Required(int)
    image = Required(unicode)
    updated_at = Required(datetime)
    created_at = Required(datetime)
db.generate_mapping()


@app.route("/", methods=['GET', 'POST'])
@db_session
def create():
    form = CreateEventForm(request.form)
    if request.method == 'POST' and form.validate():
        Events(description=form.description.data,
               amount=form.amount.data,
               card=form.card.data,
               image=form.image.data,
               created_at=datetime.now(),
               updated_at=datetime.now())
        return redirect(url_for('success'))
    return render_template('create.html', form=form)


@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run()
