from django.http import HttpResponse
from django.shortcuts import render_to_response

def home(request): 
    render_to_response('resources/home.html')
def FileHandler(request):
    if request.method == 'POST':
        for field_name in request.FILES:
            uploaded_file = request.FILES[field_name]

            # write the file into /tmp
	    import os
            from django.conf import settings
            destination_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            destination = open(destination_path, 'wb+')
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
            destination.close()

        # indicate that everything is OK for SWFUpload
        return HttpResponse("ok", mimetype="text/plain")

    else:
        # show the upload UI
        return HttpResponse("error occured!!")
