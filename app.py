#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging, os, telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from tgbot.config import mode, bot_token, HEROKU_APP_NAME, NGROK_APP_NAME, ADMIN_CHAT_GROUP_ID, MEMBERS_CHAT_GROUP_ID, ADMIN_VALIDID_CHAT\
    ,MSG_START_CHECKPROFILE_MISSING, MSG_START_EXISTMEMBER, MSG_START_PENDINGMEMBER, MSG_JOINER_OPTIONS, MSG_MEMBER_OPTIONS\
    ,MSG_MEM_REFERJOINER\
    ,MSG_INPUT_OTREFCODE, MSG_CORRECTREFCODE, MSG_REENTER_REFCODE\
    ,MSG_END_CONV, MSG_CHECKPROFILE_MISSING, MSG_CHECKPROFILE_COMPLETE\
    ,MSG_TOJOINER_PROFILESUBMIT, MSG_TOADMINS_PROFILESUBMIT, MSG_TOAPPROVER_PROFILESUBMIT\
    ,MSG_APPROVER_APPROVE,MSG_APPROVER_REJECTED, MSG_TOADMINS_JOINER_APPROVED, MSG_TOADMINS_JOINER_REJECTED, MSG_TOJOINER_INVITEBUTTON, MSG_TOJOINER_REJECTED\
    ,MSG_TONEWMEMBER_WELCOME, MSG_TOADMINS_NEWMEMBER,MSG_TOMEMBERS_NEWMEMBER, MSG_TOADMINS_UNKOWNJOINER, MSG_TOJOINER_UNKOWNJOINER, MSG_TOADMINS_LEFTMEMBER\
    ,MSG_RULES, MSG_HELP, MSG_UPDATE_REFCODE, MSG_NEW_REFCODE, MSG_REFCODE_INVALID_REFERRER\
    ,MSG_TOREF_REQCODE, MSG_TOADM_REQCODE, MSG_TOADM_RUPDATE_REFCODE, MSG_TOREF_RUPDATE_REFCODE, MSG_TOADM_RNEW_REFCODE, MSG_TOREF_RNEW_REFCODE, MSG_RREFCODE_INVALID_REFERRER\
    ,MSG_TOADM_RREFCODE_REJ, MSG_TOREF_RREFCODE_REJ, dev_chat_id, refcode_length
from tgbot.ai import codegenerator, dbconnect
# from tgbot.bfrvmemberupdate import telethonClientConnect
from telegram.ext.dispatcher import run_async
from pprint import pprint
from functools import wraps

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

#develover chat id whitelisted, remove for prod
jmj_chat_id = dev_chat_id
codelen = refcode_length

# Stages - States - Group of handlers to be active 
MEMBER_MENU, CHECK_RCODE, JOINER_MENU, CHECKCODE, RETRYCODE, CHECK_PROFILE, CHECK_REFERRER, CHECK_DOC, CHECK_VALID_ID, UPDATE_MEMBER_MENU = range(10)
# Callback data
CHECK_JOINER_PROFILE, END, RETRY, CANCEL, SUBMIT, APPROVE_JOINER, REJECT_JOINER, ADD_AS_MEMBER\
,JOIN_GROUP, REQUEST_TO_JOIN, ENTER_CODE\
,REFER_MEMBER, SEND_RCODE, REJECT_RCODE, RULES\
,ADD_REFERRER, ADD_VALIDATING_DOC, SEND_VALID_ID, UPDATE_MEMBER_MENU = range(19)

#ADMIN_CHAT_GROUP_ID = jmj_chat_id
# mode = os.getenv("MODE")
MODE = mode
TOKEN = bot_token
bot = telegram.Bot(TOKEN)

if MODE == "dev":
    PORT = "80"
    DOMAIN = ".ngrok.io/"
    APP_NAME = NGROK_APP_NAME

elif MODE == "prod":
    # PORT = "8443"
    PORT = int(os.environ.get("PORT", "8443"))
    DOMAIN = ".herokuapp.com/"
    APP_NAME = HEROKU_APP_NAME

else:
    logger.error("No MODE specified!")
    sys.exit(1)


