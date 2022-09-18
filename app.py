
from flask import Flask, render_template, request, send_file,session
from flask_dropzone import Dropzone
from transcribe import generateMOM
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'legocoders@gmail.com'
app.config['MAIL_PASSWORD'] = 'rjohxrgwnytmkpnw'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/mail",methods = ['GET','POST'])
def index():
   mailto=request.form.get("mailto")
   print(mailto,flush=True)
   msg = Message('Hello', sender = 'legocoders@gmail.com', recipients = [mailto]) 
   with app.open_resource("your_mom.txt") as fp:  
    msg.attach("your_mom.txt", "application/txt", fp.read())
   fp = app.open_resource("your_mom.txt")
   content=fp.read()
   #msg.html = render_template('mom_template.html', content=content)
   msg.body = fp.read()
   mail.send(msg)
   success_message = "Your Minutes of Meeting has been send successfully on your provided emails. Happy Working!"
   return render_template('MOM.html', success_message=success_message)


@app.route('/')
def upload_file():
   return render_template('upload1.html')

@app.route('/generate', methods = ['GET', 'POST'])
def generate():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename) 
        path = generateMOM(f.filename)
        with open(path, 'r') as f:
            t=f.read() 
        return render_template('MOM.html', t=t)

@app.route('/download')
def download_file():
    path = 'your_mom.txt'
    return send_file(path, as_attachment=True)
