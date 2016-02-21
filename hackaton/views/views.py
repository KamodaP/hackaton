from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
    
from pyramid.view import (
    view_config,
    view_defaults
    )

from pyramid.response import (
    Response
)

from ..database.data_source import (
    get_newes_public_games,
    get_tags_of_games,
    get_user,
    set_user
)
    
from ..login_module.security import check_login
from os import path

_here = path.dirname(__file__)
_icon = open(path.join(_here, '', 'favicon.ico'))
_fi_response = Response(content_type='image/x-icon', body=_icon)

@view_config
def favicon(request):
    response = _fi_response


@view_defaults(renderer = 'home.pt')
class CommonViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid
        
    @view_config(route_name='home')
    def home(self):
        games = get_newes_public_games()
        game_records = []

        for game in games:
            tags = get_tags_of_games(game.id)#[{'tag' : 'tag1'}, {'tag' : 'tag2'}, {'tag' : 'tag3'}]#None #get from DB for game
            user = get_user(game.owner_id)#None #get from DB for game
            super_tag = ""
            for tag in tags:
                super_tag = super_tag + ';' + tag.tag
            game_records.append({'name' : game.game_name, 'owner' : user.user_name, 'tags' : super_tag[1:]})

        return {'game_records' : game_records, 'name': 'Home View'}
        
    @view_config(route_name='about')
    def about(self):
        return {'name': 'About View'}

    @view_config(route_name = 'register', renderer = 'user_register.pt')
    def register(self):
        request = self.request
        register_url = request.route_url('register')
        referrer = request.url
        if referrer == register_url:
            referrer = '/'
        came_from = request.params.get('came_from', referrer)
        message = ''
        login = ''
        user_name = ''
        password = ''
        if 'form.submited' in request.params:
            login = request.params['login']
            user_name = request.params['user_name']
            password = request.params['password']
            set_user(user_name = user_name, password = password, login = login)
            headers = remember(request, login)
            return HTTPFound(location = came_from, headers = headers)
        return dict(
            name = 'Login',
            message = message,
            url = request.application_url + '/register',
            came_from = came_from,
            login = login,
            password = password,
        )
        
    @view_config(route_name = 'login', renderer = 'login.pt')
    def login(self):
        request = self.request
        login_url = request.route_url('login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/'
        came_from = request.params.get('came_from', referrer)
        message = ''
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
            message = message,
            url = request.application_url + '/login',
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