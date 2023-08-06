from keyring import get_password
from mongoengine import *
from cryptomodel.operations import OPERATIONS
from cryptomodel.order_types import ORDER_TYPES
from cryptomodel.transaction_types import TRANSACTION_TYPES


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
    fields_to_send = StringField()
    source_id = ObjectIdField()
    operation = StringField(choices=OPERATIONS.choices())


class user_transaction(Document):
    meta = {'strict': False}
    user_id = IntField()
    volume = FloatField()
    symbol = StringField()
    value = FloatField()
    price = FloatField()
    date = DateField()
    source = StringField()
    currency = StringField()
    order_type = StringField(choices=ORDER_TYPES.choices())
    type = StringField(choices=TRANSACTION_TYPES.choices())
    source_id = ObjectIdField()
    operation = StringField(choices=OPERATIONS.choices())
    is_valid = BooleanField(default=True)
    invalid_reason = StringField(default="")

    def validate_symbol(self, symbols):
        if symbols is None:
            self.is_valid = False
            self.invalid_reason = "symbol list empty " + self.symbol
            return self.is_valid

        if self.symbol not in symbols.keys():
            self.is_valid = False
            self.invalid_reason = "symbol does not exist in list value:" + self.symbol
        return self.is_valid


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
