import json
import random

from django.db.models.fields.files import ImageFieldFile
from quiz.models import Question, Result, Topic, Word
from myproject.models import Category


def make_new_questions_set(request):

    question_set: list = []
    category = Category.get_by_id(request.GET.get("category", ""))

    if category is None:
        return question_set

    question_query = Question.objects.all().filter(category=category)

    for question_obj in question_query:

        question = {'id': question_obj.id,
                    'text': question_obj.text,
                    'image': encode_img(question_obj.image)}
        answers_list = []
        order = 1
        answers_query = question_obj.answer_set.all()

        for answer_obj in answers_query:

            answers_list.append({'order': order,
                                 'id': answer_obj.id,
                                 'correct': answer_obj.itsRight,
                                 'text': answer_obj.text,
                                 'image': encode_img(answer_obj.image)})
            order += 1

            if answer_obj.itsRight:
                question['correct'] = answer_obj.id

        question['answers'] = answers_list
        question_set.append(question)

    return question_set


def get_or_create_topic(request):

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


def get_random_words(request):

    data = []
    try:
        words_count = int(request.GET.get("count", ""))
    except:
        return []

    def get_rnd_record(curr_id):

        rand_record = q[random.randint(0, words_count-1)]
        if rand_record.id == curr_id:
            rand_record = get_rnd_record(curr_id)
        return rand_record

    # print(Word.objects.all().count()) = 758
    position = random.randint(0, (758-words_count))
    q = Word.objects.order_by('?')[position:position+words_count]

    for w in q:

        word = {"id": w.id,
                     "text": w.text,
                     "translation": w.translation,
                     "left": random.randint(0, 1),
                     "wrong_answer": get_rnd_record(w.id).translation}

        data.append(word)

    return data


def set_words_result(request):

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


def encode_img(obj):
    """
    Extended encoder function that helps to serialize dates and images
    """
    if isinstance(obj, ImageFieldFile):
        try:
            return obj.url
        except ValueError as e:
            return ''

    raise TypeError(repr(obj) + " is not JSON serializable")