def run(updater):
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    s = updater.bot.set_webhook("https://{}{}{}".format(APP_NAME,DOMAIN,TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

LIST_ADMIN_MEMBER_MGT = [340959814, 381947529, 518176853, 364364393, 395077750, 599281804, dev_chat_id]
#paulinetornito, aub_reee, carloliveta, FayeCarmona, Avelaiz, mackyclavero


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_ADMIN_MEMBER_MGT:
            logger.error("Unauthorized access denied for {}.!").format(user_id)
            return
        return func(update, context, *args, **kwargs)
    return wrapped



@run_async
def rules(update, context):
    chat_type = update.message.chat.type
    user = update.message.from_user.first_name
    userid = update.message.from_user.id

    try:
        if chat_type == 'private':
            logger.info(
                "/rules command triggered by {} with userid: {} in private message with bot".format(user, userid)
                )
            db_conn = dbconnect()
            is_member = db_conn.ismemberbyid(userid)
            if is_member:
                update.message.reply_text(
                    MSG_RULES
                    )
            else:
                is_pending_member = db_conn.isjoinerbyid(userid)
                if is_pending_member:
                    update.message.reply_text(
                        MSG_RULES
                        )                                   
                else:
                    pass
            db_conn.closedbconnection()
        else:
            logger.info(
                 "/rules command triggered by {} with userid: {} in group chat".format(user, userid)
                )
            update.message.reply_text(
                MSG_RULES
                )
            bot.send_message(
                chat_id= userid, 
                text= MSG_RULES,
                )

    except Exception as e:
        db_conn.closedbconnection()
        raise



@run_async
def rules_m(update, context):
    query = update.callback_query
    chat_type = query.message.chat.type
    user = query.message.chat.username
    userid = query.message.chat.id

    # print(query)
    try:
        if chat_type == 'private':
            logger.info(
                "/rules command triggered by {} with userid: {} in private message with bot".format(user, userid)
                )
            db_conn = dbconnect()
            is_member = db_conn.ismemberbyid(userid)
            if is_member:
                bot.edit_message_text(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text= MSG_RULES,
                    parse_mode= 'HTML')
                # query.message.reply_text(
                #     MSG_RULES
                #     )
            else:
                is_pending_member = db_conn.isjoinerbyid(userid)
                if is_pending_member:
                    bot.edit_message_text(
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text= MSG_RULES,
                        parse_mode= 'HTML')
                    # query.message.reply_text(
                    #     MSG_RULES
                    #     )                                   
                else:
                    pass
            db_conn.closedbconnection()
            return ConversationHandler.END 
        else:
            return ConversationHandler.END 
            pass

    except Exception as e:
        return ConversationHandler.END 
        db_conn.closedbconnection()
        raise



@run_async
def start(update, context):
    chat_type = update.message.chat.type
    starter = update.message.from_user.first_name
    starter_id = update.message.from_user.id
    user = update.message.from_user
    user_id = user.id
    # print(update)
    try:
        if chat_type == 'private' or update.message.chat.id == ADMIN_CHAT_GROUP_ID:
            logger.info(
                "/start command triggered by {} with userid: {} in private message with bot".format(starter, starter_id)
                )
            db_conn = dbconnect()
            is_member = db_conn.ismemberbyid(starter_id)
            if is_member:
####################################################################################
                if user.username:
                    username = user.username
                    #update username in member!!!!!!!!!!!!!!!!!!! or update script
                else:
                    username = 'none'

                if user.first_name:
                    #update username in member
                    first_name = user.first_name
                else:
                    first_name = 'none'    

                if user.last_name:
                    #update username in member
                    last_name = user.last_name
                else:
                    last_name = 'none'    

                try:
                    photo_id = bot.get_user_profile_photos(user_id= user_id, limit=1).photos[0][0].file_id
                except Exception as e:
                    photo_id = 'none'

                if photo_id is not None:
                    #update username in member
                    photo_remarks = 'has profile photo'
                else:
                    photo_remarks = 'none'

                if first_name == 'none' or last_name == 'none' or photo_id =='none' or username =='none':
                    logger.info(
                        "{} setup incomplete profile".format(user_id)
                        ) 
                    update.message.reply_text(
                        MSG_START_CHECKPROFILE_MISSING.format(username, first_name, last_name, photo_remarks)
                        )
                else:
                    logger.info(
                        "{} setup complete profile; show menu for existing members".format(user_id)
                        )
                    #update all
###################################################################################     
                    keyboard = [
                        [InlineKeyboardButton("VIEW RULES", callback_data=str(RULES))],
                        [InlineKeyboardButton("REQUEST TO ADD MEMBER", callback_data=str(REFER_MEMBER))],
                        [InlineKeyboardButton("UPDATE MEMBER DETAILS", callback_data=str(UPDATE_MEMBER_MENU))],
                         # [InlineKeyboardButton("ADD REFERRER", callback_data=str(ADD_REFERRER))],
                         # [InlineKeyboardButton("ADD VALIDATING LINK", callback_data=str(ADD_VALIDATING_DOC))],
                         # [InlineKeyboardButton("SEND VALID ID", callback_data=str(SEND_VALID_ID))],                   
                         [InlineKeyboardButton("END", callback_data=str(END))],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)  
                    update.message.reply_text(
                        MSG_MEMBER_OPTIONS.format(starter),
                        reply_markup=reply_markup
                        )                
                    # return ConversationHandler.END
                    return MEMBER_MENU

###################################################################################                     
            else:
                is_pending_member = db_conn.isjoinerbyid(starter_id)
                if is_pending_member:
                    update.message.reply_text(
                        MSG_START_PENDINGMEMBER.format(starter),
                        force_reply = True,
                        selective = True,
                        )
                    return ConversationHandler.END                                       
                else:
                    update.message.reply_text(
                        MSG_INPUT_OTREFCODE.format(starter),
                        force_reply = True,
                        selective = True,
                        )
                    return CHECKCODE

            db_conn.closedbconnection()
        else:
            return ConversationHandler.END
            logger.info(
                "/start command triggered by {} with userid: {} in group chat".format(starter, starter_id)
                )
    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 
        raise


@run_async
def update_member_m(update, context):
    try:

        query = update.callback_query
        user = query.from_user
        # print(query)
        member_id = query.from_user.id
        member_username = query.from_user.username
        member_fname = query.from_user.first_name
        member_lname = query.from_user.last_name
        # photo_id = query.from_user.id

        keyboard = [
             [InlineKeyboardButton("ADD REFERRER", callback_data=str(ADD_REFERRER))],
             [InlineKeyboardButton("ADD VALIDATING LINK", callback_data=str(ADD_VALIDATING_DOC))],
             [InlineKeyboardButton("SEND VALID ID", callback_data=str(SEND_VALID_ID))],                   
             [InlineKeyboardButton("END", callback_data=str(END))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)  

        #show your member ship information
        #username, firstname, last_name, referrer, approver, validating link(social media profile), submitted ID: , joined meetup: 
        db_conn = dbconnect()

        update_basic_info = db_conn.update_basicinfo(member_id, member_username, member_fname, member_lname)      
        member_profile = db_conn.getmemberprofileinfo(member_id)
        # print(member_profile)
        if member_profile:
            id_submitted = member_profile[5]
            if id_submitted:
                id_submitted = "valid id sent"
            else:
                id_submitted = None

            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text= "Profile Details:\n\nUsername: {}\nFirst Name: {}\nLast Name: {}\nSocial Media Profile Link: {}\nID Submitted: {}\nReferrer: {}\n\nYou may update your membership details using this menu:".format(member_profile[1], member_profile[2],member_profile[3],member_profile[4],id_submitted ,member_profile[6]),
                reply_markup=reply_markup
                )
            logger.info(
                "update_member_m function"
                )
            return UPDATE_MEMBER_MENU
        else:
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text= "ERROR, PLEASE TRY AGAIN LATER\n\n/start",
                # reply_markup=reply_markup
                )
            logger.info(
                "{} : update_member_m"
                )
        db_conn.closedbconnection()
    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END




@run_async
def add_referrer_m(update, context):
    try:
        query = update.callback_query
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text= "Please enter the exact telegram username of your referrer without '@'.\n e.g. BFRV_PoolBot.\nMake sure to inform your referrer first before sending his/her username here.",
            )
        logger.info(
            "add_referrer_m"
            )
        return CHECK_REFERRER
    except Exception as e:
        return ConversationHandler.END

@run_async
def validate_referrer(update, context):
    referrer = update.message.text
    member_id = update.message.from_user.id
    member_username = update.message.from_user.username
    try:
        logger.info(
            "validate_referrer"
            )        
        db_conn = dbconnect()
        referrer = db_conn.ismemberbyusername(referrer)
 
        if referrer:
            update.message.reply_text(
                "You have added {} as your referrer. Make sure you informed {} that you added him/her. THANK YOU!".format(referrer[0], referrer[0]),
                )
            update_referrer = db_conn.update_member_referrer(member_id, referrer[1], referrer[0])
            db_conn.closedbconnection()
            return ConversationHandler.END 
        else:
            update.message.reply_text(
                "Invalid referrer username. Make sure you type in only the exact telegram username. This is case sensitive.\n\nType in start to view the menu again.",
                )
            db_conn.closedbconnection()
            return ConversationHandler.END 
    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 
        raise


