import sqlalchemy as sq
from sqlalchemy import ForeignKey, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

print('Укажите пользователя, пароль и название базы данных на строках 7-9')
username = 'укажите пользователя'
password = 'укажите пароль'
db_name = 'укажите называние базы данных'

engine = sq.create_engine(f'postgresql+psycopg2://{username}:{password}@localhost:5432/{db_name}')
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
Base = declarative_base()

metadata = MetaData()

publisher = Table('publisher', metadata,
                  sq.Column('id', sq.INTEGER, primary_key = True),
                  sq.Column('name', sq.String),
                  )

book = Table('book', metadata,
             sq.Column('id', sq.INTEGER, primary_key = True),
             sq.Column('title', sq.String),
             sq.Column('id_publ', sq.INTEGER, ForeignKey('publisher.id'))
             )

shop = Table('shop', metadata,
                  sq.Column('id', sq.INTEGER, primary_key = True),
                  sq.Column('name', sq.String),
                  )

stock = Table('stock', metadata,
              sq.Column('id', sq.INTEGER, primary_key = True),
              sq.Column('count', sq.INTEGER),
              sq.Column('id_book', sq.INTEGER, ForeignKey('book.id')),
              sq.Column('id_shop', sq.INTEGER, ForeignKey('shop.id'))
              )

sale = Table('sale', metadata,
             sq.Column('id', sq.INTEGER, primary_key = True),
             sq.Column('price', sq.DECIMAL),
             sq.Column('date_sale', sq.DATE),
             sq.Column('count', sq.INTEGER),
             sq.Column('id_stock', sq.INTEGER, ForeignKey('stock.id'))
             )

metadata.create_all(engine)

class Publisher(Base):
    __tablename__ = 'publisher'
    id = sq.Column(sq.INTEGER, primary_key = True)
    name = sq.Column(sq.String)
    book = relationship('Book', backref='publisher')

class Book(Base):
    __tablename__ = 'book'
    id = sq.Column(sq.INTEGER, primary_key = True)
    title = sq.Column(sq.String)
    id_publ = sq.Column(sq.INTEGER, ForeignKey('publisher.id'))
    stock = relationship('Stock', backref='book')

class Shop(Base):
    __tablename__ = 'shop'
    id = sq.Column(sq.INTEGER, primary_key = True )
    name = sq.Column(sq.String )
    stock = relationship('Stock', backref='shop')

class Stock(Base):
    __tablename__ = 'stock'
    id = sq.Column(sq.INTEGER, primary_key = True)
    count = sq.Column(sq.INTEGER)
    id_book = sq.Column(sq.INTEGER, ForeignKey('book.id'))
    id_shop = sq.Column(sq.INTEGER, ForeignKey('shop.id'))
    sale = relationship('Sale', backref='stock')

class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.INTEGER, primary_key = True)
    price = sq.Column(sq.DECIMAL)
    date_sale = sq.Column(sq.DATE)
    count = sq.Column(sq.INTEGER)
    id_stock = sq.Column(sq.INTEGER, ForeignKey('stock.id'))

session = Session()

def add_f(obj):
    session.add(obj)
    session.commit()

pub1 = Publisher(name='Дрофа')
pub2 = Publisher(name='МиФ')
add_f(pub1)
add_f(pub2)

b1 = Book(title='Азбука', id_publ=pub1.id)
b2 = Book(title='Евгений Онегин', id_publ=pub2.id)
b3 = Book(title='Герой нашего времени', id_publ=pub1.id)
b4 = Book(title='Война и мир', id_publ=pub2.id)
add_f(b1)
add_f(b2)
add_f(b3)
add_f(b4)

sh1 = Shop(name='ЦУМ')
sh2 = Shop(name='Детский мир')
add_f(sh1)
add_f(sh2)

st1 = Stock(id_book=b1.id, id_shop=sh1.id, count=1)
st2 = Stock(id_book=b2.id, id_shop=sh2.id, count=2)
st3 = Stock(id_book=b3.id, id_shop=sh1.id, count=3)
st4 = Stock(id_book=b4.id, id_shop=sh2.id, count=4)
add_f(st1)
add_f(st2)
add_f(st3)
add_f(st4)

sl1 = Sale(price=1.5, date_sale = '1/1/2020', id_stock=st1.id, count=1)
sl2 = Sale(price=2.5, date_sale = '1/1/2019', id_stock=st2.id, count=2)
sl3 = Sale(price=3.5, date_sale = '1/2/2019', id_stock=st3.id, count=3)
sl4 = Sale(price=4.5, date_sale = '2/1/2018', id_stock=st4.id, count=4)
add_f(sl1)
add_f(sl2)
add_f(sl3)
add_f(sl4)

inp = input('Введите имя издательства. Возможные варианты (МиФ, Дрофа): ')
pub_id = session.query(Publisher.id).filter(Publisher.name == inp)
q = session.query(Book.title).filter(Book.id_publ == pub_id).all()
print(f'Издательство выпустило книгу (книги): {q}')