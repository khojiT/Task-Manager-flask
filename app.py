from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime , String
from sqlalchemy.sql import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class todo(db.Model):
    id = Column(Integer, primary_key = True)
    content = Column(String(200),nullable = False)
    completed = Column(Integer,default = 0)
    date = Column(DateTime(timezone=True), server_default=func.now())
    def __repr__(self):
        return f'<Task {self.id}>'




@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_c = request.form['content']
        new = todo(content=task_c)

        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/')
        except:
            return 'something is wrong'
    else:
        tasks = todo.query.order_by(todo.date).all()
        return render_template('index.html',tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_del = todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem'

@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    task = todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'sth was wrong'
    else:
        return render_template('update.html',task=task)

if __name__ == "__main__":
    app.run(debug=True)