@run_async
def add_valdoc_m(update, context):
    try:
        query = update.callback_query
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text= "Enter any of your social media profile link which can be used to validate your details:",
            )
        logger.info(
            "add_valdoc_m"
            )
        return CHECK_DOC
    except Exception as e:
        return ConversationHandler.END 
        raise


@run_async
def add_poid(update, context):
    proof_of_id = update.message.text
    member_id = update.message.from_user.id
    member_username = update.message.from_user.username
    try:
        logger.info(
            "add_poid"
            )  
        db_conn = dbconnect()
        # referrer = db_conn.ismemberbyusername(referrer)
        update.message.reply_text(
            "You have added a link as a proof of idenfication/verification. THANK YOU!",
            )
        update_poid = db_conn.update_member_poid(member_id, proof_of_id)
        db_conn.closedbconnection()
        return ConversationHandler.END 

    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 
        raise

@run_async
def invalid_val_link(update, context):
    proof_of_id = update.message.text
    # member_id = update.message.from_user.id
    # member_username = update.message.from_user.username
    try:
        logger.info(
            "invalid_val_link"
            )  
        # referrer = db_conn.ismemberbyusername(referrer)
        update.message.reply_text(
            "You have not entered a url or link. Please try again by typing in /start. Thank you!",
            )

        return ConversationHandler.END 

    except Exception as e:
        return ConversationHandler.END 
        raise


@run_async
def send_validid_m(update, context):
    try:
        query = update.callback_query
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text= "Please upload your valid/government id that shows your name and photo only. Please hide/blur any other personal information.\nMake sure to upload a valid image format:",
            )
        logger.info(
            "send_validid_m"
            )
        return CHECK_VALID_ID
    except Exception as e:
        return ConversationHandler.END 
        raise

@run_async
def send_validid(update, context):
    member_id = update.message.from_user.id
    member_username = update.message.from_user.username
    member_fname = update.message.from_user.first_name  
    member_lname = update.message.from_user.last_name
    valid_id = update.message.photo[0].file_id

    
    try:
        
        bot.send_message(
            chat_id= member_id, 
            text = "You have sent a proof of verification. Thank you!"
            )
        bot.send_message(
            chat_id= ADMIN_VALIDID_CHAT, 
            # text= MSG_TOADM_REQCODE.format(referrer_username, joinerusername, referrer_username, joinerusername),
            text = "{}: AN EXISTING MEMBER HAS SUBMITTED HIS/HER VALID ID:\n\nuserid: {}\nusername: {}\nfirst_name: {}\nlast_name: {}\nSee below submitted image:".format(member_username, member_id, member_username, member_fname, member_lname)
            )
        bot.send_photo(chat_id=ADMIN_VALIDID_CHAT, photo=valid_id)
        # print(str(valid_id))
        db_conn = dbconnect()
        valid_id_str = "CHAT_government_id_" + str(valid_id)
        update_valid_id = db_conn.update_member_valid_id(member_id, valid_id_str)
        db_conn.closedbconnection()
        
        #update poid image

        logger.info(
            # "{}: {} is in send_validid".format(referrer_id, referrer_username)
            "{}: in send_validid function, file_id: {}".format(member_username, valid_id_str)
            )
        return ConversationHandler.END 
    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 

    
@run_async
def refer_member(update, context):
    query = update.callback_query
    user = query.from_user
    referrer_id = query.from_user.id
    referrer_username = query.from_user.username

    try:
        if referrer_username:
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text= "Hi {},  please enter the telegram username of the joiner you want to add.\ne.g. BFRV_PoolBot\n\n*note: Make sure you entered the exact username. Make sure there are no extra characters and case is properly aligned.".format(referrer_username),
                )
            logger.info(
                "{}: {} is in refer_member option".format(referrer_id, referrer_username)
                )
            return CHECK_RCODE
        else:
            referrer_fname = query.from_user.first_name
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text= "Hi {},  please setup your telegram username first then type in /start again.".format(referrer_fname),
                )
            logger.info(
                "{}: {} has no username in refer_member option. ending conversation".format(referrer_id, referrer_fname)
                )        
            return ConversationHandler.END 
                
    except Exception as e:
        # db_conn.closedbconnection()
        return ConversationHandler.END 
        raise

@run_async
def request_code(update, context):
    query = update.callback_query
    joiner_username = update.message.text
    referrer_username = update.message.from_user.username
    referrer_id = str(update.message.from_user.id)
    # print(joiner_username)
    try:
        print(joiner_username)
        if joiner_username[0] == '@':
            joiner_username = joiner_username[1:]
            print(joiner_username)
        else:
            joiner_username = joiner_username


        db_conn = dbconnect()
        # referrer = db_conn.ismemberbyusername(referrer_username)
        refcode = db_conn.getrefcodebyusername(joiner_username)
        # print(update)
        if refcode:
            update_new_code = db_conn.update_refcode_byusername(joiner_username, codelen, None, 'BFRV_PoolBot', None, referrer_username, referrer_id)

            update.message.reply_text(
                text= MSG_MEM_REFERJOINER.format(referrer_username, update_new_code),
                )

            bot.send_message(
                chat_id=update.message.chat_id, 
                text="{}".format(update_new_code),
                parse_mode= 'HTML')

            logger.info(
                "{}: {} is in request_code".format(referrer_id, referrer_username)
                )

        else:
            gen_new_code = db_conn.new_refcode_byusername(joiner_username, codelen, None, 'BFRV_PoolBot', None, referrer_username, referrer_id)

            update.message.reply_text(
                text= MSG_MEM_REFERJOINER.format(referrer_username, gen_new_code),
                )

            bot.send_message(
                chat_id=update.message.chat_id, 
                text="{}".format(gen_new_code),
                parse_mode= 'HTML')

            logger.info(
                "{}: {} is in request_code option".format(referrer_id, referrer_username)
                )
        db_conn.closedbconnection()
        return ConversationHandler.END 
                
    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 
        raise

