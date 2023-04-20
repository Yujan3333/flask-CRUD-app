from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc


app= Flask(__name__)
# '///' represents the relative path right here
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///friends.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize the database
db=SQLAlchemy(app)

# For runnind command in terminal
app.app_context().push()


# Create db model
#write python that is converted to SQL
class Friends(db.Model):
    id= db.Column(db.Integer ,primary_key=True)
    name= db.Column(db.String(100), nullable=False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create a function to return a string whe we add something
    def __repr__(self):
        return '<Name %r>' %self.id



#For the displaying of the content of the form
subscribers = [];


@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return "Problem deleting the friend"








@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id) 
    if request.method=='POST':
        friend_to_update.name= request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was a problem updating friends!"
    else:
        return render_template('update.html',friend_to_update=friend_to_update)



@app.route('/friends', methods=['POST','GET'])
def friends():
    title="Friends of Yujan"
    
    if request.method =='POST':
        friend_name= request.form['name']
        # adding the friend name from form to db table Friends(Class dec above)
        new_friend=  Friends(name=friend_name)
        
        # push to db
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was error adding friends name to db"
    else:
        friends =Friends.query.order_by(desc(Friends.date_created))
        return render_template("friends.html",title=title, friends=friends)





# Homepage routing
@app.route('/')
def index():
    return render_template("index.html")




@app.route('/about')
def about():
    # using jinja
    title="About Yujan"
    return render_template("about.html",title=title)





@app.route('/subscribe')
def subscribe():
    # using jinja
    title="Subscribe my blog"
    return render_template("subscribe.html",title=title)



@app.route('/form', methods=["POST"])
def form():
    #taking data from html page
    first_name= request.form.get("first_name")
    last_name= request.form.get("last_name")
    email= request.form.get("email")
    
    
    if not first_name or not last_name or not email:
        error_statement = "All fields must be filled !!"
        return render_template('subscribe.html', error_statement=error_statement, first_name=first_name,last_name=last_name,email=email)
    
    subscribers.append(f"Name:{first_name}{last_name} || Email: {email}")
    
    # using jinja
    title="Display Details"
    
    # return render_template("form.html",title=title,first_name=first_name,last_name=last_name,email=email)
    
    return render_template("form1.html",title=title,subscribers=subscribers)



# for running using python app.py
if __name__ == '__main__':
    app.run(debug=True)