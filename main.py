
import math
import smtplib
import difflib
import random
import flask
import os
import multiprocessing
from importlib_metadata import method_cache
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("jarvis.v.assistant@gmail.com", "jarvis_zcb123")
app = flask.Flask(__name__)
app.secret_key = "abcd123"
app.config['UPLOAD_FOLDER'] = 'static'
app.config['CUSTOM_STATIC_PATH'] = 'images'

@app.before_request
def make_session_permanent():
    flask.session.permanent = True
def show(user):
        
        images = {}
        following = f'static/Users/{user}/following'
        f = open(following)
        follwings = f.readlines()
        f.close()
        for user in follwings:
            userr = user.replace('\n','')
            path = f'static/Users/{userr}/post'
            files = os.listdir(path)
            for file in files:
                rasta = path+'/'+file
                images[rasta] = userr

        items = list(images.items())   
        print(items)    
        random.shuffle(items)
        return flask.render_template('index.html',images = items,user=user)







@app.route('/',methods = ['POST','GET'] )
def login():
    if flask.request.method == 'GET':
        try:
            if flask.session['user'] != '' :
            
                return show(flask.session['user'])
            else:    
                return flask.render_template('login.html')
        except Exception as e:
            print("eror",e)
            return flask.render_template('login.html')


    if flask.request.method == 'POST':
        print(flask.request.form['bttn'])
        print(flask.session)
        if flask.request.form['bttn'] == 'Login':
            user = flask.request.form['name']
            flask.session['user'] = user
            password= flask.request.form['pwd']
            if user in os.listdir('static'):
                f = open(f'static/Users/{user}/passwd.txt') 
                pwd = f.read()
                f.close()
                if pwd == password:
                    return show(user)      
                else:
                    flask.flash("Wrong Password")
                    return flask.redirect('/')
            else:
                flask.flash("Wrong Password")
                return flask.redirect('/')
        else:
            term = flask.request.form['term']
            return flask.redirect(f'/search/{term}')
#@app.route('/otp')        
def otp(user,pass1,email,phone):
    print(flask.request.method)
    if flask.request.method == 'POST':
        otp = flask.request.form['otp']
        if OTP == otp:
            os.mkdir(f"static/Users/{user}")
            os.mkdir(f"static/Users/{user}/post")
            f = open(f"static/Users/{user}/passwd.txt","w")
            f.write(pass1) 
            f.close()  
            f = open(f"static/Users/{user}/followers","w")   
            f.close()
            f = open(f"static/Users/{user}/following","w")   
            f.close()
            f = open('static/images/pic.png','rb')
            data = f.read()
            f.close()
            f = open(f"static/Users/{user}/pic.png","wb")  
            f.write(data) 
            f.close()
            f = open(f"static/Users/{user}/email","w")   
            f.write(email)
            f.close()
            f = open(f"static/Users/{user}/phone","w") 
            f.write(phone)  
              
            f.close()
            return flask.redirect('/')
    if flask.request.method == 'GET':
       
        digits="0123456789"
        OTP=""
        for i in range(6):
            OTP+=digits[math.floor(random.random()*10)]
        otp = OTP + " is your OTP"
        msg= otp 
        return flask.render_template('otp.html')

@app.route('/register',methods=['POST','GET']) 
def register():
    if flask.request.method == 'GET':
        return flask.render_template('register.html',submit='Send OTP')

    if flask.request.method == 'POST':
        print(flask.request.form['submit'])
        if flask.request.form['submit'] == 'Send OTP':
            user = flask.request.form['name']
            email = flask.request.form['email']
            phone = flask.request.form['numb']
            pass1= flask.request.form['pwd1']
            pass2= flask.request.form['pwd2']
            flask.session['user'] = user
            flask.session['email'] = email
            flask.session['phone'] = phone
            
            if os.path.exists(f'static/Users/{user}'):
                flask.flash("User Already Taken",'error')
                return flask.redirect("/register")

            else:  
            

                if pass2 == pass1:
                    flask.session['password'] = pass1 
                    digits="0123456789"
                    print(digits)
                    OTP=""
                    for i in range(6):
                        OTP+=digits[math.floor(random.random()*10)]
                    otp = OTP + " is your OTP"
                    msg= otp 
                    flask.session['otp'] = OTP
                    s.sendmail('&&&&&&&&&&&',email,msg)
                    return flask.render_template('otp.html')
                else:
                    flask.flash("Password Does not Match",'error')
                    return flask.redirect("/register")
        else:
            otp = flask.request.form['otp']
            print(otp)
            
            user = flask.session['user'] 
            email = flask.session['email'] 
            phone = flask.session['phone'] 
            pass1 = flask.session['password']
            ootp = flask.session['otp']
            
            print(otp)
            if ootp == otp:
                
                os.mkdir(f"static/Users/{user}")
                os.mkdir(f"static/Users/{user}/post")
                os.mkdir(f'static/Users/{user}/messages')
                f = open(f"static/Users/{user}/passwd.txt","w")
                f.write(pass1) 
                f.close()  
                f = open(f"static/Users/{user}/followers","w")   
                f.close()
                f = open(f"static/Users/{user}/following","w")   
                f.close()
                f = open('static/images/pic.png','rb')
                data = f.read()
                f.close()
                f = open(f"static/Users/{user}/pic.png","wb")  
                f.write(data) 
                f.close()
                f = open(f"static/Users/{user}/email","w")   
                f.write(email)
                f.close()
                f = open(f"static/Users/{user}/phone","w") 
                f.write(phone)  
                
                f.close()
                flask.session.clear()
                return flask.redirect('/')         


