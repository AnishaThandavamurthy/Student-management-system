from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,migrate


app=Flask(__name__)
app.debug=True

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///student.db'
db=SQLAlchemy(app)
migrate=Migrate(app,db)
#registration db
class User(db.Model):
    

    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String(20), nullable=False)
    dob=db.Column(db.String(20),nullable=False)
    gender=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(20),unique=True,nullable=False)
    phone=db.Column(db.String(20),nullable=False)
    course=db.Column(db.String(20),nullable=False)
    yos=db.Column(db.String(20),nullable=False)
    user_name=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return f"register({self.name},{self.dob},{self.gender},{self.email},{self.phone},{self.course},{self.yos},{self.user_name},{self.password})"
#==================================================================================================================================================
    
# Define the database model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(20), unique=False, nullable=False)
    marks = db.Column(db.Integer, unique=False, nullable=False)  # Marks can be non-unique

    def __repr__(self):
        return f"Subject name: {self.subject_name}, IA 1: {self.marks}"



#============================================================================================================

#for contact page
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Message {self.id} from {self.name}>'
#=============================================================================================
class Log2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Log2 {self.id} from {self.name}>'
#====================================================================================

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register')
def reg():
    return render_template('register.html')

@app.route('/tt')
def classtt():
    return render_template('tt.html')

@app.route('/note')
def note():
    return render_template('notification.html')

@app.route('/exam')
def exam():
    return render_template('universityexam.html')

@app.route('/attendance')
def attend():
    return render_template('attendance.html')

@app.route('/lesson')
def lesson():
    return render_template('lesson.html')

@app.route('/assessment')
def assessment():
    return redirect(url_for("index"))
# @app.route('/dashboard')
# def dashboard():
#     dummyUser = {
#         "id": '',
#         "user_name": '',
#         "password": ""
#     }
#     return render_template('dashboard.html', user=dummyUser)

@app.route('/dashboard')
def dashboard_login():
    # user = login.query.get(id)
    return render_template('dashboard.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

#===========================================================================
# Route for the home page
@app.route('/index')
def index():
    users = Subject.query.all()
    return render_template('index.html', users=users)

# Route for adding a new user
@app.route('/adduser')
def adduser():
    return render_template('assessment.html')

# Route for handling the addition of a new subject
@app.route('/add', methods=["POST"])
def user():
    subject_name = request.form.get("subject_name")
    marks = request.form.get("marks")

    if subject_name and marks is not None:
        new_record = Subject(subject_name=subject_name, marks=marks)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('dashboard_login'))

# Route for editing a subject
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    user = Subject.query.get_or_404(id)

    if request.method == 'POST':  # Handling the form submission
        user.subject_name = request.form['subject_name']
        user.marks = request.form['marks']
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit.html', user=user)



#=================================================================================================================================


@app.route('/reg',methods=['POST'])
def register():
    name=request.form.get("name")
    dob=request.form.get("dob")
    gender=request.form.get("gender")
    email=request.form.get("email")
    phone=request.form.get("phone")
    course=request.form.get("course")
    yos=request.form.get("yos")
    user_name=request.form.get("user_name")
    password=request.form.get("password")
    
    

    
    
    new_user = User(
        name=name,
        dob=dob,
        gender=gender,
        email=email,
        phone=phone,
        course=course,
        yos=yos,
        user_name=user_name,
        password=password, 
        
        )
       
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("login"))


@app.route('/delete/<int:id>')
def erase(id):
    data=User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('index1'))

@app.route('/index1')
def index1():
   
    registers=User.query.all()
    return render_template('index1.html',registers=registers)

#===================================================================================================================================================
@app.route('/loguser')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        
        
        user = User.query.filter_by(user_name=user_name, password=password).first()
        if user_name!='' and password !='':
            user = User(user_name=user_name,password=password)
            
       
        return redirect(url_for("dashboard_login"))
    else:
        return redirect(url_for("register.html"))

        
    


       
#===================================================================================================================================
#  Route for the contact page
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Create a new Log2 instance
        new_message = Log2(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        
        return redirect(url_for('contacts'))  # Redirect after POST
    
    return render_template('contact.html')  # Render the contact page

# Route to view stored messages
@app.route('/messages', methods=['GET'])
def messages():
    all_messages = Log2.query.all()
    return render_template('messages.html', messages=all_messages)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)