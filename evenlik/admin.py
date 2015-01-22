# -*- encoding: utf-8 -*-

#imports from django
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from pymongo import MongoClient
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from easy_pdf.rendering import render_to_pdf_response


#imports from python
import hashlib
import json

#request.session['cart'] = "hello" -- insert
#del request.session['cart'] -- remove

def logout(request):
	del request.session['login']
	return HttpResponseRedirect("/login/")

def mainViewAdmin(request, checkin):
	if 'login' not in request.session:

		return HttpResponseRedirect("/login/")
	else:
		connection = MongoClient("localhost")

		db = connection.evenlik.users

		subscribers_db = db.find({u"present":False});
		
		subscribers_list = []
		for item in subscribers_db:
			subscribers_list.append({'name': item['name'],'email': item['email'],'id': item['id']})
			pass

		connection.close()
		return render_to_response("admin.html", {u"Checkin" : checkin,u"user" : request.session['login'],u'subscribers' : subscribers_list})



def subscribers(request):
	return mainViewAdmin(request,False)

def checkin(request):
	return mainViewAdmin(request,True)


def login(request):
	c = {}
    	c.update(csrf(request))
	if 'login' not in request.session:
		username = request.POST.get('username',False)
		password = request.POST.get('passwd',False)
		submit = request.POST.get('submit',False)
		if(submit):
			connection = MongoClient("localhost")
		
			db = connection.evenlik.admin
			user = db.find({u'user' : u'jeffersonmourak'}).distinct('user')
			passwd = db.find({u'user' : u'jeffersonmourak'}).distinct('passwd')
			connection.close()

			if(user[0] == username and passwd[0] == password):
				request.session['login'] = username
				return HttpResponseRedirect("/admin/")


			c = {u"msgError": u"usuário ou senha incorretos"}
    			c.update(csrf(request))


			return render_to_response("login.html", c)
		else:
			return render_to_response("login.html", c)
	else:

		return HttpResponseRedirect("/admin/")


def get_event_info(additional):
	connection = MongoClient("localhost")

	db = connection.evenlik.event_config

	event_configs_db = db.find({u"event_id" : 0})
	
	for item in event_configs_db:
		time_config = u"checked" if item['time'] == True else u""
		speaker_config = u"checked" if item['speaker'] == True else u""
		painelist_config = u"checked" if item['painelist'] == True else u""

	

	db = connection.evenlik.event
	dbQuery = db.find({u"event_id" : 0})
	painelist_data = dbQuery.distinct("painelist")
	speaker_data = dbQuery.distinct("speakers")
	time_data = dbQuery.distinct("time")

	days = dbQuery.distinct("event_days")

	eventName = dbQuery.distinct("event_name")[0]

	day_value = 0

	for day in days:
		day_value = day

	painelist_template = []
	speaker_template = []
	time_template = []
	for painelist in painelist_data:
		painelist_template.append(painelist)
	
	for days in time_data:
		time_template.append(days)

	for speaker in speaker_data:
		speaker_template.append(speaker)

	connection.close()
	return {u"messages" : additional,u"time" : time_template,u"event_name": eventName,u"days": day_value,u"list_speaker": speaker_template ,u"list_painelist": painelist_template ,u"Time" : time_config,u"Speaker" : speaker_config,u"Painelist" : painelist_config}

def edit_event(request):
	


	if 'login' not in request.session:
		return HttpResponseRedirect("/login/")
		
	else:
		

		c = get_event_info(False)
    		c.update(csrf(request))

		event_details = request.POST.get("save_event",False)
		event_configs = request.POST.get("save_config",False)
		if(event_configs):
			haveTime = True if request.POST.get("time",False) != False else False
			haveSpeaker = True if request.POST.get("speaker",False) != False else False
			havePainelist = True if request.POST.get("painelist",False) != False else False
			connection = MongoClient("localhost")
	
			db = connection.evenlik.event_config

			db.update({u"event_id" : 0}, {u"event_id" : 0, u"time" : haveTime, u"speaker" : haveSpeaker, u"painelist" : havePainelist});
			
			event_configs_db = db.find({u"event_id" : 0})
		
			c = get_event_info(False)
	    		c.update(csrf(request))

			connection.close()

		if(event_details):
			day_number = request.POST.get("days",False)
			event_name = request.POST.get("event_name",False)
			speakers = request.POST.getlist('speaker[]')
			painelist = request.POST.getlist('painelist[]')

			time_list = []
			print day_number
			for i in range(int(day_number)):
				time = request.POST.getlist('time['+str(i)+']')
				time_list.append(time)

			connection = MongoClient("localhost")
	
			db = connection.evenlik.event

			db.update({u"event_id" : 0}, {u"time" : time_list ,u"event_id" : 0, u"event_name" : event_name, u"event_days":day_number, u"speakers" : speakers, u"painelist" : painelist});
			
			connection.close()
			c = get_event_info({u"msg" : u"Salvo com Sucesso"})
    			c.update(csrf(request))

		return render_to_response("editor.html", c)

plaintext = get_template('email.txt')
htmly     = get_template('news_email.html')

def massMail(request):
	c = {}
    	c.update(csrf(request))
	if 'login' not in request.session:
		return HttpResponseRedirect("/login/")
	else:
		submit = request.POST.get("send",False)
		if(submit):
			subject = request.POST.get("subject","sem assunto")
			message = request.POST.get("message","sem mensagem")
			connection = MongoClient("localhost")
		
			db = connection.evenlik.users

			users = db.find({}).distinct("email")
			mailList = []
			for user in users:
				mailList.append(user)

			connection.close()
			d = Context({ 'text': message })

			subject, from_email, to = subject, 'contato@jeffersonmourak.com', mailList
			text_content = plaintext.render(d)
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, text_content, from_email, to)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
		return render_to_response("send_mail.html",c)

	return HttpResponse(u"hi")


def generatePDF(request,hash):
	connection = MongoClient("localhost")
	
	db = connection.evenlik.users

	user = db.find({u"id" : hash}).distinct("name")
	name = ""
	for data in user:
		name = data
	connection.close()
	return render_to_pdf_response(request, 'pdf_content.html', {"name":name})