#@app.route('/otp', methods = ['POST','GET'])



@app.route('/<usern>',methods=['POST','GET'])
def shooe(usern):
    if flask.request.method == 'GET':
        if usern in os.listdir("static/Users"):
            path = f"static/Users/{usern}/post"
            images = []
            for i in os.listdir(path):
                images.append(path+"/"+i)
            
            f= open(f'static/Users/{usern}/followers','r')
            liss = f.readlines()
            f.close()
            print(flask.session['user'])
            print(liss)
            if flask.session['user'] == usern: 
                print('\n\n\n\n\n\n\n bro change krle')
                if (flask.session['user']+'\n') in liss:
                    return flask.render_template("user.html",usern=usern,images=images,followersno=len(liss),thef="Following",value='null',vata='change')
                else:    
                    return flask.render_template("user.html",usern=usern,images=images,followersno=len(liss),thef="Follow",value = 'foll',vata='change')  

            else:
                if (flask.session['user']+'\n') in liss:
                    return flask.render_template("user.html",usern=usern,images=images,followersno=len(liss),thef="Following",value='null',vata="die")
                else:    
                    return flask.render_template("user.html",usern=usern,images=images,followersno=len(liss),thef="Follow",value = 'foll',vata='die')   
        
        else:
            return "No User found"      
    if flask.request.method == 'POST':
        if flask.request.form['follow'] == 'foll':
            with open(f'static/Users/{usern}/followers','a') as f:
                f.writelines(flask.session['user']+"\n")
                f.close()
            name = flask.session['user']
            with open(f'static/Users/{name }/following','a') as f:
                f.writelines(usern+"\n")
                f.close()   
        
        else:
            pass        
        return flask.redirect(f'/{usern}')    

@app.route('/post',methods=['POST','GET'])        
def post():
    if flask.request.method == 'POST':
        file = flask.request.files['file']
        extension = file.filename.split('.')[1]
        print(extension)
        user = flask.session['user']
        no = len(os.listdir(f'static/Users/{user}/post/'))
        naame = f'{no+1}.{extension}'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],f'Users/{user}/post/{naame}'))
        return flask.render_template('post.html',src ='file')
    else:   
        return flask.render_template('post.html')

@app.route('/search',methods=['POST','GET'])
def search():
    if flask.request.method == "POST":
        term = flask.request.form['term']
        return flask.redirect(f'/search/{term}')
    else:    
        return flask.render_template('search.html')  

@app.route('/search/<term>',methods=['POST','GET'])
def find(term):
    if flask.request.method == "POST":
        term = flask.request.form['term']
        return flask.redirect(f'/search/{term}')
    else:    
            
        listt = os.listdir('static/Users')
        dekho = (difflib.get_close_matches(term,listt,10,0.2))
        return flask.render_template('search.html',valu=term,names = dekho )


@app.route('/<user>/change',methods=['POST','GET'])
def changePic(user):
    if flask.session['user'] == user:
        if flask.request.method == 'POST':
            try:
                file = flask.request.files['profile']
                file.save(f'static/Users/{user}/pic.png')
                return flask.redirect(f"/{user}")
            except Exception as e:
                print(e)
                return flask.redirect(f'/{user}')
        else:
            return flask.render_template('pic.html')  

    else:
        return flask.redirect(f'/{user}')

@app.route('/message',methods=['POST','GET'])
def message():
    if flask.request.method == 'GET':
        user = flask.session['user']
        path = f'static/Users/{user}/messages'
        chats = []
        for chat in  os.listdir(f'static/Users/{user}/messages'):
            chats.append(chat.replace('.chat',''))
        return flask.render_template('message.html',chats=chats)


@app.route('/message/<usern>/chat')
def sendOTP(usern):
    user = flask.session['user']
    path = f'static/Users/{user}/messages/{usern}.chat'
    path1 =  f'static/Users/{usern}/messages/{user}.chat'     

    
    
    if os.path.exists(path):
        f = open(path)
        
        cha = f.readlines()
        f.close()
        user_gamer = '['+ user + ']'
        print(user_gamer)
        #user_gamer = '['
        return flask.render_template('chat.html',chats=cha ,user = user_gamer,usern = usern)


    if os.path.exists(path1):
        f = open(path1)
        
        cha = f.readlines()
        f.close()
        user_gamer = '['+ user + ']'
        print(user_gamer)
        while True:
               return flask.render_template('chat.html',chats=cha ,user = user_gamer,usern = usern)    
    else:
        f = open(path,'w+')
        f.close()
    return flask.redirect(f'/message/{usern}')

@app.route('/message/<usern>')
def yo(usern):
    return flask.render_template('main.html',user=usern)
         
if __name__ == "__main__":
    app.run(threaded=True)

    