from .models import DBSession, data, games, users, tags, game_tag_rel, game_user_rel

#user connections

def get_user(userid):
    user = DBSession.query(users).filter_by(id=userid).first()
    return user

def get_user_id_by_email(email):
    user = DBSession.query(users).filter_by(email_addr = email).first()
    return user.id

def set_user(user_name, login, password):
    user = users(user_name = user_name, email_addr = login, pswd_hash = password, respect = 0)
    DBSession.add(user)

#data connectios

def get_game_data(gameid):
    game_data = DBSession.query(data).filter_by(game_id=gameid).order_by(data.id).all()
    return game_data

def set_data(gameid, val1, val2):
    dataset = data(game_id = gameid, value_1 = val1, value_2 = val2)
    DBSession.add(dataset)

#games connections

def get_games_of_owner(ownerid):
    games_of_owner = DBSession.query(games).filter_by(owner_id=ownerid).all()
    return games_of_owner

def get_games_of_user(userid):
    games_of_user = DBSession.query(games).join(game_user_rel).filter_by(user_id=userid).all()
    return games_of_user

def get_public_games_of_user(userid):
    games_of_user = DBSession.query(games).join(game_user_rel).filter_by(user_id=userid).filter_by(status=0).all()
    return games_of_user

def get_private_games_of_user(userid):
    games_of_user = DBSession.query(games).join(game_user_rel).filter_by(user_id=userid).filter_by(status=1).all()
    return games_of_user

def get_game_by_id(gameid):
    game = DBSession.query(games).filter_by(id = gameid).first()
    return game

def get_newes_public_games():
    newest_games = DBSession.query(games).filter_by(status=0).order_by(games.id.desc()).limit(50)
    return newest_games

def set_game(game_name, owner_id, status):
    game = games(game_name = game_name, owner_id = owner_id, status = status)
    DBSession.add(game)


def set_game_with_data(game_name, owner_id, status, data):
    game = games(game_name = game_name, owner_id = owner_id, status = status)
    DBSession.add(game)
    DBSession.flush()
    game_id = game.id
    
    import logging
    log = logging.getLogger(__name__)
    log.debug('Id: %s', game_id)
    for (val1, val2) in data:
        set_data(game_id, val1, val2)


#tags connections

def get_tags_of_games(gameid):
    tags_of_game = DBSession.query(tags).join(game_tag_rel).filter_by(game_id=gameid).all()
    return tags_of_game