@run_async
# @restricted
def send_rcode(update, context):
    query = update.callback_query
    text = query.message.text

    ref_username_pos = text.find("referrer username: ") + 1
    join_username_pos = text.find("joiner username: ") + 1
    referrer_username = text[ref_username_pos:].split()[2]
    joiner_username = text[join_username_pos:].split()[2]

    joinerid = None
    adminid = query.from_user.id
    adminusername = query.from_user.username
    referrerusername = None
    referrerid = None
    # print(query)
    # print(adminusername)
    try:
        db_conn = dbconnect()
        referrer = db_conn.ismemberbyusername(referrer_username)
        refcode = db_conn.getrefcodebyusername(joiner_username)

        # print(referrer)
        # # print(update.message)
        if query.message.chat_id == ADMIN_CHAT_GROUP_ID or query.message.chat_id == jmj_chat_id:
            if referrer:
                if refcode:
                    update_new_code = db_conn.update_refcode_byusername(joiner_username, codelen, adminid, adminusername, joinerid, referrer_username, referrer[1])

                    bot.edit_message_text(
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text= MSG_TOADM_RUPDATE_REFCODE.format(joiner_username, referrer_username),
                        parse_mode= 'HTML')

                    bot.send_message(
                        chat_id=query.message.chat_id, 
                        text="{}".format(update_new_code),
                        parse_mode= 'HTML')

                    bot.send_message(
                        chat_id=referrer[1], 
                        text=MSG_TOREF_RUPDATE_REFCODE.format(referrer_username),
                        parse_mode= 'HTML')
                    bot.send_message(
                        chat_id=referrer[1], 
                        text="{}".format(update_new_code),
                        parse_mode= 'HTML')

                    logger.info(
                        "Admin {} generated code for {}".format(adminusername, joiner_username)
                        )
                else:
                    gen_new_code = db_conn.new_refcode_byusername(joiner_username, codelen, adminid, adminusername, joinerid, referrer_username, referrer[1])

                    bot.edit_message_text(
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text= MSG_TOADM_RNEW_REFCODE.format(joiner_username, referrer_username),
                        parse_mode= 'HTML')

                    bot.send_message(
                        chat_id=query.message.chat_id, 
                        text="{}".format(gen_new_code),
                        parse_mode= 'HTML') 

                    bot.send_message(
                        chat_id=referrer[1], 
                        text=MSG_TOREF_RNEW_REFCODE.format(referrer_username),
                        parse_mode= 'HTML')
                    bot.send_message(
                        chat_id=referrer[1], 
                        text="{}".format(gen_new_code),
                        parse_mode= 'HTML')

                    logger.info(
                        "Admin {} generated code for {}".format(adminusername, joiner_username)
                        )

            else:
                bot.edit_message_text(
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    text= MSG_RREFCODE_INVALID_REFERRER.format(joiner_username, referrer_username),
                    parse_mode= 'HTML')

                logger.info(
                    "{}: Code not generated for {} due to invalid referrer {}".format(adminusername, joiner_username ,referrer_username)
                    )                
        else:
            pass
        db_conn.closedbconnection()


    except Exception as e:
        db_conn.closedbconnection()
        raise


@run_async
# @restricted
def reject_rcode(update, context):
    query = update.callback_query
    text = query.message.text

    ref_username_pos = text.find("referrer username: ") + 1
    join_username_pos = text.find("joiner username: ") + 1
    referrer_username = text[ref_username_pos:].split()[2]
    joiner_username = text[join_username_pos:].split()[2]

    joinerid = None
    adminid = query.from_user.id
    adminusername = query.from_user.username
    # referrerusername = None
    # referrerid = None

    try:
        db_conn = dbconnect()
        referrer = db_conn.ismemberbyusername(referrer_username)
        if referrer:
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text= MSG_TOADM_RREFCODE_REJ.format(adminusername, joiner_username),
                parse_mode= 'HTML')

            bot.send_message(
                chat_id=referrer[1], 
                text=MSG_TOREF_RREFCODE_REJ.format(referrer_username),
                parse_mode= 'HTML') 

            logger.info(
                "Admin {} rejected request of {}".format(adminusername, joiner_username)
                )
        else:
            pass
        db_conn.closedbconnection()
    except Exception as e:
        db_conn.closedbconnection()
        raise
#DECLINE -->Please make sure the username is correct and his/her profile is properly set. Please read the /rules. Thank you!



# this function is just to repeat start for joiners only entering one time code
@run_async
def start_over(update, context):
    query = update.callback_query
    bot = context.bot
    chat_type = query.message.chat.type
    starter = query.from_user.first_name
    starter_id = query.from_user.id    

    try:
        if chat_type == 'private':
            logger.info(
                "/start command triggered by {} with userid: {} in private message with bot".format(starter, starter_id)
                )
            db_conn = dbconnect()
            is_member = db_conn.ismemberbyid(starter_id)
            if is_member:
                update.message.reply_text(
                    MSG_START_EXISTMEMBER.format(starter)
                    )
                return ConversationHandler.END
            else:
                is_pending_member = db_conn.isjoinerbyid(starter_id)
                if is_pending_member:
                    update.message.reply_text(
                        MSG_START_PENDINGMEMBER.format(starter),
                        force_reply = True,
                        selective = True,
                        )
                    return ConversationHandler.END                     
                else:
                    bot.edit_message_text(
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text= MSG_INPUT_OTREFCODE.format(starter),
                        force_reply = True,
                        selective = True,
                        )
                    return CHECKCODE
            db_conn.closedbconnection()
        else:
            logger.info(
                "/start command triggered by {} with userid: {} in group chat".format(starter, starter_id)
                )
            return ConversationHandler.END 
    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 
        raise


