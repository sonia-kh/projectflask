from flask import render_template, request, redirect, flash, url_for
from app import app, db
from app.models.user import User
from flask_login import login_user, logout_user, login_required, current_user
from app.api.registration import REGISTER_in_LIBRARY, REGISTER_in_FINANCIAL
from app.api.graduation import fetch_student_graduation_status
@app.route("/")
def home():

    return render_template('pages/home.html')



@app.route("/graduation")
@login_required
def graduation():
    student_id = current_user.student_id  # Assuming current_user has a student_id attribute
    graduation_info = fetch_student_graduation_status(student_id)
    print(graduation_info)
    if graduation_info.get('error'):
        flash(graduation_info['error'], 'danger')
        return render_template("pages/graduation.html", can_graduate=False)
    
    if not graduation_info['account_exists']:
        flash('Account not found for current user.', 'danger')
        return render_template("pages/graduation.html", can_graduate=False)
    
    if graduation_info['has_outstanding_balance']:
        flash('You have outstanding balance and are not eligible for graduation.', 'danger')
        return render_template("pages/graduation.html", can_graduate=False)
    
    # can_graduate = graduation_info['graduation_eligibility']
    
    return render_template("pages/graduation.html", can_graduate=True)
@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if password != password2:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('home'))
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash('Username or Email already exists', 'danger')
            return redirect(url_for('home'))

        try:
            new_user = User(email=email, username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            student_id = new_user.student_id
            
            library = REGISTER_in_LIBRARY(student_id)
            finance = REGISTER_in_FINANCIAL(student_id)
            print(library, finance)
            if library and finance:
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('home'))
            else:
                db.session.delete(new_user)
                db.session.commit()
                flash('Library account registration failed. Please try again.', 'danger')
                return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration: {str(e)}', 'danger')
            return redirect(url_for('home'))

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))    
    return render_template("pages/login.html")




@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))



@app.route("/student_info")
@login_required
def student_info():
    student = current_user
    return render_template("pages/profile.html", student=student)

@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    student = current_user
    student.first_name = request.form.get('first_name')
    student.last_name = request.form.get('last_name')
    student.username = request.form.get('username')
    student.email = request.form.get('email')
    student.phone = request.form.get('phone')
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('student_info'))
