from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


#--------For database-----------
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todos.db"
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
db=SQLAlchemy(app)


class ToDO(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{ self.sno} - {self.title}"
    


#-------------------------------
@app.route('/', methods =['GET','POST'])
def hello_world():
    
    if request.method=='POST':
        # print(request.form['title'])
        title=request.form['title']
        desc=request.form['desc']
        
        todo=ToDO(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    # todo=ToDO(title="First todo",desc="Start Investing asap....")
    # db.session.add(todo)
    # db.session.commit()
    
    allTodo=ToDO.query.all()
   
    
    return render_template("index.html",allTodo=allTodo)
    

@app.route('/products')
def prods():
    return 'Hello, Products here'
    # return 'Hello, pab!'
    

@app.route('/update/<int:sno>',methods =['GET','POST'])
def update(sno):
    
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        
        todo=ToDO.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=ToDO.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)
    


@app.route('/delete/<int:sno>')
def delete(sno):
    todo=ToDO.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__== "__main__":      
    app.run(debug=False,host="0.0.0.0")    # debug true to show errors in browser # app.run calls to run the script
    
    
    