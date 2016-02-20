from .models import DBSession, data, games, users

def get_game_data(gameid):
    game_data = DBSession.query(data).filter_by(game_id == gameid).order_by(data.id).all()
    return game_data

def set_data(gameid, val1, val2):
    dataset = data(game_id = gameid, value_1 = val1, value_2 = val2)
    DBSession.add(dataset)
    return True

def get_user_games(ownerid):
    games_names = DBSession.fliter_by(owner_id == ownerid).all()
    return games_names

