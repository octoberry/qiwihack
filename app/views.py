# -*- coding: utf-8 -*-
__author__ = 'fuse'

from server import app
import os
from flask import render_template, request, redirect, url_for, jsonify
from forms import CreateEventForm, CreateEmailForm, PaymentForm, CardForm
from models import Events, Transaction, Subscribe
from pony.orm import db_session, commit
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound
import uuid
import payonline
from PIL import Image


def get_event(event_id):
    event = Events.get(id=event_id)
    if not event:
        raise NotFound()
    payonline.EVENT_ID = event_id
    return event


@app.route("/", methods=['GET', 'POST'])
def landing():
    return redirect('http://www.peerpay.ru')


@app.route("/new", methods=['GET'])
def create_form():
    form = CreateEventForm()
    return render_template('create.html', form=form)


@app.route("/new", methods=['POST'])
@db_session
def create():
    form = CreateEventForm(request.form)
    if not form.validate():
        return jsonify(status='validation_failed', errors=form.errors)
    if request.form.get('payment_type') in app.config['DISABLED_PAYMENT_TYPES']:
        return jsonify(status='not_supported',
                       url=url_for('not_supported', payment_type=request.form.get('payment_type')))

    event_data = dict(
        description=form.description.data,
        amount=form.amount.data,
        image=form.image.data,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    event = Events(**event_data)
    commit()
    return jsonify(status='success', url=url_for('visa', event_id=event.id))


@app.route("/visa/<int:event_id>", methods=['GET'])
@db_session
def visa_form(event_id):
    event = get_event(event_id)
    form = CardForm()
    return render_template('visa.html', form=form, event=event)


@app.route("/visa/<int:event_id>", methods=['POST'])
@db_session
def visa(event_id):
    event = get_event(event_id)
    form = CardForm(request.form)
    if not form.validate():
        return jsonify(status='validation_failed', errors=form.errors)

    card = payonline.Card.from_form(form)
    rebill_anchor = payonline.get_card_rebill_anchor(card)
    if not rebill_anchor:
        return jsonify(status='card_auth_error')

    event.rebill_anchor = rebill_anchor
    commit()
    return jsonify(status='success', url=url_for('success', event_id=event.id))


@app.route('/success/<int:event_id>')
@db_session
def success(event_id):
    event = get_event(event_id)
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
    im.thumbnail(app.config['UPLOAD_SIZE'], Image.ANTIALIAS)
    im.save(app.config['UPLOAD_FOLDER'] + outfile, "PNG")
    return jsonify(file=dict(url=app.config['UPLOAD_PATH'] + outfile))


@app.route('/payment/<int:event_id>', methods=['POST'])
@db_session
def invoke_payment(event_id):
    event = get_event(event_id)
    form = PaymentForm(request.form)
    if not form.validate():
        return jsonify(result='validation_failed', errors=form.errors)

    card = payonline.Card.from_form(form)
    rebill_anchor = payonline.get_card_rebill_anchor(card)
    if not rebill_anchor:
        return jsonify(result='card_auth_error')

    recip_card = payonline.RecipientCard(rebill_anchor=event.rebill_anchor)
    order = payonline.Order(order_id=event.id, amount=float(form.amount.data))
    res = payonline.transaction_card2card(rebill_anchor, recip_card, order)
    if res.required_3ds:
        trans_data = {
            'event_id': event.id,
            'amount': int(order.amount),
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
    pares = request.form['PaRes']
    md = request.form['MD']
    event_id, pd = md.split(';')
    event = Events.get(id=event_id)
    if event:
        payonline.EVENT_ID = event_id
        trans = Transaction.select(lambda t: t.md == md)[:]
        if trans:
            trans = trans[0]
            if trans.status == 0:
                res = payonline.transaction_card2card_3ds(pares, pd)
                if res.is_ok or res.get('Result') == 'Settled':
                    trans.status = 1
                    commit()
                else:
                    print res.body
            if trans.status == 1:
                return redirect(url_for('event', hashid=event.hashid)+'?status=ok')

        print 'Transaction not found'
    print 'Event not found'

    return redirect(url_for('event', hashid=event.hashid)+'?status=error')


# @app.route('/subscribe')
# def subscribe():
#     form = CreateEmailForm(request.form)
#     return render_template('subscribe.html', form=form)


@app.route('/not_supported/<string:payment_type>', methods=['GET', 'POST'])
@db_session
def not_supported(payment_type):
    if payment_type not in app.config['DISABLED_PAYMENT_TYPES']:
        return redirect('new')
    else:
        form = CreateEmailForm(request.form)
        if request.method == 'POST' and form.validate():
            email_data = dict(
                email=form.email.data,
                tags=form.tags.data,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            Subscribe(**email_data)
            commit()
            return render_template('email_saved.html')
        else:
            return render_template('not_supported.html', payment_type=payment_type, form=form)
