from flaks import Flask, session
from uuid import uuid4
import pickle, os
from models import FlaskSession
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from database import db_session

class SQLAlchemySession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        Callbackdict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False
