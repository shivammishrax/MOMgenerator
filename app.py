
from flask import Flask, render_template, request, send_file,session
from flask_dropzone import Dropzone
from transcribe import generateMOM
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
mail= Mail(app)
app.secret_key = "abc"

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'xshivammishra@gmail.com'
app.config['MAIL_PASSWORD'] = 'vrbirujjuntkumkt'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/mail",methods = ['GET','POST'])
def index():
   mailto=request.form.get("mailto")
   #list = mailto.split(",")
   list = mailto.split(",")
   print(list,flush=True)
   msg = Message('Minutes of Meeting', sender = 'xshivammishra@gmail.com', recipients = list) 
   with app.open_resource("your_mom.txt") as fp:  
    msg.attach("your_mom.txt", "application/txt", fp.read())
   fp = app.open_resource("your_mom.txt")
   msg.html = fp.read()
   #mom=extract_mom(fp.filename)
   
   mom=session['mom']
   print(mom['date'],flush=True)
   msg.html = render_template('your_mom_template.html', mom=mom)
   #msg.body = fp.read()
   mail.send(msg)
   message = "Your Minutes of Meeting has been sent successfully on your provided emails. Happy Working!"
   return render_template('mom_template.html', message=message, mom=mom)

@app.route('/')
def upload_file():
   return render_template('upload1.html')

@app.route('/generate', methods = ['GET', 'POST'])
def generate():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        mom=generateMOM(f.filename)
        session['mom']=mom
        return render_template('mom_template.html', mom=mom)

@app.route('/download')
def download_file():
    path = 'your_mom.txt'
    return send_file(path, as_attachment=True)