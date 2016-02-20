from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from .security import groupfinder

def main(global_config, **settings):
	config = Configurator(settings=settings)
	config.include('pyramid_chameleon')
	
	#Policies
	authn_policy = AuthTktAuthenticationPolicy(settings['hackaton.secret'], 
		callback = groupfinder, hashalg='sha512')
	authz_policy = ACLAuthorizationPolicy()
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)
	
	config.add_route('home', '/')
	config.add_route('about', '/about')
	config.add_route('login', '/login')
	config.add_route('logout', '/logout')
	config.scan('.views')
		
	return config.make_wsgi_app()