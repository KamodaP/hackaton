﻿from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
	remember,
	forget,
	)
	
from pyramid.view import (
	view_config,
	view_defaults
	)
	
from ..login_module.security import check_login


@view_defaults(renderer = 'home.pt')
class CommonViews:
	def __init__(self, request):
		self.request = request
		self.logged_in = request.authenticated_userid
		
	@view_config(route_name='home')
	def home(self):
		return {'name': 'Home View'}
		
	@view_config(route_name='about')
	def about(self):
		return {'name': 'About View'}
		
	@view_config(route_name = 'login', renderer = 'login.pt')
	def login(self):
		request = self.request
		login_url = request.route_url('login')
		referrer = request.url
		if referrer == login_url:
			referrer = '/'
		came_from = request.params.get('came_from', referrer)
		massege = ''
		login = ''
		password = ''
		if 'form.submitted' in request.params:
			login = request.params['login']
			password = request.params['password']
			if check_login(login, password) == True:
				headers = remember(request, login)
				return HTTPFound(location = came_from,
					headers=headers)
			message = 'Failed login'
		return dict(
			name = 'Login',
			massage = message,
			url = requuest.application_url + '/login',
			came_from = came_from,
			login = login,
			password = password,
		)
		
	@view_config(route_name='logout')
	def logout(self):
		request = self.request
		headers = forget(request)
		url = request.route_url('home')
		return HTTPFound(location=url,
			headers=headers)