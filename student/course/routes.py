from course import course
from flask import render_template, redirect, url_for, flash
from app.models.course import Course, Enrollment
from app import app, db

from flask_login import current_user, login_required
from .api.generateInvoice import CREATE_BILL
from .api.voidInvoice import VOID_INVOICE


@course.route("/courses")
def courses():
    courses = Course.query.all()
    return render_template("pages/courses.html", courses=courses)

@course.route("/course/<int:course_id>")
def courseView(course_id):
    course = Course.query.get_or_404(course_id)
    enrolled = False
    if current_user.is_authenticated:
        enrolled = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first() is not None
    return render_template('pages/course.html', course=course, enrolled=enrolled)


@course.route("/enroll/<int:course_id>", methods=["GET"])
@login_required
def enroll_course(course_id):
    course = Course.query.get_or_404(course_id)
    if Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first():
        flash('You are already enrolled in this course.', 'info')
        return redirect(url_for('course.courseView', course_id=course.id))
    
    invoice_result = CREATE_BILL(course.fee, current_user.student_id)
    print(invoice_result)
    if invoice_result['created_successfully']:
        enrollment = Enrollment(user_id=current_user.id, course_id=course.id, reference=invoice_result['invoice_reference'])
        db.session.add(enrollment)
        db.session.commit()
        flash('You have successfully enrolled in the course!', 'success')
    else:
        if invoice_result.get('student_invalid', False):
            flash('Invalid student information. Please contact support.', 'danger')
        else:
            flash('Failed to create the invoice. Enrollment unsuccessful.', 'danger')
    
    return redirect(url_for('course.courseView', course_id=course.id))


@app.route("/cancel/<int:course_id>", methods=["GET"])
@login_required
def cancel_enrollment(course_id):
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course.id).first()
    
    if enrollment:
        
        invoice_reference = enrollment.reference
        invoice_result = VOID_INVOICE(invoice_reference)
        
        if invoice_result["cancellation_successful"]:
            db.session.delete(enrollment)
            db.session.commit()
            flash('You have successfully canceled your enrollment in the course.', 'success')
        else:
            flash(f'Failed to cancel enrollment: {invoice_result["feedback"]}', 'danger')
    else:
        flash('You are not enrolled in this course.', 'info')
    
    return redirect(url_for('course.courseView', course_id=course.id))


@app.route("/my_courses")
@login_required
def my_courses():
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    course_ids = [enrollment.course_id for enrollment in enrollments]
    courses = Course.query.filter(Course.id.in_(course_ids)).all()
    return render_template("pages/courses.html", courses=courses)