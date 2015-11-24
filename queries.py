from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DatabaseSession = sessionmaker(bind = engine)
session = DatabaseSession()

# firstPuppy = session.query(Puppy).first()
# print firstPuppy.name

dishes = session.query(MenuItem).all()
for dish in dishes:
    print 'working,...'
    print dish.name
    print "\n"
    print "\n"
