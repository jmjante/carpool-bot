from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from tgbot.ai import dbconnect
import csv
from datetime import datetime
now = datetime.now()

api_id = 
api_hash = ''
phone = ''

class telethonClientConnect:
    def memberScraper(self):
        try:
            client = TelegramClient('anon', api_id, api_hash)
            client.connect()
            
            if not client.is_user_authorized():
                client.send_code_request(phone)
                client.sign_in(phone, input('Enter the code: '))

            chats = []
            last_date = None
            chunk_size = 200
            groups=[]
            
            try:
                result = client(GetDialogsRequest(
                             offset_date=last_date,
                             offset_id=0,
                             offset_peer=InputPeerEmpty(),
                             limit=chunk_size,
                             hash = 0
                         ))
                chats.extend(result.chats)

                target_group='BFRV etc.'

                print('Fetching Members...')
                all_participants = []
                all_participants = client.get_participants(target_group, aggressive=True)
                print('Saving In file...')
                
                db_conn = dbconnect()
                if db_conn:
                    count_members_before = db_conn.count_members_table()[0]
                    mem_file_count = 0
                    mem_updated_count = 0
                    print("member count before: {}".format(count_members_before))
                    users_in_file = []
                    for user in all_participants:
                        users_in_file.append(user.id)
                        mem_file_count += 1
                        is_member = db_conn.ismemberbyid(user.id)
                        if is_member:
                            if user.photo is not None:
                                photo_id = user.photo.photo_id
                            else:
                                photo_id = None
                            
                            update_user = db_conn.update_basicinfo(user.id, user.username, user.first_name, user.last_name, photo_id)
                            
                            if update_user:
                                mem_updated_count += 1
                            else:
                                pass
                        else:
                            #new members in file that needs to be inserted
                            print("{} {} {} {} {}".format(user.id, user.username, user.first_name, user.last_name, photo_id))
                            new_member = db_conn.add_member_table(user.id, user.username, user.first_name, user.last_name, photo_id, None, None, None, None, None, None, True)
   
                    print("member count in file: {}".format(mem_file_count))
                    print("member count successful updated members: {}".format(mem_updated_count))
                    #for deletion
                    #select * non updated members less than date time now -5 minutes
                    mem_for_del = db_conn.get_members_for_deletion(users_in_file)
                    delete_members = db_conn.delete_members(mem_for_del)
                    if delete_members:
                        print("successfully cleaned up members list")
                    else:
                        print("error in deletion")


                    db_conn.closedbconnection()
                    
                else:
                    print("cannot connect to database")

                print('Members scraped successfully.')

            except Exception as e:
                # return False 
                raise

        except:
            raise
            print("Cannot connect to telethon client")
 
 
teleClient = telethonClientConnect()
scrape_member = teleClient.memberScraper()