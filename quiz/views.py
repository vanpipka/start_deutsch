from django.http import JsonResponse
import services.quiz_services as quiz_services
from django.shortcuts import render, redirect


def test(request):

	response = JsonResponse({'result': True})
	response['Access-Control-Allow-Origin'] = '*'

	return response


def words(request):

	return render(
		request,
		'words_test.html',
		context={}
	)


def api_get_or_create_topic(request):

	response = JsonResponse({'data': quiz_services.get_or_create_topic(request)})
	response['Access-Control-Allow-Origin'] = '*'

	return response


def api_get_random_words(request):

	response = JsonResponse({'data': quiz_services.get_random_words(request)})
	response['Access-Control-Allow-Origin'] = '*'

	return response


def api_set_words_result(request):

	if request.POST.__contains__('data'):
		return JsonResponse({'status': quiz_services.set_words_result(request)})

	return redirect('/forbiden')

