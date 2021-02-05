from webapp.lesson.forms import lessonForm
from webapp.lesson.models import Lesson


blueprint = Blueprint('word', __name__)

@blueprint.route('lesson', __name__)
def lesson():
    
