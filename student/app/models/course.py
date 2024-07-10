from app.database import db



enrollments = db.Table('enrollments',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    enrolled_users = db.relationship('User', secondary=enrollments, backref=db.backref('courses', lazy='dynamic'))

    def __repr__(self):
        return f'<Course {self.title}>'


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    reference = db.Column(db.String(150), nullable=True)

    user = db.relationship('User', backref=db.backref('enrollments', lazy=True))
    course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))

    def __repr__(self):
        return f'<Enrollment {self.user.username} in {self.course.title}>'