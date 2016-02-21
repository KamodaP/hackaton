USERS = {'editor': 'editor',
	'viewer': 'viewer'}
GROUPS = {'editor': ['group:editors']}

from ..database.models import DBSession, users

def groupfinder(userid, request):
	if userid in USERS:
		return GROUPS.get(userid, [])

def check_login(userid, passwd):
    import logging
    log = logging.getLogger(__name__)
    user = DBSession.query(users).filter_by(email_addr = userid, pswd_hash = passwd).first()
    if user != None:
        log.debug('login attemt by %s with %s successfull', userid, passwd)
        return True
    else:
        log.debug('login attemt by %s with %s failed', userid, passwd)
        return False