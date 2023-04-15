from flask import Flask, render_template, request

app= Flask(__name__);

#For the displaying of the content of the form
subscribers = [];

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
    
    subscribers.append(f"Name:{first_name}{last_name} || Email: {email}")
    
    # using jinja
    title="form page"
    
    # return render_template("form.html",title=title,first_name=first_name,last_name=last_name,email=email)
    
    return render_template("form.html",title=title,subscribers=subscribers)



# for running using python app.py
if __name__ == '__main__':
    app.run(debug=True)