mode = "prod"

dev_chat_id = 
refcode_length = 
if mode == "prod":
	db_setup = "dbname='' user='' host='' password='' port=''"
	bot_token = ""
	MEMBERS_CHAT_GROUP_ID = 
	ADMIN_CHAT_GROUP_ID = 
	ADMIN_VALIDID_CHAT = 
	HEROKU_APP_NAME = ""
	NGROK_APP_NAME = ''
else:
	db_setup = "dbname='' user='' host='' password='' port=''"
	bot_token = ""
	MEMBERS_CHAT_GROUP_ID = #staging this is the supergroup chat id the bot is monitoring testbfbot-chat
	ADMIN_CHAT_GROUP_ID = #stagingtemporary test group testbfbot-admin
	ADMIN_VALIDID_CHAT = 	
	NGROK_APP_NAME = "" #this should be changed everytime you triger ./ngrok http 80 get the link with https
	HEROKU_APP_NAME = ''

MSG_UPDATE_REFCODE = "<b>please use new code for</b> <i>{}</i><b>:</b>"
MSG_NEW_REFCODE = "<b>one-time code generated for</b> <i>{}</i><b>:</b>"
MSG_REFCODE_INVALID_REFERRER = "Referrer entered is not a member. Please check if the the username inputs or syntax is correct.\njoiner: <i>{}</i>\nreferrer: <i>{}</i>"

MSG_TOREF_REQCODE = "Your request for a referral code has been sent and will be reviewed. Admins will get in touch as needed. Thank you!"
MSG_TOADM_REQCODE = "Hi  Admins, @{} would like to add @{} in our group chat and is requesting for a referral code. Before sending a code or rejecting the request, make sure you have initiated a conversation with @BFRV_PoolBot(this is only done once) by clicking on start or typing in /start command.Please check on the details below\n\nreferrer username: {}\njoiner username: {}"

MSG_TOADM_RUPDATE_REFCODE = "Referral code for @{} and instructions has been sent to @{}. Kindly wait for your approval options after the joiner has submitted his/her application.\nBelow is the generated code for your reference:"
MSG_TOADM_RNEW_REFCODE = "Referral code for @{} and instructions has been sent to @{}. Kindly wait for your approval options after the joiner has submitted his/her application.\nBelow is the generated code for your reference:"

MSG_TOREF_RUPDATE_REFCODE = "Hi {}, an admin has approved your request. Please take note that this code will only work for the exact telegram username you entered in your request. As a member, you are expected to know the /rules. Also for everyone's safety, kindly ensure that the member you referred will follow and understand the /rules.\n\n Please instruct the joiner to initiate a conversation with our bot @BFRV_PoolBot by clicking on the start button or typing in /start in bot conversation. Then, enter the code below:\n"
MSG_TOREF_RNEW_REFCODE ="Hi {}, an admin has approved your request. Please take note that this code will only work for the exact telegram username you entered in your request. As a member, you are expected to know the /rules. Also for everyone's safety, kindly ensure that the member you referred will follow and understand the /rules.\n\n Please instruct the joiner to initiate a conversation with our bot @BFRV_PoolBot by clicking on the start button or typing in /start. Then, enter the code below:\n"

MSG_RREFCODE_INVALID_REFERRER = "Referrer entered is not a member. Please check if the the username inputs or syntax is correct.\njoiner: <i>{}</i>\nreferrer: <i>{}</i>"

MSG_TOADM_RREFCODE_REJ = "Hi Admin @{}, you have rejected the referral code request of @{}. A message has been sent to the requestor Thank you!"
MSG_TOREF_RREFCODE_REJ = "Hi {}, your request has been rejected. This feature is still under test.\nFor now, please review the /rules."

MSG_START_EXISTMEMBER = 'Hi {}! You are an existing member. Your menu and feautures are still under development.'
MSG_START_PENDINGMEMBER = 'Hi {}! Your membership is still pending for approval. Please wait for admin approval or feedback. Thank you!'
MSG_MEMBER_OPTIONS = 'Hi {}, as a member, you may choose from the options below:'
MSG_JOINER_OPTIONS = 'Hi {}, Please choose from the options below:'

MSG_MEM_REFERJOINER = "Hi {}, to add a new member, please ask the joiner to find @BFRV_PoolBot and click on START button to see the steps to join.\nAsk him/her to enter this one time-code when prompted:\n\n{}"

MSG_INPUT_OTREFCODE = 'Welcome {}! Please enter your one-time referral code:'
MSG_CORRECTREFCODE = 'Referral Code entered is correct! Please ensure that you update your profile properly.\n\nSetup your telegram username, first name and last name. Use recent, clear, and identifiable profile picture\n\n\nIf you are done, click next'
MSG_REENTER_REFCODE = "You have entered an invalid referral code. Please check or contact your referrer/admin contact."
MSG_END_CONV = 'Goodbye! Have a safe ride!'

