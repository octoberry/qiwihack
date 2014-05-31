import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from forms import CreateEventForm
from pony.orm import db_session, Database, Required, commit
from datetime import datetime
from config import config
from werkzeug.utils import secure_filename
import uuid
import splitpay
from PIL import Image

app = Flask(__name__)
app.config.update(config)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads/'
app.config['UPLOAD_PATH'] = '/static/uploads/'
db = Database('postgres', app.config['DATABASE'])
size = 250, 250


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


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image_file']
    filename = secure_filename(str(uuid.uuid1().int) + file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    outfile = "thumb" + filename
    im = Image.open(app.config['UPLOAD_FOLDER'] + filename)
    w, h = im.size
    if w < h:
        im = im.crop((0, 0+(h-w)/2, w, w+(h-w)/2))
    else:
        im = im.crop((0+(w-h)/2, 0, h+(w-h)/2, h))
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(app.config['UPLOAD_FOLDER'] + outfile, "PNG")
    return jsonify(file=dict(url=app.config['UPLOAD_PATH'] + outfile))


@app.route('/test', methods=['GET'])
def test_form():
    event = splitpay.test_event()
    return render_template('test.html', event=event)

if __name__ == "__main__":
    app.run()
