from django.utils import simplejson
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	return render_to_response('ajax/test.html', context_instance = RequestContext(request))

def get_content(request, c_id):
	if request.is_ajax():
		return render_to_response('ajax/con.html', context_instance = RequestContext(request))
	else:
		return HttpResponse("Page Not Found...!!")

def get_navigation(request, c_id):
	if request.is_ajax():
		import time
		time.sleep(5)
		return render_to_response('ajax/nav.html', context_instance = RequestContext(request))
	else:
		return HttpResponse("Page Not Found!!")

def ex(var):
	return 'just for testing...'
sdkj fk jsdkfhsdkjfhkjsd
