from flask import Flask,render_template ,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# 3 slash is relative path
db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r' %self.id
@app.route('/',methods = ['POST','GET'])


def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') 
        except:
            return 'there is an issue '
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)
        
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem delete that taslk'
    
    
@app.route('/update/<int:id>',methods = ['POST','GET'])
def update(id):
    # task_to_update = Todo.query.get_or_404(id)
    # try:
    #     db
    task   =  Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "not added to the database"
        
    else:
        return render_template('update.html' , task = task)



# no need to specify the path of folder auto looks in templates
if(__name__ == "__main__"):
    app.run(debug=True)
    
    #  dont use python interactive shell
    # instead use flask shell
    