import os
import toml

class Config:
    _CONFIG_PATH = os.path.expanduser("~/.scrap_config.toml")

    @classmethod
    def load(cls, grp=None):
        with open(cls._CONFIG_PATH, 'r') as fh:
            parsed_toml = toml.loads(fh.read())
        if grp:
            return parsed_toml['commands'][grp]
        return parsed_toml

    @classmethod
    def get_chat_id(cls, chname=None):
        if chname:
            with open(cls._CONFIG_PATH, 'r') as fh:
                return toml.loads(fh.read())['telegram']['chats']['id'].get(chname)

    @classmethod
    def get_bot_token(cls):
        with open(cls._CONFIG_PATH, 'r') as fh:
            return toml.loads(fh.read())['commands']['telegram']['bot_token']

    @classmethod
    def get_mashov_stat_file_path(cls):
        with open(cls._CONFIG_PATH, 'r') as fh:
            return toml.loads(fh.read())['commands']['mashov']['stat_img_file']
