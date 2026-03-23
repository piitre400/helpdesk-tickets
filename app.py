from flask import Flask, render_template, request, redirect, url_for
from models import db, Ticket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helpdesk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tickets = Ticket.query.order_by(Ticket.fecha.desc()).all()
    return render_template('index.html', tickets=tickets)

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
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('detalle_ticket.html', ticket=ticket)

if __name__ == '__main__':
    app.run(debug=True)

    