MSG_CHECKPROFILE_MISSING = 'Please review and update your profile! We can still see some missing information.\nusername: @{}\nfirst_name: {}\nlast_name: {}\nphoto: {}\n*make sure to upload your real picture'

MSG_CHECKPROFILE_COMPLETE = 'Telegram Profile Setup COMPLETE!\n\nusername: @{}\nfirst_name: {}\nlast_name: {}\nphoto: {}\n*make sure to upload your real picture.\n\n\nPlease send us a link to your social media profile to validate your identity\nor send us a screenshot of your government/validid showing your name and face only:'

MSG_TOJOINER_PROFILESUBMIT = "Your profile details are submitted to the admins for review. Please wait within 24 hours for approval or possible feedback. We'll get in touch!"
MSG_TOADMINS_PROFILESUBMIT= 'Hi Admins! A joiner has sent his/her application. See details below:\n\nUsername: @{}\nFirst Name: {}\nLast Name: {}\nPhoto ID: please review by checking the photo of the username link of the joiner\n\nAdmin @{}, for your review.'
MSG_TOAPPROVER_PROFILESUBMIT= "Hi Admins! A new member request has been submitted.\n\nUsername: {}\nFirst Name: {}\nLast Name: {}\nPhoto ID: manually validate the photo of @{}\nReferrer: {}\nProof of Identity: {}"

MSG_APPROVER_APPROVE = 'Approved! A JOIN BUTTON will be shared to {}. Thank you!'
MSG_APPROVER_REJECTED = 'Rejected! Reject message will be sent to the user and the admins! Thank you!'
MSG_TOJOINER_REJECTED = 'Your application has been rejected due to one or more of the following reasons:\n\n1. Inappropriate Photo\n2. Incomplete name or username\n3. Incomplete Requirements\n\nPlease review the /rules and contact your referrer or admin.'
MSG_TOADMINS_JOINER_APPROVED = 'Hi Admins! Joiner {} has been approved by Admin {}.\nA JOIN BUTTON will be shared to him/her in private.\n\nThank you!'
MSG_TOADMINS_JOINER_REJECTED = 'Hi Admins! Joiner {} has been rejected by Admin {}.'
MSG_TOJOINER_INVITEBUTTON = 'Hi {}. Your application has been approved. :) You may join the group by clicking on the button below to join {}. Happy carpooling!'

MSG_TONEWMEMBER_WELCOME = 'Welcome {} to BFRV etc! Please make sure to follow our rules and policies all the time. You can check it by typing /rules in the main chat room. Enjoy!'
MSG_TOADMINS_NEWMEMBER = 'Hi Admins! {}, a new member has joined!'
MSG_TOMEMBERS_NEWMEMBER = 'Welcome {} to BFRV etc! Please make sure to follow our rules and policies all the time. You can check it by typing /rules in the main chat room. Enjoy!'

MSG_TOADMINS_UNKOWNJOINER = 'Hi Admins, {} tried to join the group. The JOIN button might have been forwarded to an unknown joiner or he/she was added by an admin manually.\n\nPlease verify. Thank you!'
MSG_TOJOINER_UNKOWNJOINER = 'Hello, {}. You are not a verified member. You will be removed from the group immediately!\n'

MSG_TOADMINS_LEFTMEMBER = 'Hi Admins! {} has left or has been kicked!'

MSG_RULES ="UPDATED MEMBERSHIP RULES\n\nThis applies to ALL (OLD & NEW)\n\n1. ALL members should have a Telegram account with the following:\n   a. Username (ex. @Chi206) – this will be our main unique identifier\n   b. Recent, clear, and identifiable picture\n   c. REAL first and last name\n   d. Telegram privacy settings should have profile photo showing to everybody and phone number showing to contacts only\n\n2. ALL members should know/have the username of the person who invited/referred them to BFRV etc. This will be collected by the admins.\n\n3. For everyone’s security, ALL members should have at least 1 of the following validating requirements below:\n   a. Attended one of our OFFICIAL group get-togethers at least once – this will show your good faith and to get to know other members (and vice versa)\n   b. Link to your personal social media account (FB/IG/TWITTER) that CAN VALIDATE your telegram profile\n   c. Photocopy/Screensot of any government ID (only showing your name and picture)"

MSG_HELP = "Hello {}! You may view the members menu by sending a private message to @BFRV_PoolBot. Click on START or send /start to the bot.\n\n*How to add a member?\n*Update or submit your member details?\nCheck out @BFRV_PoolBot"
MSG_START_CHECKPROFILE_MISSING = 'YOUR PROFILE SETUP IS INCOMPLETE!\n\nPlease review the /rules and update your profile accordingly.\nusername: @{}\nfirst_name: {}\nlast_name: {}\nphoto: {}\n*make sure to upload your real picture\n\nType in /start again when you are done!'