from flask import Blueprint

course = Blueprint('course', __name__)

from course import routes