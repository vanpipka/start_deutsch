import json
from typing import List, Optional
from urllib.request import Request

from django.db.models.fields.files import ImageFieldFile
from exam.models import Exam, Question, Result, Section
import uuid


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


def check_exam_result(request: Request) -> Optional[str]:
    if not request.POST.__contains__('data'):
        return None

    try_id = uuid.uuid4()

    data = json.loads(request.POST.__getitem__('data'))
    exam = Exam.get_by_id(data["exam"])

    if not exam:
        return None

    for i in data["questions"]:
        record = Result()
        if request.user.is_authenticated:
            record.user = request.user

        record.try_id = try_id
        record.exam = exam
        record.answer = i["answer"]
        record.question = Question.get_by_id(i["id"])

        record.save()

    return "/exam/result/?id=" + str(try_id)


def make_new_exam(request: Request) -> Optional[dict]:
    from services.constants import SERVICES_IDS
    from myproject.settings import MEDIA_ROOT
    import os

    exam_name = request.GET.get("name", "")
    if not exam_name:
        return {"error": "exam name not specified"}

    if Exam.objects.filter(name=exam_name).exists():
        return {"error": "exam exists"}

    path = os.path.join(MEDIA_ROOT, exam_name)
    img_path = os.path.join(path, "img")

    audio = ""
    questions = []

    for root, dirs, files in os.walk(path):
        for filename in files:
            file_data = filename.split(".")
            if file_data[-1] == "mp3":
                audio = os.path.join(path, filename)
            elif file_data[-1] == "png":
                questions.append({"name": file_data[0],
                                  "file": os.path.join(img_path, filename)})

    exam = Exam(name=exam_name, title=exam_name)
    if audio:
        exam.audio = audio
    exam.save()

    for q in questions:
        _, number, part, answer = q.get("name", "").split("-")

        question = Question()
        question.exam = exam
        question.section = Section.get_by_id(SERVICES_IDS.get(f"horen_{part}"))
        question.order = number
        question.right_answer = answer
        question.image = q.get("file", "")
        question.save()

    return {"id": exam.id}


def get_result_data(request: Request) -> Optional[dict]:
    return Result.get_by_try(request.GET.get("id", None))


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
