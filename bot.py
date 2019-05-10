import os
import sqlite3
import telebot
from config import token

bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda msg: True, content_types=["audio"])
def handle_voice(msg):
    print(msg)  # debug
    uid = msg.chat.id
    aid = msg.audio.file_id
    bot.send_message(uid, "UID: {}, AID: {}".format(uid, aid))
    try:
        file_info = bot.get_file(aid)
        file_data = bot.download_file(file_info.file_path)
        
        print(file_info.file_path)  # debug
        save_to = '/tmp/' + file_info.file_path

        try:
            os.mkdir(os.path.dirname(save_to))
        except FileExistsError:
            pass
        except Exception as e:
            #print(type(e).__name__)
            bot.send_message(uid, 'Can\'t prepare directory({})'.format(e))
    
        with open(save_to, 'wb') as new_file:
            new_file.write(file_data)

        bot.send_message(uid, 'Audio saved')
        save_to_db(uid, save_to)
    except Exception as e:
        bot.send_message(uid, 'Can\'t save audio({})'.format(e))


def save_to_db(uid, path):
    connection = sqlite3.connect(".db", check_same_thread = True)
    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS audio (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, UID INT, Path TEXT)")
    
    sql = 'INSERT INTO audio (UID, Path) VALUES ({}, "{}")'.format(uid, path)
    cur.execute(sql)
    
    connection.commit()
    connection.close()


if __name__ == '__main__':
    print("Bot Started")
    bot.polling(none_stop=True)

