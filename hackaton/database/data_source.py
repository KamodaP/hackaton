from .models import DBSession, data, games, users, tags, game_tag_rel, game_user_rel

#data connectios

def get_game_data(gameid):
    game_data = DBSession.query(data).filter_by(data.game_id == gameid).order_by(data.id).all()
    return game_data

def set_data(gameid, val1, val2):
    dataset = data(game_id = gameid, value_1 = val1, value_2 = val2)
    DBSession.add(dataset)
    return True

#games connections

def get_games_of_owner(ownerid):
    games_of_owner = DBSession.query(games).filter_by(games.owner_id == ownerid).all()
    return games_of_owner

def get_games_of_user(userid):
    games_of_user = DBSession.query(games).join(game_user_rel).filter_by(game_user_rel.user_id==userid).all()
    return games_of_user


def get_newes_public_games():
    newest_games = DBSession.query(games).filter_by('status==0').order_by(desc(games.id)).limit(50)
    return newest_games


#tags connections

def get_tags_of_games(gameid):
    tags_of_game = DBSession.query(tags).join(game_tag_rel).filter_by(game_tag_rel.game_id==gameid).all()
    return tags_of_game