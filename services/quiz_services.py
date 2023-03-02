import json
import random
from typing import List, Optional
from urllib.request import Request

from django.db.models.functions import TruncDay
from django.db.models import Count

from services.myproject_services import get_users_info
from django.db.models.fields.files import ImageFieldFile
from quiz.models import Result, Topic, Word

WORDS_COUNT = 758


def get_or_create_topic(request: Request) -> dict:
    id = request.GET.get("id", "")
    name = request.GET.get("name", "")
    topic = {}

    if id:
        topic = Topic.get_by_id(id)
    elif name:
        topic = Topic.get_or_create_by_name(name)
    else:
        return {"error": "not enough information"}

    return topic


def get_random_words(request: Request) -> List:
    data = []
    try:
        words_count = int(request.GET.get("count", ""))
    except ValueError:
        return []

    def get_rnd_record(curr_id):

        rand_record = q[random.randint(0, words_count - 1)]
        if rand_record.id == curr_id:
            rand_record = get_rnd_record(curr_id)
        return rand_record

    position = random.randint(0, (WORDS_COUNT - words_count))
    q = Word.objects.order_by('?')[position:position + words_count]

    for w in q:
        word = {"id": w.id,
                "text": w.text,
                "translation": w.translation,
                "left": random.randint(0, 1),
                "wrong_answer": get_rnd_record(w.id).translation}

        data.append(word)

    return data


def set_words_result(request: Request) -> bool:
    result = False

    if request.POST.__contains__('data'):
        data = dict(json.loads(request.POST.__getitem__('data')))

        record = Result()

        if request.user.is_authenticated:
            record.user = request.user
        record.question_count = data.get('all', 0)
        record.right_answers = data.get('right', 0)
        record.quiz_type = "words"

        record.save()

        return True

    return result


def get_quiz_stats_by_period(request: Request) -> bool:

    q = Result.objects.all().annotate(day=TruncDay('date'))
    q = q.values("user", "day", "right_answers", "question_count")

    stats_builder = StatsBuilder(q)
    result = {"data_by_date": stats_builder.get_stat_by_period(),
              "data_by_user": stats_builder.get_stat_by_user()}

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

    def get_stat_by_user(self) -> List[dict]:

        data_map = {}
        users_set = set()

        for i in self.__dataset:

            user = i["user"]

            if user:
                users_set.add(user)

            value = data_map.get(user, None)
            if not value:
                data_map[user] = 1
            else:
                data_map[user] = value + 1

        users_info = get_users_info(users_set)

        data = [{"key": users_info.get(key, {"name": "unknown user"})["name"], "value": value} for key, value in data_map.items()]

        return data


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
