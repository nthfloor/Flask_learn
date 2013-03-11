from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm
from models import User, ROLE_USER, ROLE_ADMIN

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    #user = {'name':'nathan','email':'nathan.floor@gmail.com'}
    posts = [ 
        {
            'author':{'name':'John'},
            'body':'Beautiful day in Portland!'
        },
        {
            'author':{'name':'Susan'},
            'body':'The avengers movie was cool'
        }
    ]
    return render_template("index.html",title = 'Home', user = user, posts = posts)

@app.before_request
def before_request():
    g.user = current_user


@app.route('/login',methods = ['GET','POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    # if form.validate_on_submit():
    #     session['remember_me'] = form.remember_me.data
    #     print form.openid.data
    #     return oid.try_login(form.openid.data, ask_for = ['nickname','email'])

    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email','nickname'])

    return render_template('login.html',title = 'Sign In',form = form,providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    # if resp.email is None or resp.email == "":
    #     flash('Invalid login. Please try again.')
    #     redirect(url_for('login'))
   
    # flash('Successful login') 
    # user = User.query.filter_by(email = resp.email).first()
    # if user is None:
    #     name = resp.name
    #     if name is None or name == "":
    #         name = resp.email.split('@')[0]
    #     user = User(name=name,email=resp.email,role=ROLE_USER)
    #     db.session.add(user)
    #     db.session.commit()
    # remember_me = False
    # if 'remember_me' in session:
    #     remember_me = session['remember_me']
    #     session.pop('remember_me', None)
    # login_user(user,remember = remember_me)
    # return redirect(request.args.get('next') or url_for('index'))

    #debug
    session['openid'] = resp.identity_url
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('index', next=oid.get_next_url(),
                            name= resp.nickname, email=resp.email))


@lm.user_loader
def load_user(id):
    session.pop('openid', None)
    flash(u'You have been signed out')
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
