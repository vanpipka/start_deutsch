from django.http import Http404, JsonResponse
from django.shortcuts import render
from services.exam import get_exam_data, get_questions_by_exam
from services.db_backend import get_all_category


def exam(request):

    exam_data = get_exam_data(request)

    if not exam_data:
        raise Http404("Article not found")

    return render(
        request,
        'exam.html',
        context={"article": exam_data,
                 "categories": get_all_category()}
    )


def api_get_questions_by_exam(request):
    response = JsonResponse({'data': get_questions_by_exam(request)})
    response['Access-Control-Allow-Origin'] = '*'

    return response
