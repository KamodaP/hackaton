from ..database.models import DBSession, users

def groupfinder(userid, request):
    user = DBSession.query(users).filter_by(email_addr = userid).first()
    if user is not None:
        return ['group:editors']

def check_login(userid, passwd):
    user = DBSession.query(users).filter_by(email_addr = userid, pswd_hash = passwd).first()
    if user != None:
        return True
    else:
        return False