from flask import Flask, render_template, request, redirect, url_for
from models import db, Ticket
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    prioridad = request.args.get('prioridad', '')
    estado = request.args.get('estado', '')
    query = Ticket.query
    if prioridad:
        query = query.filter_by(prioridad=prioridad)
    if estado:
        query = query.filter_by(estado=estado)
    tickets = query.order_by(Ticket.fecha.desc()).all()
    return render_template('index.html', tickets=tickets,
                           prioridad=prioridad, estado=estado)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_ticket():
    if request.method == 'POST':
        ticket = Ticket(
            cliente=request.form['cliente'],
            descripcion=request.form['descripcion'],
            prioridad=request.form['prioridad']
        )
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('nuevo_ticket.html')

@app.route('/ticket/<int:id>', methods=['GET', 'POST'])
def detalle_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    if request.method == 'POST':
        ticket.tecnico = request.form['tecnico']
        ticket.estado = request.form['estado']
        fecha_visita_str = request.form.get('fecha_visita')
        if fecha_visita_str:
            ticket.fecha_visita = datetime.strptime(fecha_visita_str, '%Y-%m-%dT%H:%M')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('detalle_ticket.html', ticket=ticket)

@app.route('/dashboard')
def dashboard():
    total = Ticket.query.count()
    abiertos = Ticket.query.filter_by(estado='abierto').count()
    en_proceso = Ticket.query.filter_by(estado='en proceso').count()
    cerrados = Ticket.query.filter_by(estado='cerrado').count()
    alta = Ticket.query.filter_by(prioridad='alta').count()
    media = Ticket.query.filter_by(prioridad='media').count()
    baja = Ticket.query.filter_by(prioridad='baja').count()

    tickets_cerrados = Ticket.query.filter_by(estado='cerrado').all()
    tiempos = []
    for t in tickets_cerrados:
        if t.fecha_visita:
            diff = (t.fecha_visita - t.fecha).total_seconds() / 3600
            tiempos.append(round(diff, 1))
    promedio = round(sum(tiempos) / len(tiempos), 1) if tiempos else 0

    return render_template('dashboard.html',
                           total=total, abiertos=abiertos,
                           en_proceso=en_proceso, cerrados=cerrados,
                           alta=alta, media=media, baja=baja,
                           promedio=promedio)

if __name__ == '__main__':
    app.run(debug=True)