from app import app
from course import course
from app.database import db
app.register_blueprint(course)


with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)