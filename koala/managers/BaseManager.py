
from koala import settings, application
from koala.models import Post, Item
from koala.providers import provider
from koala.util.parser import parsePhone
from koala.webutils import getReferer
from myutil import idtool
from myutil.objdict import ObjDict
import json
import logging


class BaseManager:
    pass