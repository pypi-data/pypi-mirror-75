from keyring import get_password
from mongoengine import *
from cryptomodel.operations import OPERATIONS


class user_settings(Document):
    meta = {'strict': False}
    user_id = IntField()
    preferred_currency = StringField()
    source_id = ObjectIdField()
    operation = StringField(choices=OPERATIONS.choices())


class user_notification(Document):
    meta = {'strict': False}
    user_id = IntField()
    user_name = StringField()
    user_email = StringField()
    expression_to_evaluate = StringField()
    check_every_seconds = LongField()
    check_times = LongField()
    is_active = BooleanField()
    channel_type = StringField()
    fields_to_send = StringField()  ### collection:field latest date ?
    ### collection:field by latest user_id ?
    source_id = ObjectIdField()
    operation = StringField(choices=OPERATIONS.choices())


class user_transaction(Document):
    meta = {'strict': False}
    user_id = IntField()
    volume = LongField()
    symbol = StringField()
    value = LongField()
    price = LongField()
    date = DateField()
    source = StringField()
    currency = StringField()
    source_id = ObjectIdField()
    operation = StringField(choices=OPERATIONS.choices())


class user_channel(Document):
    meta = {'strict': False}
    user_id = IntField()
    channel_type = StringField()
    chat_id = StringField()
    user_email = StringField()
    source_id = ObjectIdField()
    operation = StringField(choices=OPERATIONS.choices())

    def set_token(self):
        self.token = get_password(self.notification_type, 'token')
