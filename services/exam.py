from typing import List, Optional
from urllib.request import Request

from django.db.models.fields.files import ImageFieldFile
from exam.models import Exam, Question


def get_exam_from_request(request: Request) -> Optional[Exam]:

    exam_id = request.GET.get("id", None)
    if not exam_id:
        return None

    return Exam.get_by_id(exam_id)


def get_exam_data(request: Request) -> dict:

    return Exam.get_as_dict(get_exam_from_request(request))


def get_questions_by_exam(request: Request) -> List[dict]:

    exam = get_exam_from_request(request)

    if not exam:
        return None

    return get_questions(exam)


def get_questions(exam: Exam) -> List[dict]:

    result = []

    for q in Question.objects.filter(exam=exam).order_by("order"):
        result.append(q.get_as_dict())

    return result


def encode_img(obj) -> Optional[str]:
    """
    Extended encoder function that helps to serialize dates and images
    """
    if isinstance(obj, ImageFieldFile):
        try:
            return obj.url
        except ValueError as e:
            return ''

    raise TypeError(repr(obj) + " is not JSON serializable")
