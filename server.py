from flask import Flask, render_template, request, redirect, url_for
from forms import CreateEventForm
from pony.orm import db_session, Database, Required, commit
from datetime import datetime
from config import config
import splitpay

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
    split_event_id = Required(int)
    split_owner_id = Required(int)
    split_member_id = Required(int)


db.generate_mapping()


@app.route("/", methods=['GET', 'POST'])
@db_session
def create():
    form = CreateEventForm(request.form)
    if request.method == 'POST' and form.validate():
        event_data = dict(
            description=form.description.data,
            amount=form.amount.data,
            card=form.card.data,
            image=form.image.data,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        event_data = add_split_event(event_data)
        event = Events(**event_data)
        commit()
        return redirect(url_for('success', event_id=event.id))
    return render_template('create.html', form=form)

def add_split_event(event_data):
    split_event = splitpay.add_event(
        amount=event_data['amount'],
        card_number=event_data['card'],
        owner_name='Default owner',
        members=[splitpay.default_member(event_data['amount'])]
    )
    if split_event:
        event_data['split_event_id'] = split_event['id_event']
        event_data['split_owner_id'] = split_event['owner_id']
        event_data['split_member_id'] = split_event['members'][0]['id_member']
    return event_data

@app.route('/success/<int:event_id>')
@db_session
def success(event_id):
    event = Events.get(id=event_id)
    event.url = url_for('event', event_id=event_id, _external=True)
    return render_template('success.html', event=event)

@app.route('/event/<int:event_id>')
@db_session
def event(event_id):
    event = Events.get(id=event_id)
    event.url = url_for('event', event_id=event_id, _external=True)
    return render_template('event.html', event=event)

@app.route('/test', methods=['GET'])
def test_form():
    event = splitpay.test_event()
    return render_template('test.html', event=event)

if __name__ == "__main__":
    app.run()
