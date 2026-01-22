from flask import render_template, request, redirect, url_for
from portfo import db, app, bcrypt
from portfo.forms import RegisterForm, LoginForm, UpdateAccountForm
from portfo.models import User, FriendProfile
from portfo.forms import FriendProfileForm
from flask_login import login_user, logout_user, current_user, login_required
import os, secrets
from PIL import Image

@app.route('/')
@login_required
def home():
    # Query all friend profiles for the current user
    friends = FriendProfile.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', friends=friends)


@app.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hash_password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('user/register.html', title='Register Page', form=form)

@app.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = db.session.scalar(db.select(User).where(User.username == username))

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user=user, remember=remember)
            return redirect(url_for('home'))
    return render_template('user/login.html', title='Login Page', form=form)

@app.route('/user/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/friend/profile', methods=['GET', 'POST'])
@login_required
def friend_profile():
    # Retrieve the friend profile associated with the current user, or create one if it doesn't exist
    friend = FriendProfile.query.filter_by(user_id=current_user.id).first()

    if not friend:
        return redirect(url_for('add_friend_profile'))  # Redirect to add friend profile if it doesn't exist

    if request.method == 'POST':
        # Update the friend's profile with the data from the form
        friend.fullname = request.form['friend_fullname']
        friend.role = request.form['role']
        friend.bio = request.form['bio']
        friend.img = request.form['friend_image']  # Assuming image name or path is passed in form
        db.session.commit()
        return redirect(url_for('friend_profile'))

    return render_template('friend/profile.html', title="Friend's Profile", friend=friend)


@app.route('/friend/add', methods=['GET', 'POST'])
@login_required
def add_friend_profile():
    form = FriendProfileForm()
    if form.validate_on_submit():
        # Handle the image upload and ensure avatar is set
        if form.avatar.data:
            avatar = save_avatar(form.avatar.data)  # Assuming save_avatar handles the file saving
        else:
            avatar = 'default.png'  # Default avatar when no image is uploaded

        # Create and add the FriendProfile
        friend = FriendProfile(
            fullname=form.fullname.data,
            role=form.role.data,
            bio=form.bio.data,
            img=avatar,
            user_id=current_user.id  # Assuming you're associating the profile with the logged-in user
        )

        # Add to the database and commit
        db.session.add(friend)
        db.session.commit()

        return redirect(url_for('friend_profile'))  # Redirect to the Friend's Profile page

    return render_template('friend/add_profile.html', title="Add Friend Profile", form=form)


def save_avatar(form_avatar):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_avatar.filename)
    avatar_fn = random_hex + ext

    avatar_path = os.path.join(app.root_path, 'static/img', avatar_fn)

    img_size = (256, 256)
    img = Image.open(form_avatar)
    img.thumbnail(img_size)
    img.save(avatar_path)

    return avatar_fn

@app.route('/user/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.fullname.data = current_user.fullname
    elif form.validate_on_submit():
        if form.avatar.data:
            avatar = save_avatar(form.avatar.data)
            current_user.avatar = avatar
        current_user.fullname = form.fullname.data
        db.session.commit()
        return redirect(url_for('account'))
    avatar_pic = current_user.avatar
    return render_template('user/account.html', title='Account Info Page', form=form, avatar_pic=avatar_pic)

