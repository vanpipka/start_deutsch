import json
from typing import List, Optional
from urllib.request import Request

from django.db.models.fields.files import ImageFieldFile
from django.db.models.functions import TruncDay

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
    img_path = os.path.join(exam_name, "img")

    audio = ""
    questions = []

    for root, dirs, files in os.walk(path):
        for filename in files:
            file_data = filename.split(".")
            if file_data[-1] == "mp3":
                audio = os.path.join(exam_name, filename)
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
        question.section = Section.get_by_id(SERVICES_IDS.get(f"{exam_name.split(' ')[0]}_{part}"))
        question.order = number
        question.right_answer = answer
        question.image = q.get("file", "")
        question.save()

    return {"id": exam.id}


def get_result_data(request: Request) -> Optional[dict]:
    return Result.get_by_try(request.GET.get("id", None))


def get_exam_stats_by_period(request: Request) -> dict:

    q = Result.objects.all().annotate(day=TruncDay('date'))
    q = q.values("try_id", "day").distinct()

    stats_builder = StatsBuilder(q)
    result = {"data_by_date": stats_builder.get_stat_by_period(),
              "data_by_user": []}  # stats_builder.get_stat_by_user()}

    return result


class StatsBuilder:

    def __init__(self, query):
        self.query = query
        self.__dataset = []

        self.__make_dataset()

    def __make_dataset(self) -> List:
        if not self.__dataset:
            self.__dataset = list(self.query)

    def get_stat_by_period(self) -> List[dict]:

        data_map = {}

        for i in self.__dataset:
            day = i["day"]
            value = data_map.get(day, None)
            if not value:
                data_map[day] = 1
            else:
                data_map[day] = value + 1

        data = [{"key": key, "value": value} for key, value in data_map.items()]

        return sorted(data, key=lambda x: x["key"])


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
