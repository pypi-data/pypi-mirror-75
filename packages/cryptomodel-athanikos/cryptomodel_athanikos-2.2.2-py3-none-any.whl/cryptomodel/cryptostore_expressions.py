from mongoengine import *

ORDER_BY_VALUES = (
    'asc',
    'desc'
)

ENTITIES = (
    'prices',
    'transactions'
)

AGGREGATE_TYPES = (
    'SUM',
    'MAX',
    'AVG',
    'MIN',
    ''
)


class filterItem(Document):
    field_name = StringField()
    operator = StringField()
    field_type = StringField()
    parameter_name = StringField()


class orderByItem(Document):
    name = StringField()
    value = StringField(choices=ORDER_BY_VALUES)


'''
examples:
get latest price for symbol = BTC ==>  get_prices.where(symbol == BTC AND date latest)
this requires variable_name = symbols (corresponds to some get symbols method with parameter symbol = BTC and dt = today
with is_top_1 = True (since it will get the first record)
ordered by dt desc
'''


class query(Document):
    meta = {'strict': False}
    name = StringField()
    entity_name = StringField(choices=ENTITIES)

    filters = ListField(EmbeddedDocumentListField(filterItem, db_field='filters'))

    orderByItems = ListField(EmbeddedDocumentListField(orderByItem, db_field='orderByItems'))

    is_top = BooleanField()
    top_value = IntField()
    applies_aggregate = BooleanField()
    aggregate_type = StringField(choices=AGGREGATE_TYPES)
