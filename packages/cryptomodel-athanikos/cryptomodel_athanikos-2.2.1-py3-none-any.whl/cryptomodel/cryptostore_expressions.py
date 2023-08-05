from mongoengine import *


class expression_variable(Document):
    meta = {'strict': False}
    variable_name = StringField()
    entity_name = StringField() # table / collection
    field_name = StringField()
    filter_by_name = StringField()
    filter_by_value = StringField()
    is_order_by = BooleanField()
    order_by_date_field_name = StringField()
    order_by_value = StringField() # desc / asc

