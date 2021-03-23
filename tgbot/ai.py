import psycopg2, random, string, logging
from tgbot.config import db_setup
from psycopg2 import sql
from pprint import pprint
from datetime import datetime

now = datetime.now()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class codegenerator:
    def gencode(stringLength):
        lettersAndDigits = string.ascii_letters + string.digits
        return str(''.join(random.choice(lettersAndDigits) for i in range(stringLength)))

class dbconnect:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(db_setup)
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except:
            pprint("Cannot connect to database")


    def ismemberbyid(self, userid):
        col0 = sql.Identifier('userid')
        col1 = sql.Identifier('username')
        col2 = sql.Identifier('first_name')
        col3 = sql.Identifier('last_name')
        self.userid = userid
        self.cur.execute(
            sql.SQL("select {} from  bfrvschema.members where userid =%s and is_ingroup = True").format(col0),
                (self.userid,)
            )
        member = self.cur.fetchone()
        if member is None:
            return False
        else:
            return member[0]


    def ismemberbyusername(self, username):
        col0 = sql.Identifier('userid')
        col1 = sql.Identifier('username')
        col2 = sql.Identifier('first_name')
        col3 = sql.Identifier('last_name')

        self.username = username
        self.cur.execute(
            sql.SQL("select {}, {} from  bfrvschema.members where username =%s and is_ingroup = True").format(col1, col0),
                (self.username,)
            )
        member = self.cur.fetchone()
        if member is None:
            return False
        else:
            return member

    def getmemberprofileinfo(self, userid):
        memberid = sql.Identifier('userid')
        username = sql.Identifier('username')
        first_name = sql.Identifier('first_name')
        last_name = sql.Identifier('last_name')
        proof_of_id = sql.Identifier('proof_of_id')
        valid_id = sql.Identifier('valid_id')
        referrer_username = sql.Identifier('referrer_username')
        verifier_username = sql.Identifier('verifier_username')        
        self.userid = userid

        self.cur.execute(
            sql.SQL("select {}, {}, {}, {}, {}, {}, {}, {} from  bfrvschema.members where userid =%s and is_ingroup = True").format(memberid, username, first_name, last_name, proof_of_id, valid_id, referrer_username, verifier_username),
                (self.userid,)
            )
        member = self.cur.fetchone()
        if member is None:
            return False
        else:
            return member


    def update_basicinfo(self, userid, username, first_name, last_name):
        self.userid = userid
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        # self.photo_id = photo_id
        self.last_update_date = now
        update_sql = "UPDATE bfrvschema.members SET username=%s, first_name=%s, last_name=%s, last_update_date = %s where userid =%s"
        self.cur.execute(
            sql.SQL(update_sql), (self.username, self.first_name, self.last_name,  self.last_update_date, self.userid,)
            )
        logger.info(
            "{}: in update_basic_info successful update of members".format(self.username,)
            )
        return True

    def count_members_table(self):
        self.cur.execute(
            sql.SQL("select count(userid) from  bfrvschema.members"),
            )
        member = self.cur.fetchone()
        logger.info(
            "in count_members_table"
            )
        if member is None:
            return False
        else:
            return member

    def get_members_for_deletion(self, id_list):
        memberid = sql.Identifier('userid')

        self.cur.execute(
            sql.SQL("select userid from  bfrvschema.members where userid NOT IN %(id_list)s"),
            {'id_list':tuple(id_list),}
            )
        member = self.cur.fetchall()
        logger.info(
            "in get_members_for_deletion"
            )
        if member is None:
            return False
        else:
            return member

    def delete_members(self, id_list):
        # self.username = str(username)
        try:
            delete_sql = "DELETE FROM  bfrvschema.members WHERE userid IN %(id_list)s"
            self.cur.execute(
                sql.SQL(delete_sql), {'id_list':tuple(id_list),}
                )
            logger.info(
                "successful delete from members"
                )
            return True
        except Exception as e:
            return False
            raise




    def isapproved_notjoined(self, userid):
        col0 = sql.Identifier('userid')
        col1 = sql.Identifier('username')
        col2 = sql.Identifier('first_name')
        col3 = sql.Identifier('last_name')
        self.userid = userid
        self.cur.execute(
            sql.SQL("select {} from  bfrvschema.members where userid =%s and (is_ingroup is null or is_ingroup = False)").format(col0),
                (self.userid,)
            )
        member = self.cur.fetchone()
        if member is None:
            return False
        else:
            return member[0]


    def isjoinerbyid(self, joinerid):
        self.joinerid = joinerid
        col0 = sql.Identifier('joinerid')
        col1 = sql.Identifier('username')
        col2 = sql.Identifier('first_name')
        col3 = sql.Identifier('last_name')
        col4 = sql.Identifier('verifier_id')
        col5 = sql.Identifier('referrer_username')
        col6 = sql.Identifier('verifier_username')
        col7 = sql.Identifier('proof_of_id')
        col8 = sql.Identifier('valid_id')

        self.cur.execute(
            sql.SQL("select {}, {}, {}, {}, {}, {}, {}, {}, {} from  bfrvschema.joiners where joinerid =%s and is_submitted = True").format(col0, col1, col2, col3, col4, col5, col6, col7, col8),
                (self.joinerid,)
            )
        member = self.cur.fetchone()
        if member is None:
            return False
        else:
            return member


    def istemp_joinerbyid(self, joinerid):
        self.joinerid = joinerid
        col0 = sql.Identifier('joinerid')
        col1 = sql.Identifier('username')
        col2 = sql.Identifier('first_name')
        col3 = sql.Identifier('last_name')
        col4 = sql.Identifier('verifier_id')
        self.cur.execute(
            sql.SQL("select {}, {}, {}, {}, {} from  bfrvschema.joiners where joinerid =%s and is_submitted = False").format(col0, col1, col2, col3, col4),
                (self.joinerid,)
            )
        member = self.cur.fetchone()
        if member is None:
            return False
        else:
            return member

    def closedbconnection(self):
        self.cur.close()
        self.conn.close()           


    def getrefcodebyusername(self, joiner_username):
        col0 = sql.Identifier('refcode')
        col1 = sql.Identifier('admin_username')
        col2 = sql.Identifier('adminid')
        col3 = sql.Identifier('referrer_username')
        col4 = sql.Identifier('referrerid')

        
        self.cur.execute(
            sql.SQL("select {},{},{},{},{} from  bfrvschema.refcode where joiner_username =%s and is_active = True").format(col0, col1, col2, col3, col4),
                (joiner_username,)
            )
        refcode = self.cur.fetchone()
              
        if refcode is None:
            return False
        else:
            return refcode


    def new_refcode_byusername(self, joiner_username, codelen, adminid, adminusername, joinerid, referrer_username, referrerid):
        self.new_code = codegenerator.gencode(codelen)
        self.admin_id = adminid
        self.admin_username = adminusername
        self.joiner_id = joinerid
        self.joiner_username = joiner_username
        self.date_generated = now
        self.date_expiry = now
        self.is_active = True
        self.last_update_date = now
        self.referrer_username = referrer_username
        self.referrer_id = referrerid

        insert_sql ="INSERT INTO bfrvschema.refcode (refcode, adminid, admin_username, joinerid, joiner_username, date_generated, date_expiry, is_active, last_update_date, referrer_username, referrerid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cur.execute(
            sql.SQL(insert_sql), (self.new_code, self.admin_id, self.admin_username, self.joiner_id, self.joiner_username, self.date_generated, self.date_expiry, self.is_active, self.last_update_date, self.referrer_username, self.referrer_id)
            )
        return self.new_code


    def update_refcode_byusername(self, joiner_username, len, adminid, adminusername, joinerid, referrer_username, referrerid):
        new_code = codegenerator.gencode(len)
        date_generated = now
        update_sql = "UPDATE bfrvschema.refcode SET refcode=%s, adminid=%s, admin_username=%s, joinerid=%s, referrer_username=%s, referrerid=%s, is_active = True, date_generated = %s WHERE joiner_username=%s"
        self.cur.execute(
            sql.SQL(update_sql), (new_code, adminid, adminusername, joinerid, referrer_username, referrerid, date_generated, joiner_username)
            )
        return new_code

    def delete_refcode_byusername(self, username):
        self.username = str(username)
        delete_sql = "DELETE FROM  bfrvschema.refcode WHERE joiner_username=%s"
        self.cur.execute(
            sql.SQL(delete_sql), (self.username,)
            )
        logger.info(
            "{}: successful delete from refcode".format(self.username,)
            )
        return True

    def add_joiner_table(self, joinerid, username, first_name, last_name, photo_id, admin_username, admin_userid, referrer_username, referrer_id, valid_id): 
        self.joinerid = joinerid
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo_id = photo_id
        self.is_driver = False
        self.is_passenger = False
        self.proof_of_id = None
        self.points_total = 0
        self.referrer_id = referrer_id
        self.referrer_username = referrer_username
        self.verifier_id = admin_userid
        self.verifier_username = admin_username
        self.date_verified = None
        self.is_submitted = False
        self.is_ingroup = False
        self.last_update_date = now
        self.valid_id = valid_id 
 
        insert_sql ="INSERT INTO bfrvschema.joiners VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cur.execute(
            sql.SQL(insert_sql), (self.joinerid, self.username, self.first_name, self.last_name, self.photo_id, self.is_driver, self.is_passenger, self.proof_of_id, self.points_total, self.referrer_id, self.referrer_username, self.verifier_id, self.verifier_username, self.date_verified, self.is_submitted, self.is_ingroup, self.last_update_date, self.valid_id )
            )

        return True

    def get_joinersby_approver(self, approverid):
        col0 = sql.Identifier('joinerid')
        col1 = sql.Identifier('username')
        col2 = sql.Identifier('referred_by')

        self.verified_by = str(approverid)

        self.cur.execute(
            sql.SQL("select {},{},{} from  bfrvschema.joiners where verifier_id =%s and date_verified is %s ").format(col0, col1, col2),
                (self.verifier_id, None)
            )
        joiner = self.cur.fetchall()
              
        if joiner is None:
            return False
        else:
            return joiner
        return True

    def get_joinerby_username(self, username):
        self.username = username

        self.cur.execute(
            sql.SQL("select * from  bfrvschema.joiners where username =%s and date_verified is %s "),
                (self.username, None)
            )
        joiner = self.cur.fetchone()
              
        if joiner is None:
            return False
        else:
            return joiner
        return True

    def update_joiner_submit(self, joinerid):
        self.last_update_date = now
        self.joinerid = joinerid
        update_sql = "UPDATE bfrvschema.joiners SET is_submitted = True, last_update_date = %s WHERE joinerid=%s"
        self.cur.execute(
            sql.SQL(update_sql), (self.last_update_date, self.joinerid)
            )
        logger.info(
            "{}: successful update to joiners set submitted".format(self.joinerid)
            )
        return True

    def update_joiner_poid(self, joinerid, proof_of_id):
        self.last_update_date = now
        self.joinerid = joinerid
        self.proof_of_id = str(proof_of_id)

        update_sql = "UPDATE bfrvschema.joiners SET proof_of_id = %s, last_update_date = %s WHERE joinerid=%s"
        
        self.cur.execute(
            sql.SQL(update_sql), (self.proof_of_id, self.last_update_date, self.joinerid)
            )
        logger.info(
            "{}: successful update to joiners set proof_of_id".format(self.joinerid)
            )
        return True

    def update_joiner_valid_id(self, joiner_id, valid_id):
        self.last_update_date = now
        self.joinerid = joiner_id
        self.valid_id = valid_id
        #CHAT_government_id_<PHOTO_ID>
        update_sql = "UPDATE bfrvschema.joiners SET last_update_date = %s, valid_id =%s WHERE joinerid=%s"
        self.cur.execute(
            sql.SQL(update_sql), (self.last_update_date, self.valid_id, self.joinerid,)
            )
        logger.info(
            "{}: successful update to joiners set valid_id".format(self.joinerid)
            )
        return True



    def update_joiner_referrer(self, joinerid, referrer_username, referrer_id):
        self.last_update_date = now
        self.joinerid = joinerid
        self.referrer_username = referrer_username
        self.referrer_id = referrer_id

        update_sql = "UPDATE bfrvschema.joiners SET referrer_username = %s, referrer_id = %s last_update_date = %s WHERE joinerid=%s"
        self.cur.execute(
            sql.SQL(update_sql), (self.referrer_username, self.last_update_date, self.referrer_id, self.joinerid)
            )
        logger.info(
            "{}: successful update to joiners set referrer".format(self.joinerid)
            )
        return True

    def delete_joiner(self, joinerid):
        self.joinerid = joinerid
        delete_sql = "DELETE from bfrvschema.joiners WHERE joinerid=%s"
        self.cur.execute(
            sql.SQL(delete_sql), (self.joinerid,)
            )
        logger.info(
            "{}: successful delete from joiners".format(self.joinerid)
            )
        return True

    def delete_joiner_byusername(self, username):
        self.username = username
        delete_sql = "DELETE from bfrvschema.joiners WHERE username=%s"
        self.cur.execute(
            sql.SQL(delete_sql), (self.username,)
            )
        logger.info(
            "{}: successful delete from joiners".format(self.username)
            )
        return True

    def delete_member_byusername(self, username):
        self.username = username
        delete_sql = "DELETE from bfrvschema.members WHERE username=%s"
        self.cur.execute(
            sql.SQL(delete_sql), (self.username,)
            )
        logger.info(
            "{}: successful delete from members".format(self.username)
            )
        return True


    def add_member_table(self, joinerid, username, first_name, last_name, photo_id, referrer_id, referrer_username, admin_userid, verifier_username, valid_id, proof_of_id, is_ingroup): 
        self.userid = joinerid
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo_id = photo_id
        self.is_driver = False
        self.is_passenger = False
        self.proof_of_id = proof_of_id
        self.points_total = None
        self.follower_allowed_dr = False
        self.follower_allowed_ps = False
        self.following_allowed = False
        self.check_member_allowed = False
        self.referrer_id = referrer_id
        self.referrer_username = referrer_username
        self.verifier_id = admin_userid
        self.verifier_username = verifier_username
        self.date_verified = now
        self.is_ingroup = is_ingroup
        self.last_update_date = now
        self.valid_id = None
        self.valid_id = valid_id

        insert_sql ="INSERT INTO bfrvschema.members VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s)"
        self.cur.execute(
            sql.SQL(insert_sql), (self.userid, self.username, self.first_name, self.last_name, self.photo_id, self.is_driver, self.is_passenger, self.proof_of_id, self.points_total, self.follower_allowed_dr, self.follower_allowed_ps, self.following_allowed, self.check_member_allowed, self.referrer_id, self.referrer_username, self.verifier_id, self.verifier_username, self.date_verified, self.is_ingroup, self.last_update_date, self.valid_id)
            )
        logger.info(
            "{}: successful adding to members".format(self.username,)
            )
        return True

    def update_member_joined(self, member_id):
        self.last_update_date = now
        self.userid = member_id
        update_sql = "UPDATE bfrvschema.members SET last_update_date = %s, is_ingroup = True WHERE userid=%s"
        self.cur.execute(
            sql.SQL(update_sql), (self.last_update_date, self.userid,)
            )
        logger.info(
            "{}: successful update to members set is_ingroup to true".format(self.userid)
            )
        return True

    def update_member_left(self, member_id):
        self.last_update_date = now
        self.userid = member_id
        update_sql = "UPDATE bfrvschema.members SET last_update_date = %s, is_ingroup = False WHERE userid=%s"
        self.cur.execute(
            sql.SQL(update_sql), (self.last_update_date, self.userid,)
            )
        logger.info(
            "{}: successful update to members set is_ingroup to false".format(self.userid)
            )
        return True

    def update_member_referrer(self, member_id, referrer_id, referrer_username):
        self.last_update_date = now
        self.userid = member_id
        self.referrer_id = referrer_id
        self.referrer_username = referrer_username
        update_sql = "UPDATE bfrvschema.members SET last_update_date = %s, referrer_id = %s, referrer_username =%s WHERE userid=%s"
        self.cur.execute(
            sql.SQL(update_sql), (self.last_update_date, self.referrer_id, self.referrer_username, self.userid,)
            )
        logger.info(
            "{}: successful update to members set referrer".format(self.userid)
            )
        return True

    def update_member_poid(self, member_id, proof_of_id):
        self.last_update_date = now
        self.userid = member_id
        self.proof_of_id = proof_of_id
        update_sql = "UPDATE bfrvschema.members SET last_update_date = %s, proof_of_id =%s WHERE userid=%s"
        self.cur.execute(
            sql.SQL(update_sql), (self.last_update_date, self.proof_of_id, self.userid,)
            )
        logger.info(
            "{}: successful update to members set proof_of_id".format(self.userid)
            )
        return True


    def update_member_valid_id(self, member_id, valid_id):
        self.last_update_date = now
        self.userid = member_id
        self.valid_id = valid_id
        #CHAT_government_id_<PHOTO_ID>
        update_sql = "UPDATE bfrvschema.members SET last_update_date = %s, valid_id =%s WHERE userid=%s"
        self.cur.execute(
            sql.SQL(update_sql), (self.last_update_date, self.valid_id, self.userid,)
            )
        logger.info(
            "{}: successful update to members set valid_id".format(self.userid)
            )
        return True