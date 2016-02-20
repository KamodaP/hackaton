USERS = {'editor': 'editor',
	'viewer': 'viewer'}
GROUPS = {'editor': ['group:editors']}

from ..database.model import DBSession, users

def groupfinder(userid, request):
	if userid in USERS:
		return GROUPS.get(userid, [])

def check_login(userid, passwd):
    user = BDSession.query(users).filter_by(email_addr = userid, pswd_hash = passwd).first()
    if user != None:
        return True
    else:
        return False