import pyramid.httpexceptions as exc

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
    get_games_of_user,
    get_public_games_of_user,
    get_private_games_of_user,
    get_user,
    set_user,
    set_game_with_data
)
    
from ..login_module.security import check_login
from os import path

_here = path.dirname(__file__)
_icon = open(path.join(_here, '', 'favicon.ico')).read()
_fi_response = Response(content_type='image/x-icon', body=_icon)

@view_config(route_name='favicon')
def favicon(context, request):
    response = _fi_response
    return response


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

    @view_config(route_name='user_games', renderer = 'user_games.pt')
    def user_games(self):
        login = self.logged_in
        if self.logged_in:
            all_games = get_games_of_user(login)
            all_game_records  = []

            for game in all_games:
                tags = get_tags_of_games(game.id)#[{'tag' : 'tag1'}, {'tag' : 'tag2'}, {'tag' : 'tag3'}]#None #get from DB for game
                user = get_user(game.owner_id)#None #get from DB for game
                super_tag = ""
                for tag in tags:
                    super_tag = super_tag + ';' + tag.tag
                all_game_records.append({'name' : game.game_name, 'owner' : user.user_name, 'tags' : super_tag[1:]})

            public_games = get_public_games_of_user(login)
            public_game_records = []

            for game in public_games:
                tags = get_tags_of_games(game.id)#[{'tag' : 'tag1'}, {'tag' : 'tag2'}, {'tag' : 'tag3'}]#None #get from DB for game
                user = get_user(game.owner_id)#None #get from DB for game
                super_tag = ""
                for tag in tags:
                    super_tag = super_tag + ';' + tag.tag
                public_game_records.append({'name' : game.game_name, 'owner' : user.user_name, 'tags' : super_tag[1:]})

            private_games = get_private_games_of_user(login)
            private_game_records = []

            for game in all_games:
                tags = get_tags_of_games(game.id)#[{'tag' : 'tag1'}, {'tag' : 'tag2'}, {'tag' : 'tag3'}]#None #get from DB for game
                user = get_user(game.owner_id)#None #get from DB for game
                super_tag = ""
                for tag in tags:
                    super_tag = super_tag + ';' + tag.tag
                private_game_records.append({'name' : game.game_name, 'owner' : user.user_name, 'tags' : super_tag[1:]})

            return {'all_game_records' : all_game_records, 'public_game_records' : public_game_records, 'private_game_records' : private_game_records, 'name': 'User Games View'}
        else:
            request = self.request
            return exc.HTTPFound(request.route_url("register"))   # Redirect

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
        if 'user_submit' in request.params:
            email = request.params['email']
            first_name = request.params['first_name']
            last_name  = request.params['last_name']
            nick = request.params['nick']
            password = request.params['password']
            set_user(user_name = first_name + ' ' + last_name, password = password, login = email)
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

    @view_config(route_name='add_game', renderer='creating_game.pt')
    def add_game(self):
        request = self.request
        #TO-DO: Check if user is registered
        login = ''
        game_url = request.route_url('add_game')
        referrer = request.url
        if referrer == game_url:
            referrer = '/'
        came_from = request.params.get('came_from', referrer)
        message = ''


        if 'game_submit' in request.params:
            iter = 0
            body1 = 'in_val_1_'
            body2 = 'in_val_2_'
            data = []
            while (body1 + str(iter)) in request.params:
                val1 = request.params.get(body1 + str(iter), None)
                val2 = request.params.get(body2 + str(iter), None)
                iter += 1
                if val1 is None or val2 is None:
                    message = 'All fields must be filled'
                    return {'messgae' : message}
                data.append((val1, val2))
            if len(data) > 0:
                game_name = request.params.get('game_name', '')
                set_game_with_data(game_name, 1, 0, data)
                url = request.route_url('home')
                headers = remember(request, login)
                return HTTPFound(location=url, headers=headers)
        return {'request' : request, 'came_from' : came_from}
        
    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
            headers=headers)