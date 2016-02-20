from pyramid.authentication import AuthTktAuthenyicationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from .security import groupfinder

def main(global_config, **settings):
	config = Configurator(settings=settings)
	config.include('pyramid_chameleon')
	
	#Policies
	authn_policy = AuthTktAuthenyicationPolicy()
	authz_policy = ACLAuthorizationPolicy()
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)
	
	return config.make_wsgi_app()