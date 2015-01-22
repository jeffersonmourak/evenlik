# -*- encoding: utf-8 -*-
#27017
from django.http import HttpResponse
from pymongo import MongoClient

def index(request,user_id,user_name):
	connection = MongoClient("localhost")
	db = connection.test.posts

	db.insert({u"id": user_id, u"name": user_name});

	connection.close()
	return HttpResponse(u"O id é " + str(user_id) + u" usuario é: " +user_name)