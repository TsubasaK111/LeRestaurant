from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()

dishes = session.query(MenuItem).all()
for dish in dishes:
    print 'working,...'
    print dish.name
    print "\n"
    print "\n"

restaurants = session.query(Restaurant).all()
for restaurant in restaurants:
    print restaurant.name
