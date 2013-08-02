from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from django.utils import simplejson
import json
from django.db.models import Max
from django.contrib.auth.models import User
from portfolio.models import PortfolioGroup, PortfolioItem, ItemMarkedUsers, Portfolio, PortfolioMarkedUsers

@login_required
def home(request, user_id):
	#print(int(user_id)+1)
	#print((request.user.pk)+2)

	if not user_id is None:
			if int(user_id) == request.user.pk:    # With an assumption that user.pk is always is of integer type.

					portfolio = Portfolio.objects.get(owner = request.user)
					plikes = portfolio.likes
					groups = PortfolioGroup.objects.filter(owner = request.user)
					items = {}
					results = {}
					for group in groups:
						items[ group.pk ] = PortfolioItem.objects.filter(group = group.pk)
						results[group.pk] = len(items[ group.pk ])
			
					data = {
					 'plikes' : plikes,
					 'groups' : groups,
					 'items' : items,
					 'results' : results,
					}	
					return render_to_response('portfolio/home.html', data, context_instance = RequestContext(request))
			else:
					other_user = get_object_or_404(User, pk = user_id)
					portfolio = Portfolio.objects.get(owner = other_user)
					plikes = portfolio.likes
					liked_users_list = PortfolioMarkedUsers.objects.filter(portfolio = portfolio, token = 1)
					plu = []
					for person in liked_users_list:
						full_name = person.user.first_name +" "+ person.user.last_name
						plu.append(full_name)

					try:
						pmu = PortfolioMarkedUsers.objects.get(portfolio = portfolio, user = request.user)
						status = pmu.token
					except PortfolioMarkedUsers.DoesNotExist:
						status = 0

					groups = PortfolioGroup.objects.filter(owner = other_user)
					items = {}
					for group in groups:
						items[ group.pk ] = PortfolioItem.objects.filter(group = group.pk)

					data = {
					 'groups' : groups,
					 'items' : items,
					 'other_user':other_user,
					 'plikes':plikes,
					 'status':status,
					 'plu':plu,
					}	
					return render_to_response('portfolio/home_other.html', data, context_instance = RequestContext(request))
							
	else: 
		return HttpResponse("Hello!!  Why are you trying to mess our website !!")

@login_required
def mark_portfolio(request, owner_id, token):     # token represents like/unlike.
	if request.user.pk != owner_id:
		if token == '1':
			owner = User.objects.get(pk = owner_id)
			portfolio = Portfolio.objects.get(owner = owner)
			obj, create = PortfolioMarkedUsers.objects.get_or_create(portfolio = portfolio, user = request.user)
			if create is True:
				obj.user = request.user
				obj.token = 1
				plikes = portfolio.likes
	                        portfolio.likes = plikes + 1
				portfolio.save()
				obj.save()
				likes = portfolio.likes
				return HttpResponse(likes)
			elif create is False and obj.token == 0:
				obj.token = 1
                                plikes = portfolio.likes
                                portfolio.likes = plikes + 1
                                portfolio.save()
                                obj.save()
                                likes = portfolio.likes
                                return HttpResponse(likes)
			else:
				return HttpResponse("You can like a portfolio only once. So kindly get out from this page :P")
		elif token == '0':
			owner = User.objects.get(pk = owner_id)
			portfolio = Portfolio.objects.get(owner = owner)
			try:
				obj = PortfolioMarkedUsers.objects.get(portfolio = portfolio, user = request.user)
				if portfolio.likes > 0: 
					if obj.token == 1:
						obj.token = 0
						plikes = portfolio.likes
						portfolio.likes = plikes - 1
						portfolio.save()
						obj.save()
						likes = portfolio.likes
						return HttpResponse(likes)
					elif obj.token == 0:
						return HttpResponse("Don't try to mess our site.")		
				else:
                                        portfolio.likes = 0
                                        portfolio.save()
					return HttpResponse(portfolio.likes)

			except PortfolioMarkedUsers.DoesNotExist:
				return HttpResponse("You are trying to unlike the portfolio that you didn't liked yet!! What a surprise!! We will look into it asap.")	
		else:
			return HttpResponse("Invalid url!! Don't try to mess our site!!")

	else:
		return HttpResponse("Sorry!!! There is no provision for a user to like his/her own portfolio in our site :P")


@login_required
def fetch_likes(request, user_id):
	user = User.objects.get(pk=user_id)
	portfolio = Portfolio.objects.get(owner = user)	
	plikes = portfolio.likes
	liked_users_list = PortfolioMarkedUsers.objects.filter(portfolio = portfolio, token = 1)

	#pitem_likes =   
	data = {}
	tmp = {}
	counter = 1
	for person in liked_users_list:
		full_name = person.user.first_name +" "+ person.user.last_name
		tmp[counter] = full_name
		counter = counter + 1

	data['pl'] = int(plikes)
	data['plu'] = tmp
	
	json_obj = {'data': data}
	return HttpResponse(json.dumps(json_obj), mimetype='application/json') 

