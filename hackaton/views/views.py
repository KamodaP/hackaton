from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
    
from pyramid.view import (
    view_config,
    view_defaults
    )

from ..database.data_source import (
    get_newes_public_games
)
    
from ..login_module.security import check_login


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
            tags = [{'tag' : 'tag1'}, {'tag' : 'tag2'}, {'tag' : 'tag3'}]#None #get from DB for game
            user = {'user_name' : 'Marek Marecki'}#None #get from DB for game
            super_tag = ""
            for tag in tags:
                super_tag = super_tag + ';' + tag['tag']
            game_records.append({'name' : game['game_name'], 'owner' : user['user_name'], 'tags' : super_tag})

        return {'game_records' : game_records, 'name': 'Home View'}
        
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