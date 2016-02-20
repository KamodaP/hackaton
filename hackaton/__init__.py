from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .security import groupfinder

from scripts.models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
	
	#Policies
	authn_policy = AuthTktAuthenticationPolicy(settings['hackaton.secret'], 
		callback = groupfinder, hashalg='sha512')
	authz_policy = ACLAuthorizationPolicy()
	config.set_authentication_policy(authn_policy)
	config.set_authorization_policy(authz_policy)
	
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
	config.add_route('about', '/about')
	config.add_route('login', '/login')
	config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
