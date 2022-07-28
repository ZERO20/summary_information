from peewee import AutoField, CharField, DateField, ForeignKeyField, Model, FloatField

from db.db import db


class Account(Model):
   id = AutoField()
   name = CharField()
   paternal_surname = CharField()
   maternal_surname = CharField()
   email = CharField(unique=True)

   class Meta:
       database = db


class Transaction(Model):
   id = AutoField()
   number = CharField()
   date = CharField()
   amount = FloatField()
   account = ForeignKeyField(Account)

   class Meta:
       database = db


db.connect()
db.create_tables([Account, Transaction])
