import json
import random
from typing import List, Optional
from urllib.request import Request

from django.db.models.fields.files import ImageFieldFile
from quiz.models import Result, Topic, Word
from myproject.models import Category

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