@login_required
def mark_portfolio_item(request, item_id, token):
	#pitem = PortfolioItem.objects.get(pk = item_id)
	#if request.user.pk != owner_id:
	if token == '1':
		pitem = PortfolioItem.objects.get(pk = item_id)
		#owner = User.objects.get(pk = owner_id)
		#portfolio = Portfolio.objects.get(owner = owner)
		obj, create = ItemMarkedUsers.objects.get_or_create(item = pitem, user = request.user)
		if create is True:
			obj.user = request.user
			obj.token = 1
			plikes = pitem.likes
			pitem.likes = plikes + 1
			pitem.save()
			obj.save()
			likes = pitem.likes
			return HttpResponse(likes)
		elif create is False and obj.token == 0:
			obj.token = 1
			plikes = pitem.likes
			pitem.likes = plikes + 1
			pitem.save()
			obj.save()
			likes = pitem.likes
			return HttpResponse(likes)
		else:
			return HttpResponse("You can like a portfolio only once. So kindly get out from this page :P")
	elif token == '0':
		pitem = PortfolioItem.objects.get(pk = item_id)
		#owner = User.objects.get(pk = owner_id)
		#portfolio = Portfolio.objects.get(owner = owner)
		try:
			obj = ItemMarkedUsers.objects.get(item = pitem, user = request.user)
			if pitem.likes > 0:
				if obj.token == 1:
					obj.token = 0
					plikes = pitem.likes
					pitem.likes = plikes - 1
					pitem.save()
					obj.save()
					likes = pitem.likes
					return HttpResponse(likes)
				elif obj.token == 0:
					return HttpResponse("Don't try to mess our site.")		
			else:
				pitem.likes = 0
				pitem.save()
				return HttpResponse(pitem.likes)

		except ItemMarkedUsers.DoesNotExist:
			return HttpResponse("You are trying to unlike the portfolio that you didn't liked yet!! What a surprise!! We will look into it asap.")	
	else:
		return HttpResponse("Invalid url!! Don't try to mess our site!!")

	#else:
	#	return HttpResponse("Sorry!!! There is no provision for a user to like his/her own portfolio in our site :P")

	



@login_required
def update_groups(request): 	# Groups sorting.
	if request.is_ajax():
		keys_order = request.GET.getlist("group[]")
		
		counter = 1
		data = {}
		for group_key in keys_order:
			group = PortfolioGroup.objects.get(pk=group_key)
			group.recordlistingID = counter
			group.save()
			data[counter-1] = int(group_key)
			counter = counter + 1	

			#print(data)

		json_obj = {
		  'data' : data,
		}
		#import time
		#time.sleep(1)
		#print(json_obj)
		return HttpResponse(json.dumps(json_obj), mimetype='application/json')
	else:
		return HttpResponse("not ajax!!")

@login_required
def update_items(request): 	# Re-ordering within a group.
	if request.is_ajax():
		group_id = request.GET.get("group_id")
		items = PortfolioItem.objects.filter(group = group_id)
		keys_order = request.GET.getlist("portfolio_entry[]")
		#print(keys_order)
		counter = 1
		data = {}
		for item_key in keys_order:
			item = items.get(pk=item_key)
			item.recordlistingID = counter
			item.save()
			data[counter-1] = int(item_key)
			counter = counter + 1
		json_obj = {
		  'data':data,
		}
		return HttpResponse(json.dumps(json_obj), mimetype='application/json')		
	else:
		return HttpResponse("Not ajax!!")

@login_required
def move_items(request): # Moving an item between groups.
	if request.is_ajax():
		item_id = request.GET.get("item_id")
		to_group_id = request.GET.get("group_id")	
		
		data = {}
		item = PortfolioItem.objects.get(pk=item_id)
		item.group_id = to_group_id
		item.save()
		data['itemID'] = item_id
		data['groupID'] = to_group_id

		json_obj = {
		   'data' : data,
		}
		return HttpResponse(json.dumps(json_obj), mimetype='application/json')
	else:
		return HttpResponse('Not ajax!!')

@login_required
def add_new_item(request):
	return render_to_response('portfolio/portfolio_uploadForm.html', context_instance=RequestContext(request))

@login_required
def add_item(request):
	if request.method == "POST":
		data = request.POST.copy()			
		item = PortfolioItem(content=data['item_desc'])
		group = PortfolioGroup.objects.get(pk = data['group'])
		item.group = group
		max_listing_id = PortfolioItem.objects.filter(group=group).aggregate(Max('recordlistingID'))
		#print max_listing_id
		if max_listing_id['recordlistingID__max'] is not None:
			item.recordlistingID = int(max_listing_id['recordlistingID__max']) + 1
		else:
			item.recordlistingID = 0
		item.save()
		return HttpResponse("successfully saved via ajax!!")
	else:
		return HttpResponse("Invalid request!!")

@login_required
def edit_item(request, item_id):
	data = request.POST.copy()
	item = PortfolioItem.objects.get(pk = item_id)
	item.content = 	data['content']
	item.save()
	data = {
	  	'item.pk' : item.pk,
		'content' : item.content,       
	}
	json_obj = {
		'data' : data
	}	
	return HttpResponse(json.dumps(json_obj), mimetype='application/json')

#@login_required
#def delete_item(request, item_id):
	


@login_required
def portfolio_item(request, item_id):
	if request.is_ajax():
		item = PortfolioItem.objects.get(pk=item_id)
		data = {'item':item}
		if item.has_image == 1:
			return render_to_response('portfolio/portfolio_item_withPics.html', data, context_instance=RequestContext(request))
		else:
			return render_to_response('portfolio/portfolio_item_withOutPics.html', data, context_instance=RequestContext(request))
	else:
		return HttpResponse("Error occured while fetching data. Please try again...")




