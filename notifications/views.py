from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from notifications.models import *
from forum_notifications import *
#from forum.models import *

def ntfn_dict(ntfn):
	return {
		'id': ntfn.ntfnId,
		'module': ntfn.module,
		'url': ntfn.url,
		'app': ntfn.app		
	}

@login_required
def home(request):
	try:
		receiver = Receiver.objects.get(user=request.user)
	except Receiver.DoesNotExist:
		return HttpResponse('')

	ntfn_set = receiver.notification_set.all()
	if module = ""
	#fn = lambda ntfn: ntfn_dict(ntfn)
	data = simplejson.dumps({'ntfns': map(fn, ntfn_set)})	
	return HttpResponse(data, mimetype='application/json')
