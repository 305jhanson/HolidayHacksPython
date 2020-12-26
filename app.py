from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(200), nullable=False)
    rsvp = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_name = request.form['name']
        task_city = request.form['city']
        task_org = request.form['org']
        task_addy = request.form['addy']
        task_date=request.form['date']
        task_rsvp = request.form['rsvp']
        task_discription = request.form['description']

        new_task = Todo(name=task_name,
                        city=task_city,
                        organization=task_org,
                        address=task_addy,
                        date=task_date,
                        rsvp=task_rsvp,
                        description=task_discription)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Event could not be created'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
        

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'something wrong'
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'something wrong'
    else:
        return render_template('update.html', task=task_to_update)
        

@app.route('/rsvp/<int:id>', methods=['GET', 'POST'])
def rsvp(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':
        try:
            task_to_update.rsvp += 1
            db.session.commit()
            return redirect('/')
        except:
            return 'something wrong'
    else:
        return render_template('rsvp.html',task=task_to_update)

    
        

if __name__ == "__main__":
    app.run(debug=True)
