import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from forms import CreateEventForm
from pony.orm import db_session, Database, Required, commit, select
from datetime import datetime
from config import config
from werkzeug.utils import secure_filename
import uuid
import splitpay
from PIL import Image
from hashids import Hashids

app = Flask(__name__)
app.config.update(config)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads/'
app.config['UPLOAD_PATH'] = '/static/uploads/'
db = Database('postgres', app.config['DATABASE'])
size = 250, 250

hashids = Hashids(salt='Chipin')

if app.config['DEBUG']:
    splitpay.debug_logging()


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

    @property
    def income(self):
        return sum(select(t.amount for t in Transaction if t.status == 1 and t.event_id == self.id))


class Transaction(db.Entity):
    event_id = Required(int)
    amount = Required(int)
    card = Required(unicode)
    md = Required(unicode)
    status = Required(int)
    updated_at = Required(datetime)
    created_at = Required(datetime)


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
        event_data = splitpay.add_split_event(event_data)
        event = Events(**event_data)
        commit()
        return redirect(url_for('success', event_id=event.id))
    return render_template('create.html', form=form)


@app.route('/success/<int:event_id>')
@db_session
def success(event_id):
    event = Events.get(id=event_id)
    hash = hashids.encrypt(event.id, event.split_member_id)
    print hash
    event.url = url_for('event', hash=hash, _external=True)
    return render_template('success.html', event=event)


@app.route('/e/<path:hash>', methods=['GET', 'POST'])
@db_session
def event(hash):
    hash = hash.strip('/')
    event_id, _ = hashids.decrypt(hash)
    event = Events.get(id=event_id)
    event.url = url_for('event', hash=hash, _external=True)

    md = request.args.get('md')
    status = request.args.get('status')
    if md and status == 'ok':
        trans = Transaction.get(md=md)
        if trans:
            trans.status = 1
            commit()

    return render_template('event.html', event=event, status=status, error=request.args.get('error'))


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


@app.route('/transaction', methods=['POST'])
@db_session
def transaction():
    data = {
        'event_id': int(request.form['event_id']),
        'amount': int(request.form['amount']),
        'card': request.form['card'],
        'md': request.form['md'],
        'status': 0,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    trans = Transaction(**data)
    commit()
    return jsonify(status='ok')


if __name__ == "__main__":
    app.run()