@run_async
def validate_refcode(update, context):
    refcode = update.message.text
    joiner_username = update.message.from_user.username
    joiner_userid = str(update.message.from_user.id)    
    try:
        keyboard = [
            [InlineKeyboardButton("NEXT", callback_data=str(CHECK_JOINER_PROFILE)),
             ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        db_conn = dbconnect()
        db_refcode = db_conn.getrefcodebyusername(joiner_username)
        # print(db_refcode)
        if db_refcode:
            if refcode == db_refcode[0]:
                update.message.reply_text(
                    MSG_CORRECTREFCODE,
                    reply_markup=reply_markup
                    )
                logger.info(
                    "{}: {} entered the correct referral code".format(joiner_userid, joiner_username)
                    )
                return CHECK_PROFILE
            else:
                # print(refcode)
                logger.info(
                    "{}: {} entered an INCORRECT referral code".format(joiner_userid, joiner_username)
                    )                
                db_conn.closedbconnection()
                retry_option(update, context)
                return RETRYCODE
        else:
            # print(refcode)
            logger.info(
                "{}: {} entered an INCORRECT referral code".format(joiner_userid, joiner_username)
                )                
            db_conn.closedbconnection()
            retry_option(update, context)
            return RETRYCODE
   
    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 
        raise


@run_async
def check_joiner_profile(update, context):
    query = update.callback_query
    user = query.from_user
    user_id = query.from_user.id

    try:
        if user.username:
            username = user.username
        else:
            username = 'none'

        if user.first_name:
            first_name = user.first_name
        else:
            first_name = 'none'    

        if user.last_name:
            last_name = user.last_name
        else:
            last_name = 'none'    

        try:
            photo_id = bot.get_user_profile_photos(user_id= user_id, limit=1).photos[0][0].file_id
        except Exception as e:
            photo_id = 'none'

        if photo_id is not None:
            photo_remarks = 'has profile photo'
        else:
            photo_remarks = 'none'

        if first_name == 'none' or last_name == 'none' or photo_id =='none' or username =='none':
            logger.info(
                "{} setup incomplete profile".format(user_id)
                )
            keyboard = [
                [InlineKeyboardButton("CHECK AGAIN", callback_data=str(CHECK_JOINER_PROFILE)),
                 InlineKeyboardButton("END", callback_data=str(END))
                 ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)  
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text= MSG_CHECKPROFILE_MISSING.format(username, first_name, last_name, photo_remarks),
                reply_markup=reply_markup
                )
            return CHECK_PROFILE
        else:
            logger.info(
                "{} setup complete profile".format(user_id)
                )
            keyboard = [
                [InlineKeyboardButton("SUBMIT", callback_data=str(SUBMIT))]
                        ]
            reply_markup = InlineKeyboardMarkup(keyboard)  
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text= MSG_CHECKPROFILE_COMPLETE.format(username, first_name, last_name, photo_remarks),
                # reply_markup=reply_markup
                )

###########################################################################################################            
            try:
                db_conn = dbconnect()
                fetch_joiner = db_conn.istemp_joinerbyid(user_id)
                admin_username = db_conn.getrefcodebyusername(username)[1]
                admin_userid = db_conn.getrefcodebyusername(username)[2]
                referrer_username = db_conn.getrefcodebyusername(username)[3]
                referrerid = db_conn.getrefcodebyusername(username)[4]
                valid_id = None

                if fetch_joiner:
                    delete_joiner = db_conn.delete_joiner(user_id)
                    add_to_joiner = db_conn.add_joiner_table(str(user_id), username, first_name, last_name, photo_id,admin_username, admin_userid, referrer_username, referrerid, valid_id)
                    logger.info(
                        "{} joiner added to table".format(username)
                        )                
                else:
                    logger.info(
                        "{} joiner added to table".format(username)
                        )                
                    add_to_joiner = db_conn.add_joiner_table(str(user_id), username, first_name, last_name, photo_id, admin_username, admin_userid, referrer_username, referrerid, valid_id)
                
                db_conn.closedbconnection()   
                return CHECK_PROFILE
            except Exception as e:
                return ConversationHandler.END 
                db_conn.closedbconnection()      
                raise
###########################################################################################################    
            return CHECK_PROFILE

    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 



@run_async
def add_joiner_poid(update, context):
    joiner_id = update.message.from_user.id
    joiner_username = update.message.from_user.username
    joiner_fname = update.message.from_user.first_name  
    joiner_lname = update.message.from_user.last_name

    proof_of_id = update.message.text
    # joiner_id = update.message.from_user.id
    # joiner_username = update.message.from_user.username

    try:
        logger.info(
            "{} add_joiner_poid".format(joiner_username)
            )   
        db_conn = dbconnect()
        # print(db_conn)
        update_poid = db_conn.update_joiner_poid(joiner_id, proof_of_id)

        keyboard = [
            [InlineKeyboardButton("SUBMIT", callback_data=str(SUBMIT))]
                    ]
        reply_markup = InlineKeyboardMarkup(keyboard)  

        update.message.reply_text(
            # chat_id=update.message.chat_id,
            # message_id=update.message.message_id,
            text= "Thank you for providing your proof of id.\nPlease click on SUBMIT to send the details to the admins so they can review your membership.",
            reply_markup=reply_markup
            )

        bot.send_message(
            chat_id= ADMIN_VALIDID_CHAT, 
            # text= MSG_TOADM_REQCODE.format(referrer_username, joinerusername, referrer_username, joinerusername),
            text = "{}: A JOINER HAS SUBMITTED HIS/HER SOCIAL MEDIA PROFILE LINK:\n\nuserid: {}\nusername: {}\nfirst_name: {}\nlast_name: {}\nSocial Media Link: {}".format(joiner_username, joiner_id, joiner_username, joiner_fname, joiner_lname, proof_of_id)
            )

        db_conn.closedbconnection()
        return CHECK_PROFILE

    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 
        raise


@run_async
def invalid_joiner_poid(update, context):
    proof_of_id = update.message.text
    # member_id = update.message.from_user.id
    # member_username = update.message.from_user.username
    try:
        logger.info(
            "invalid_joiner_poid"
            )  
        # referrer = db_conn.ismemberbyusername(referrer)
        update.message.reply_text(
            "You have not entered a url or link. Please enter a valid profile link:",
            )

        return CHECK_PROFILE

    except Exception as e:
        return ConversationHandler.END 
        raise


@run_async
def send_joiner_validid(update, context):
    joiner_id = update.message.from_user.id
    joiner_username = update.message.from_user.username
    joiner_fname = update.message.from_user.first_name  
    joiner_lname = update.message.from_user.last_name
    valid_id = update.message.photo[0].file_id
    # joiner_id = update.message.from_user.id
    # joiner_username = update.message.from_user.username

    try:
        keyboard = [
            [InlineKeyboardButton("SUBMIT", callback_data=str(SUBMIT))]
                    ]
        reply_markup = InlineKeyboardMarkup(keyboard)  

        update.message.reply_text(
            # chat_id=update.message.chat_id,
            # message_id=update.message.message_id,
            text= "Thank you for sending your valid id.\nPlease click on SUBMIT to send the details to the admins so they can review your membership.",
            reply_markup=reply_markup
            )

        bot.send_message(
            chat_id= ADMIN_VALIDID_CHAT, 
            # text= MSG_TOADM_REQCODE.format(referrer_username, joinerusername, referrer_username, joinerusername),
            text = "{}: A JOINER HAS SUBMITTED HIS/HER VALID ID:\n\nuserid: {}\nusername: {}\nfirst_name: {}\nlast_name: {}\nSee below submitted image:".format(joiner_username, joiner_id, joiner_username, joiner_fname, joiner_lname)
            )
        bot.send_photo(chat_id=ADMIN_VALIDID_CHAT, photo=valid_id)
        db_conn = dbconnect()
        valid_id_str = "CHAT_government_id_" + str(valid_id)

        update_joiner_valid_id = db_conn.update_joiner_valid_id(joiner_id, valid_id_str)
        db_conn.closedbconnection()
        
        #update poid image

        logger.info(
            # "{}: {} is in send_validid".format(referrer_id, referrer_username)
            "{}: in send_joiner_validid function, file_id: {}".format(joiner_username, valid_id_str)
            )
        return CHECK_PROFILE
    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END 


@run_async
def submit(update, context):
    query = update.callback_query
    joinerid = query.from_user.id
    # print(query)
    logger.info(
        "{}: submitted application to admins".format(query.from_user.username)
        )  
    try:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text= MSG_TOJOINER_PROFILESUBMIT
        )
        db_conn = dbconnect()
        submit = db_conn.update_joiner_submit(joinerid)
        db_conn.closedbconnection()  
        
        admin_approval(update, context)
        return ConversationHandler.END  
        # return ADMIN_APPROVAL
    
    except Exception as e:
        db_conn.closedbconnection()
        return ConversationHandler.END        
        raise       


