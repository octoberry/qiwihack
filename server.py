from flask import Flask, render_template, request, redirect, url_for
from forms import CreateEventForm
from pony.orm import db_session, Database, Required, commit
from datetime import datetime
from config import config

app = Flask(__name__)
app.config.update(config)
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
        event = Events(description=form.description.data,
                       amount=form.amount.data,
                       card=form.card.data,
                       image=form.image.data,
                       created_at=datetime.now(),
                       updated_at=datetime.now())
        commit()
        return redirect(url_for('event', event_id=event.id))
    return render_template('create.html', form=form)


@app.route('/event/<int:event_id>')
@db_session
def event(event_id):
    event = Events.get(id=event_id)
    event.url = url_for('event', event_id=event_id, _external=True)
    return render_template('event.html', event=event)


if __name__ == "__main__":
    app.run()
