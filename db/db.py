from peewee import PostgresqlDatabase

from db import settings

db = PostgresqlDatabase(
   database=settings.DATABASE['NAME'],
   user=settings.DATABASE['USER'],
   password=settings.DATABASE['PASSWORD'],
   host=settings.DATABASE['HOST'],
   port=settings.DATABASE['PORT']
)
