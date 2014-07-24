import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from forms import CreateEventForm, CreateEmailForm, PaymentForm
from pony.orm import db_session, Database, Required, commit, select, sql_debug
from datetime import datetime
from config import config
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound
import uuid
import payonline
from PIL import Image
from hashids import Hashids

app = Flask(__name__)
app.config.update(config)
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__)) + '/static/uploads/'
app.config['UPLOAD_PATH'] = '/static/uploads/'
db = Database('postgres', app.config['DATABASE'])
size = 250, 250

hashids = Hashids(salt='Chi822pinPAdd22234')

if app.config['DEBUG']:
    payonline.debug_logging()
    sql_debug(True)

payonline.MERCHANT_ID = app.config['PAYONLINE_MERCHANT_ID']
payonline.PRIVATE_SECURITY_KEY = app.config['PAYONLINE_PRIVATE_SECURITY_KEY']


class Events(db.Entity):
    description = Required(unicode)
    amount = Required(int)
    card = Required(int)
    image = Required(unicode)
    updated_at = Required(datetime)
    created_at = Required(datetime)

    @property
    def income(self):
        return select(sum(t.amount) for t in Transaction if t.status == 1 and t.event_id == self.id)[:1][0]

    @property
    def hashid(self):
        return hashids.encrypt(self.id, int(self.created_at.strftime('%s')))

    @staticmethod
    def get_by_hashid(hashid):
        event_id, _ = hashids.decrypt(hashid)
        return Events.get(id=event_id)


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
def landing():
    return redirect('http://www.peerpay.ru')


@app.route("/new", methods=['GET', 'POST'])
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
        event = Events(**event_data)
        commit()
        return redirect(url_for('success', event_id=event.id))
    return render_template('create.html', form=form)


@app.route('/success/<int:event_id>')
@db_session
def success(event_id):
    event = Events.get(id=event_id)
    event.url = url_for('event', hashid=event.hashid, _external=True)
    return render_template('success.html', event=event)


@app.route('/e/<path:hashid>', methods=['GET', 'POST'])
@db_session
def event(hashid):
    hashid = hashid.strip('/')
    event = Events.get_by_hashid(hashid)
    event.url = url_for('event', hashid=hashid, _external=True)
    status = request.args.get('status')
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


@app.route('/payment/<int:event_id>', methods=['POST'])
@db_session
def invoke_payment(event_id):
    event = Events.get(id=event_id)
    if not event:
        raise NotFound()

    form = PaymentForm(request.form)
    if not form.validate():
        return jsonify(result='validation_failed', errors=form.errors)

    card = payonline.Card(
        holder_name=form.holder_name.data,
        number=form.card_number.data,
        exp_date=form.card_expdate.data,
        cvv=form.card_cvv.data
    )
    rebill_anchor = payonline.get_card_rebill_anchor(card)
    if not rebill_anchor:
        return jsonify(result='card_auth_error')

    recip_card = payonline.RecipientCard(card_number=event.card)
    order = payonline.Order(order_id=event.id, amount=float(form.amount.data))
    res = payonline.transaction_card2card(rebill_anchor, recip_card, order)
    if res.required_3ds:
        trans_data = {
            'event_id': event.id,
            'amount': int(order.amount),
            'card': card.number,
            'md': '%s;%s' % (event.id, res.get('pd')),
            'status': 0,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        trans = Transaction(**trans_data)
        commit()
        acsurl = res.get('acsurl')
        data_for_3ds = {
            'PaReq': res.get('pareq'),
            'MD': trans.md,
            'TermUrl': url_for('complete_payment', _external=True)
        }
        return jsonify(result='required_3ds', url=acsurl, data=data_for_3ds)

    if res.is_error:
        return jsonify(result='payment_error')

    return jsonify(result='payment_ok')


@app.route('/complete', methods=['POST'])
@db_session
def complete_payment():
    print request.form
    pares = request.form['PaRes']
    md = request.form['MD']
    event_id, pd = md.split(';')
    event = Events.get(id=event_id)
    if event:
        trans = Transaction.select(lambda t: t.md == md)[:]
        if trans:
            trans = trans[0]
            res = payonline.transaction_card2card_3ds(pares, pd)
            if res.is_ok or res.get('Result') == 'Settled':
                trans.status = 1
                commit()
                return redirect(url_for('event', hashid=event.hashid)+'?status=ok')
            print res.body
        print 'Transaction not found'
    print 'Event not found'

    return redirect(url_for('event', hashid=event.hashid)+'?status=error')


@app.route('/subscribe')
def subscribe():
    form = CreateEmailForm(request.form)
    return render_template('subscribe.html', form=form)

if __name__ == "__main__":
    app.run()
