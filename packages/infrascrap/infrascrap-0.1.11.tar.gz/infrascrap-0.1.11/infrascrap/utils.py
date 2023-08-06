import re
import os
import keyring
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from contextlib import contextmanager
from .exceptions import MissingBitWardenToken, BrowserException
from pyvirtualdisplay import Display

class BaseScrap:

    def __init__(self, cfg):
        if not all([e in cfg for e in ('username', 'bitwarden_service')]):
            raise KeyError('Missing one or more of the keys: username,bitwarden_service in config')

        self.username = cfg['username']
        self.bw_service = cfg['bitwarden_service']
        self.set_attrs_by_cfg_params(cfg)

    @property
    def pw(self):
        return self._bw_password


    def _bw_cmd_get_pw(self):
        return ['bw', 'get', 'password']

    def _bw_cmd_get_pw_with_session(self):
        returned = self._bw_cmd_get_pw()

        if os.environ.get('BW_SESSION') is None:
            raise MissingBitWardenToken('You did not login to bitwarden - Expecting BW_SESSION env var..')

        returned.append('--session')
        returned.append(os.environ.get('BW_SESSION'))
        returned.append(self.bw_service)
        return returned

    def _bw_password(self):
        return subprocess.check_output(self._bw_cmd_get_pw_with_session())
        # return keyring.get_password(self.bw_service,
        #                             self.username)

    def set_attrs_by_cfg_params(self, cfg):
        ''' config may contain keys like _param_<param name>
        and this function should set self.<param_name> with the value from config
        '''
        for k, val in cfg.items():
            mtch = re.search("_param_(.*)", k)
            if mtch:
                self.__setattr__(mtch.group(1), val)

@contextmanager
def BrowserGCM(headless=True):
    ''' Browser context manager implemented with generators'''
    def init_browser(_headless):
        chrome_options = Options()
        if _headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")

        try:
            display = Display(visible=0, size=(800, 600))
            display.start()
        except Exception as e:
            print(f'Failed loading virtual display {e}')
            raise BrowserException(f'Failed loading virtual display {e}')
        try:
            return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f'Webdrivewr.chrome failed {e}')
            raise BrowserException(f'Webdrivewr.chrome failed {e}')
    try:
        browser_cm = init_browser(headless)
        yield browser_cm
    except BrowserException as exc:
        # print(f'Failed init browser ?? {exc}')
        # raise BrowserException(f'Failed init browser ?? {exc}')
        raise
    finally:
        if browser_cm:
            browser_cm.quit()
