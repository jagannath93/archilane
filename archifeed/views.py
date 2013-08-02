from xml.etree import ElementTree
from  django.shortcuts import render_to_response
import hashlib
import datetime
import uuid
import os
from archifeed.models import ArchiFeed
#from similarity import compare
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
#haystack urls
#from haystack.query import SearchQuerySet

def data_extractor(request): 
	path = os.path.dirname(__file__)
	path = os.path.join(path, 'xml_files/')
	channel = 'international'
	#print(path)
  	#try:
	#archifeed(path, 'sports')    
	#except Exception as e:return HttpResponse(e)
#	return HttpResponse("Task completed."+ path)

#def archifeed(path, channel):
	if channel == "national":
		xml_file_path = path + 'hindu_nat.xml'
		category = channel
	if channel == "international":
		xml_file_path = path + 'hindu_int.xml'
		category = channel
	if channel == "sports":
		xml_file_path = path + 'hindu_sports.xml'
		category = channel
	if channel == "entertainment":
		xml_file_path = path + 'hindu_entertainment.xml'
		category = channel 

	xml_file = open(xml_file_path)
	tree = ElementTree.parse(xml_file)
	xml_file.close()
	root = tree.getroot()

	#print(os.getcwd())
	#os.chdir('media/news_feeds/images')
	#os.chdir('../images')
	#print(os.getcwd())
	var = 0
	afeed = []
	for item in root.iter('item'):
	
		image_path = ""
		title = item.find('title').text
		link = item.find('link').text
		des = item.find('description').text
		source = "The Hindu"
		dt = datetime.datetime.now()
		pub_date = datetime.datetime(dt.year,dt.month,dt.day)
		obj, create = ArchiFeed.objects.get_or_create(title = title)		
		if create is True:
			obj.des = des
			if image_path is not None:
				obj.image_path = image_path
				obj.has_image = True
			else:
				obj.image_path = "-"
				obj.has_image = False

			obj.channel = channel
			obj.source = source
			obj.link = link
			obj.pub_date = '2/7/2013'
			obj.save()
		else:
			continue

	return HttpResponse(link)

allowed_users = ['jaganuap', 'neel7uap']
@user_passes_test(lambda u: u.username in allowed_users)
@login_required
def archifeed(request):
	afeed = ArchiFeed.objects.all()
	feed_list = []
	for item in afeed:
		tmp = {}
		tmp['title'] = item.title
		tmp['des'] = item.des
		tmp['link'] = item.link
		tmp['source'] = item.source
		tmp['pub_date'] = item.pub_date		
		feed_list.append(tmp)
			
	#return HttpResponse(pub_date)
	return render_to_response('archifeed/index.html',{'data':afeed})

	
