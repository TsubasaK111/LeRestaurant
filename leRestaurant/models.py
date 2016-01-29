from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    name          = Column( String(80), nullable = False )
    email         = Column( String() )
    picture       = Column( String() )
    link          = Column( String() )
    id            = Column( Integer, primary_key = True )


class Restaurant(Base):
    __tablename__ = 'restaurant'
    name          = Column( String(80), nullable = False )
    id            = Column( Integer, primary_key = True )
    user_id       = Column( Integer, ForeignKey('user.id') )
    user          = relationship(User)
    @property
    def serialize(self):
        #Returns object data in easily serializeable format.
        return {
            'name': self.name,
            'id': self.id,
        }

class MenuItem(Base):
    __tablename__ = 'menu_item'
    name          = Column( String(80), nullable = False )
    course        = Column( String(250) )
    description   = Column( String(250) )
    price         = Column( String(8) )
    id            = Column( Integer, primary_key = True )
    restaurant_id = Column( Integer, ForeignKey('restaurant.id') )
    restaurant    = relationship(Restaurant)
    user_id       = Column( Integer, ForeignKey('user.id') )
    user          = relationship(User)
    @property
    def serialize(self):
        #Returns object data in easily serializeable format.
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'restaurant_id': self.restaurant_id,
        }


engine = create_engine('sqlite:///restaurantmenu.db')


Base.metadata.create_all(engine)


#Base.metadata.bind = engine


DatabaseSession = sessionmaker(bind = engine)


session = DatabaseSession()