@run_async
def admin_approval(update, context):
    query = update.callback_query
    # print(query)
    joinerid = query.from_user.id    
    # print(joinerid)    
    try:
        db_conn = dbconnect()
        fetch_joiner = db_conn.isjoinerbyid(joinerid)
        joinerid = fetch_joiner[0]
        joiner_username = fetch_joiner[1]
        joiner_fname = fetch_joiner[2]
        joiner_lname = fetch_joiner[3]
        referrer = fetch_joiner[5]
        poid_link = fetch_joiner[7]
        validid_photo = fetch_joiner[8]        
        # admin_approver_id = fetch_joiner[4]
        # admin_approver = fetch_joiner[6]

        logger.info(
            "{}: joiner application - notify approver and admin group".format(joinerid)
            ) 
        ### send notification to admin group for joiner
        # bot.send_message(
        #     chat_id= ADMIN_CHAT_GROUP_ID, 
        #     text= MSG_TOADMINS_PROFILESUBMIT.format(fetch_joiner[1], fetch_joiner[2], fetch_joiner[3], admin_approver),
        #     parse_mode = 'HTML'
        #     )

        keyboard = [
            [InlineKeyboardButton("APPROVE", callback_data=str(APPROVE_JOINER)),
             InlineKeyboardButton("REJECT", callback_data=str(REJECT_JOINER))
             ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)  

        if poid_link is not None:
            validating_doc = poid_link
        else:
            validating_doc = 'To view the submitted valid id, please search for the username in BFRV Valid docs group'
        
        ### send request to specific admin for review and approval
        bot.send_message(
            chat_id= ADMIN_CHAT_GROUP_ID, 
            text= MSG_TOAPPROVER_PROFILESUBMIT.format(joiner_username, joiner_fname, joiner_lname, joiner_username, referrer, validating_doc),
            reply_markup=reply_markup
            )

        db_conn.closedbconnection()
        return ConversationHandler.END            
    except Exception as e:
        db_conn.closedbconnection()  
        return ConversationHandler.END
        raise

    return ConversationHandler.END


# @run_async
def generate_invite_link(update, context):
    chat_type = update.message.chat.type
    dev_id = update.message.from_user.id

    bot = context.bot
    if chat_type == 'private' and dev_id == jmj_chat_id:
        # global invite_link
        # print(invite_link)
        invite_link = bot.exportChatInviteLink(chat_id = MEMBERS_CHAT_GROUP_ID)
        bot.send_message(
            chat_id=jmj_chat_id, 
            text=invite_link)       
        # print(invite_link)
    return invite_link

@run_async
def reset_joiner(update, context):
    chat_type = update.message.chat.type
    dev_id = update.message.from_user.id
    chat_id = update.message.chat.id
    text = update.message.text
    usernames = text.split()
    joiner_username = usernames[1]

    try:
        if chat_type == 'private' and dev_id == jmj_chat_id:
            db_conn = dbconnect()

            del_joiner = db_conn.delete_joiner_byusername(joiner_username)
            del_member = db_conn.delete_member_byusername(joiner_username)

            if del_joiner and del_member:
                        bot.send_message(
                            chat_id=chat_id, 
                            text="deleted in joiner and member table. ask joiner to retry by sending /start command to bot")  
            db_conn.closedbconnection()
        else:
            pass
    except Exception as e:
        db_conn.closedbconnection()  
        raise

@run_async
# @restricted
def approve_joiner(update, context):
    query = update.callback_query
    bot = context.bot
    text = query.message.text
    username_pos = text.find("@") + 1
    joiner_username = text[username_pos:].split('\n')
    # approver_id = query.from_user.id

    adminid = query.from_user.id
    adminusername = query.from_user.username

    chat = bot.get_chat(MEMBERS_CHAT_GROUP_ID)
    invite_link = chat.invite_link
    group_name = chat.title
    try:
        db_conn = dbconnect()
        joiner = db_conn.get_joinerby_username(joiner_username[0])
        member = db_conn.add_member_table(joiner[0], joiner[1], joiner[2], joiner[3], joiner[4], joiner[9], joiner[10], adminid, adminusername, joiner[17], joiner[7], False)
        
        if member:
            # bot.edit_message_text(
            #     chat_id= ADMIN_CHAT_GROUP_ID,
            #     message_id=query.message.message_id,
            #     text= MSG_APPROVER_APPROVE.format(joiner_username[0]),
            #     force_reply = True,
            #     selective = True,
            #     )

            # bot.send_message(
            bot.edit_message_text(
                chat_id= ADMIN_CHAT_GROUP_ID, 
                message_id= query.message.message_id,
                text= MSG_TOADMINS_JOINER_APPROVED.format(joiner_username[0], adminusername),
                )

            keyboard = [
                [InlineKeyboardButton("JOIN", url = invite_link, callback_data=str(JOIN_GROUP)),
                 ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)  

            bot.send_message(
                chat_id= joiner[0], 
                text= MSG_TOJOINER_INVITEBUTTON.format(joiner[1], group_name),
                reply_markup=reply_markup
                )
            
            delete_in_refcode = db_conn.delete_refcode_byusername(joiner[1])
            delete_in_joiner = db_conn.delete_joiner_byusername(joiner[1])

            logger.info(
                "{}: approver approves joiner {}. added to member database and delete to joiners and refcode tables".format(adminusername, joiner_username[0])
                ) 
            
            db_conn.closedbconnection() 

        else:
            db_conn.closedbconnection()  
            
    except Exception as e:
        db_conn.closedbconnection()  
        raise


@run_async
# @restricted
def reject_joiner(update, context):
    query = update.callback_query
    bot = context.bot
    text = query.message.text
    username_pos = text.find("@") + 1
    joiner_username = text[username_pos:].split('\n')

    adminid = query.from_user.id
    adminusername = query.from_user.username

    chat = bot.get_chat(MEMBERS_CHAT_GROUP_ID)
    # invite_link = chat.invite_link
    group_name = chat.title
    try:
        db_conn = dbconnect()
        joiner = db_conn.get_joinerby_username(joiner_username[0])

        bot.edit_message_text(
            chat_id= ADMIN_CHAT_GROUP_ID,
            message_id=query.message.message_id,
            text= MSG_TOADMINS_JOINER_REJECTED.format(joiner_username[0], adminusername),
            force_reply = True,
            selective = True,
            )

        # bot.send_message(
        #     chat_id= ADMIN_CHAT_GROUP_ID, 
        #     text= MSG_TOADMINS_JOINER_REJECTED.format(joiner_username[0], adminusername),
        #     )

        bot.send_message(
            chat_id= joiner[0], 
            text= MSG_TOJOINER_REJECTED
            )
        
        delete_in_refcode = db_conn.delete_refcode_byusername(joiner[1])
        delete_in_joiner = db_conn.delete_joiner_byusername(joiner[1])

        logger.info(
            "{}: approver rejects joiner {}. deleted to refcode and joiner tables".format(adminid, joiner_username[0])
            ) 
        
        db_conn.closedbconnection()

    except Exception as e:
        db_conn.closedbconnection()  
        raise


@run_async
def retry_option(update, context):
    # user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("RETRY", callback_data=str(RETRY)),
         InlineKeyboardButton("END", callback_data=str(END))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id= update.message.chat_id, 
        text= MSG_REENTER_REFCODE,
        reply_markup= reply_markup)
    return CHECKCODE

@run_async
def end(update, context):

    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text= MSG_END_CONV
    )
    return ConversationHandler.END


