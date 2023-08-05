import os
import telegram
import requests
from .config import Config

class Tele:

    def get_chat_ids(self):
        url = f"https://api.telegram.org/bot{Config.get_bot_token()}/getUpdates"
        res = requests.get(url)
        res.raise_for_status()
        chats_by_name = {}
        for update in res.json()['result']:
            _chat = update['message']['chat']
            _from = update['message']['from']['username']
            msg_keys = set(update['message'].keys())
            for _key in ['chat', 'date', 'message_id', 'from']:
                if _key in msg_keys:
                    msg_keys.remove(_key)
            chats_by_name[_chat['title']] = chats_by_name.get(_chat['title'],
                                                              _chat['id'])

        return chats_by_name

    def get_chat_id_by_name(self, chat_name):
        return self.get_chat_ids().get(chat_name,
                                       "No such chat name in last updates")
    @staticmethod
    def send_msg(msg, chname):
        _bot = telegram.Bot(token=Config.get_bot_token())
        _bot.send_message(chat_id=Config.get_chat_id(chname),
                         text=msg)

    @staticmethod
    def send_img(photo_stream, chname):
        if photo_stream is None:
            Tele.send_msg('No photo recieved to send', chname)
        else:
            _bot = telegram.Bot(token=Config.get_bot_token())
            _bot.send_photo(chat_id=Config.get_chat_id(chname),
                            photo=photo_stream)
            stat_file_path = Config.get_mashov_stat_file_path()
            if os.path.isfile(stat_file_path):
                os.remove(stat_file_path)
