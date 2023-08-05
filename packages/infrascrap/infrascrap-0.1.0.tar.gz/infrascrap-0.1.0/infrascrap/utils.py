import re
import os
import keyring
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from contextlib import contextmanager
from .exceptions import MissingBitWardenToken, BrowserException

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

    def _bw_password(self):
        if os.environ.get('BW_SESSION') is None:
            raise MissingBitWardenToken('You did not login to bitwarden - Expecting BW_SESSION env var..')
        return keyring.get_password(self.bw_service,
                                    self.username)

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
        return webdriver.Chrome(options=chrome_options)
    try:
        _browser = init_browser(headless)
        yield _browser
    except Exception as exc:
        raise BrowserException(exc)
    finally:
        _browser.quit()