@run_async
def getcodefor(update, context):
    text = update.message.text
    code_expiry = str(30) #expiry in minutes
    usernames = text.split()
    joiner_username = usernames[1]
    referrer_username = usernames[2]

    joinerid = None
    adminid = update.message.from_user.id
    adminusername = update.message.from_user.username

    try:
        db_conn = dbconnect()
        referrer = db_conn.ismemberbyusername(referrer_username)
        refcode = db_conn.getrefcodebyusername(joiner_username)


        # print(update.message)
        if update.message.chat_id == ADMIN_CHAT_GROUP_ID or update.message.chat_id == jmj_chat_id:
            if referrer:
                if refcode:
                    update_new_code = db_conn.update_refcode_byusername(joiner_username, codelen, adminid, adminusername, joinerid, referrer_username, referrer[1])

                    bot.send_message(
                        chat_id=update.message.chat_id, 
                        text= MSG_UPDATE_REFCODE.format(joiner_username),
                        parse_mode= 'HTML')

                    bot.send_message(
                        chat_id=update.message.chat_id, 
                        text="{}".format(update_new_code),
                        parse_mode= 'HTML')

                    logger.info(
                        "Admin {} generated code for {}".format(adminusername, joiner_username)
                        )
                else:
                    gen_new_code = db_conn.new_refcode_byusername(joiner_username, codelen, adminid, adminusername, joinerid, referrer_username, referrer[1])

                    bot.send_message(
                        chat_id=update.message.chat_id, 
                        text= MSG_NEW_REFCODE.format(joiner_username),
                        parse_mode= 'HTML')

                    bot.send_message(
                        chat_id=update.message.chat_id, 
                        text="{}".format(gen_new_code),
                        parse_mode= 'HTML') 

                    logger.info(
                        "Admin {} generated code for {}".format(adminusername, joiner_username)
                        )

            else:
                bot.send_message(
                    chat_id=update.message.chat_id, 
                    text= MSG_REFCODE_INVALID_REFERRER.format(joiner_username, referrer_username),
                    parse_mode= 'HTML')

                logger.info(
                    "{}: Code not generated for {} due to invalid referrer {}".format(adminusername, joiner_username ,referrer_username)
                    )                
        else:
            pass
        db_conn.closedbconnection()

    except Exception as e:
        db_conn.closedbconnection()
        raise


@run_async
def new_member_catcher(update, context):
    try:
        for new_member in update.message.new_chat_members:
            if update.message.chat_id == MEMBERS_CHAT_GROUP_ID:
                member_id = new_member.id

                if new_member.first_name:
                    first_name = new_member.first_name
                else:
                    first_name = "none"
                
                db_conn = dbconnect()
                isapproved_notjoined = db_conn.isapproved_notjoined(member_id)
                if isapproved_notjoined:
                    bot.send_message(
                        chat_id=member_id, 
                        text= MSG_TONEWMEMBER_WELCOME.format(new_member.username)
                        )
                    bot.send_message(
                        chat_id=ADMIN_CHAT_GROUP_ID, 
                        text= MSG_TOADMINS_NEWMEMBER.format(new_member.username),                    
                        )
                    bot.send_message(
                        chat_id=MEMBERS_CHAT_GROUP_ID, 
                        text= MSG_TOMEMBERS_NEWMEMBER.format(new_member.username),                    
                        )

                    setuser_joined = db_conn.update_member_joined(member_id)

                    logger.info(
                        "{}: joined!".format(new_member.username)
                        ) 
                else:
                    bot.send_message(
                        chat_id=ADMIN_CHAT_GROUP_ID, 
                        text= MSG_TOADMINS_UNKOWNJOINER.format(first_name),                    
                        )

                    bot.send_message(
                        chat_id=member_id, 
                        text=MSG_TOJOINER_UNKOWNJOINER.format(first_name),
                        )
                    
                    bot.kickChatMember(
                        chat_id =MEMBERS_CHAT_GROUP_ID,
                        user_id = member_id
                        )
                    logger.info(
                        "{}: {} unknown joiner warned and kicked!".format(member_id, first_name)
                        )
                db_conn.closedbconnection()
            else:
                pass
        
    except AttributeError:
        pass


@run_async
def leaving_member_catcher(update, context):
    left_userid = update.message.left_chat_member.id
    left_username = update.message.left_chat_member.username
    
    try:
        if update.message.chat_id == ADMIN_CHAT_GROUP_ID:
            bot.send_message(
                chat_id=ADMIN_CHAT_GROUP_ID, 
                text= MSG_TOADMINS_LEFTMEMBER.format(left_username)
                )

            db_conn = dbconnect()
            setuser_left = db_conn.update_member_left(left_userid)

            logger.info(
                "{}: left!".format(left_username)
                ) 
        else:
            pass
        db_conn.closedbconnection()
    except AttributeError:
        db_conn.closedbconnection()
        pass


# @run_async
@restricted
def kick_member(update, context):
    chat_type = update.message.chat.type
    # dev_id = update.message.from_user.id
    chat_id = update.message.chat.id
    text = update.message.text
    username_split = text.split()
    kick_member = username_split[1]

    try:
        if chat_id == ADMIN_CHAT_GROUP_ID:
            db_conn = dbconnect()

            update.message.reply_text(
                "you have kicked {} from BFRV Pool members chat group".format(kick_member)
                )
            kick_userid = db_conn.ismemberbyusername(kick_member)[1]
            bot.kickChatMember(
                chat_id =MEMBERS_CHAT_GROUP_ID,
                user_id = kick_userid
                )

            del_joiner = db_conn.delete_joiner_byusername(kick_member)
            del_member = db_conn.delete_member_byusername(kick_member)


            logger.info(
                "{}: {} unknown joiner warned and kicked!".format(kick_userid, kick_member)
                )
            db_conn.closedbconnection()
        else:
            pass
    except Exception as e:
        db_conn.closedbconnection()  
        raise

