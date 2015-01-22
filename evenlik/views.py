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

#myLibs Import

from admin import get_event_info

#imports from python
import hashlib
import json

plaintext = get_template('email.txt')
htmly     = get_template('email.html')

def index(request):
	c = get_event_info(False)
    	c.update(csrf(request))
	name = request.POST.get('nome',False)
	email = request.POST.get('email',False)
	submit = request.POST.get('submit',False)

	if(submit):
		connection = MongoClient("localhost")
		
		db = connection.evenlik.users

		userhash = hashlib.sha224(email).hexdigest()

		db.insert({u"id" : userhash,u"name" : name, u"email" : email, u"present": False});

		connection.close()

		d = Context({ 'username': name })

		subject, from_email, to = 'hello', 'contato@jeffersonmourak.com', email
		text_content = plaintext.render(d)
		html_content = htmly.render(d)
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		return HttpResponse(userhash)	
	else:
		return render_to_response("index.html", c)


def confirm(request,hash):
	connection = MongoClient("localhost")
	
	db = connection.evenlik.users

	db.update({u"id" : hash}, {u"id" : hash,u"present": True});

	user = db.find({u"id" : hash});
	
	connection.close()
	return HttpResponseRedirect("/admin/checkin/")