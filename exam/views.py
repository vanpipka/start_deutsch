from django.http import Http404, JsonResponse, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render
from services.exam_services import get_exam_data, get_questions_by_exam, check_exam_result,\
    get_result_data, make_new_exam
from services.myproject_services import get_all_category


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


def result(request):

    result_data = get_result_data(request)

    if not result_data:
        raise Http404("Article not found")

    result_data["categories"] = get_all_category()

    return render(
        request,
        'results.html',
        context=result_data
    )


def api_get_questions_by_exam(request):
    response = JsonResponse({'data': get_questions_by_exam(request)})
    response['Access-Control-Allow-Origin'] = '*'

    return response


def api_make_exam(request):
    if request.user.is_superuser:
        return JsonResponse(make_new_exam(request))
    else:
        raise HttpResponseForbidden


def api_get_check_result(request):

    if request.method == "POST":

        data = check_exam_result(request)
        if not data:
            raise HttpResponseServerError

        response = JsonResponse({"url": data})
        response['Access-Control-Allow-Origin'] = '*'

        return response
    else:
        return Http404