# @run_async
@restricted
def unban_member(update, context):
    chat_type = update.message.chat.type
    # dev_id = update.message.from_user.id
    chat_id = update.message.chat.id
    text = update.message.text
    userid_split = text.split()
    unban_member = userid_split[1]

    try:
        if chat_id == ADMIN_CHAT_GROUP_ID or chat_id == dev_chat_id:
            db_conn = dbconnect()

            update.message.reply_text(
                "you have unbanned {} from BFRV Pool members chat group".format(unban_member)
                )
            # kick_userid = db_conn.ismemberbyusername(kick_member)[1]
            bot.unbanChatMember(
                chat_id =MEMBERS_CHAT_GROUP_ID,
                user_id = unban_member
                )


            logger.info(
                "{}: user id unbanned".format(unban_member)
                )
            db_conn.closedbconnection()
        else:
            pass
    except Exception as e:
        db_conn.closedbconnection()  
        raise

# def members_update(update, context):
#     if update.message.chat_id == jmj_chat_id:
#         teleconn = telethonClientConnect()
#         member_updates = teleconn.memberScraper()
#     else:
#         pass

# @run_async
# @restricted
# def send_to_admins(update, context):

# def send_to_members(update, context):

# def admin_menu(update, context):
# #kick
# #unban
# #announcement + pin message

# def report_to_admins(update, context):
# #hello! please help us maintain the integrity of our carpooling community. You may report your concerns so we can assess and tag our members accordingly.
# #report a driver
#     #input valid username of the person you are reporting
#         #type in your concerns and hit enter/send when you are done.
# #report a passenger
#     #input valid username of the person you are reporting
#         #type in your concerns and hit enter/send when you are done.
# #any screenshot you would like to send? -- send now, No - submit

@run_async
def help(update, context):
    try:
        if update.message.chat.id == MEMBERS_CHAT_GROUP_ID:
            update.message.reply_text(
                MSG_HELP.format(update.message.from_user.first_name)
                )
        else:
            pass
    except Exception as e:
        raise
    
#you may message /start to @BFRV_PoolBot to view your available commands.

@run_async
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

@run_async
def error_callback(update, context):
    try:
        raise error
    except Unauthorized:
        raise error 
    except BadRequest:
        raise error
    except TimedOut:
        raise error
    except NetworkError:
        raise error
    except ChatMigrated as e:
        raise error
    except TelegramError:
        raise error


def main():
    updater = Updater(TOKEN, use_context=True, workers=32)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # JOINER_MENU: [CallbackQueryHandler(start_over, pattern='^' + str(ADD_MEMBER) + '$'),
            #             CallbackQueryHandler(end, pattern='^' + str(RULES) + '$')
            #             ],
            MEMBER_MENU: [CallbackQueryHandler(refer_member, pattern='^' + str(REFER_MEMBER) + '$'),
                        CallbackQueryHandler(rules_m, pattern='^' + str(RULES) + '$'),
                        CallbackQueryHandler(update_member_m, pattern='^' + str(UPDATE_MEMBER_MENU) + '$'),
                        # CallbackQueryHandler(add_referrer_m, pattern='^' + str(ADD_REFERRER) + '$'),
                        # CallbackQueryHandler(add_valdoc_m, pattern='^' + str(ADD_VALIDATING_DOC) + '$'),
                        # CallbackQueryHandler(send_validid_m, pattern='^' + str(SEND_VALID_ID) + '$'),                        
                        CallbackQueryHandler(end, pattern='^' + str(END) + '$')
                        ],
            UPDATE_MEMBER_MENU: [CallbackQueryHandler(add_referrer_m, pattern='^' + str(ADD_REFERRER) + '$'),
                        CallbackQueryHandler(add_valdoc_m, pattern='^' + str(ADD_VALIDATING_DOC) + '$'),
                        CallbackQueryHandler(send_validid_m, pattern='^' + str(SEND_VALID_ID) + '$'), 
                        CallbackQueryHandler(end, pattern='^' + str(END) + '$')                   
                    ],  
            CHECK_RCODE: [ MessageHandler(Filters.text, request_code),
                    ],  
            CHECK_REFERRER: [ MessageHandler(Filters.text, validate_referrer),
                    ],
            CHECK_VALID_ID: [ MessageHandler(Filters.photo, send_validid),
                    ],
            CHECK_DOC: [ MessageHandler(Filters.text & (Filters.entity(MessageEntity.URL) |
                        Filters.entity(MessageEntity.TEXT_LINK)), add_poid),
                        MessageHandler(Filters.text, invalid_val_link)
                    ],  
            CHECKCODE: [MessageHandler(Filters.text, validate_refcode),
                    CallbackQueryHandler(check_joiner_profile, pattern='^' + str(CHECK_JOINER_PROFILE) + '$'),
                    ],
            RETRYCODE: [CallbackQueryHandler(start_over, pattern='^' + str(RETRY) + '$'),
                        CallbackQueryHandler(end, pattern='^' + str(END) + '$')
                        ],
            CHECK_PROFILE: [CallbackQueryHandler(check_joiner_profile, pattern='^' + str(CHECK_JOINER_PROFILE) + '$'),
                            MessageHandler(Filters.text & (Filters.entity(MessageEntity.URL) |
                                                    Filters.entity(MessageEntity.TEXT_LINK)), add_joiner_poid),
                            MessageHandler(Filters.text, invalid_joiner_poid),
                            MessageHandler(Filters.photo, send_joiner_validid),                    
                            CallbackQueryHandler(submit, pattern='^' + str(SUBMIT) + '$'),
                            CallbackQueryHandler(end, pattern='^' + str(END) + '$')
                                    ],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member_catcher))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, leaving_member_catcher))

    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bothelp", help))
    dp.add_handler(CommandHandler("resetlink", generate_invite_link))
    dp.add_handler(MessageHandler(Filters.regex('/resetjoiner '), reset_joiner))
    dp.add_handler(MessageHandler(Filters.regex('/kick '), kick_member))
    dp.add_handler(MessageHandler(Filters.regex('/unban '), unban_member))
    # dp.add_handler(CommandHandler("membersupdate", members_update))
    
    dp.add_handler(MessageHandler(Filters.regex('/codefor '), getcodefor))

    # dp.add_handler(CallbackQueryHandler(click_join, pattern='^' + str(JOIN_GROUP) + '$'))
    dp.add_handler(CallbackQueryHandler(approve_joiner, pattern='^' + str(APPROVE_JOINER) + '$'))
    dp.add_handler(CallbackQueryHandler(reject_joiner, pattern='^' + str(REJECT_JOINER) + '$'))

    dp.add_handler(CallbackQueryHandler(send_rcode, pattern='^' + str(SEND_RCODE) + '$'))
    dp.add_handler(CallbackQueryHandler(reject_rcode, pattern='^' + str(REJECT_RCODE) + '$'))

    dp.add_error_handler(error)
    dp.add_error_handler(error_callback)
 
    # Start the Bot
    run(updater)
    # updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()