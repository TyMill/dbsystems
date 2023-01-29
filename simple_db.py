from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cash_spend = Column(Float)

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    zipcode = Column(String)
    country = Column(String)

class PurchaseHistory(Base):
    __tablename__ = 'purchase_history'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    product = Column(String)
    amount = Column(Float)

engine = create_engine('sqlite:///shopping.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

import random
from datetime import date, timedelta

def generate_random_string(length):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_customer():
    name = generate_random_string(10)
    cash_spend = round(random.uniform(100, 1000), 2)
    return Customer(name=name, cash_spend=cash_spend)

def generate_random_location():
    city = generate_random_string(10)
    zipcode = generate_random_string(5)
    country = generate_random_string(10)
    return Location(city=city, zipcode=zipcode, country=country)

def generate_random_purchase():
    date = date.today() - timedelta(days=random.randint(0, 365))
    product = generate_random_string(10)
    amount = round(random.uniform(10, 100), 2)
    return PurchaseHistory(date=date, product=product, amount=amount)

# Generate random data
num_customers = 100
num_locations = 50
num_purchases = 1000

customers = [generate_random_customer() for i in range(num_customers)]
locations = [generate_random_location() for i in range(num_locations)]
purchases = [generate_random_purchase() for i in range(num_purchases)]

# Assign random location to each customer
for customer in customers:
    customer.location_id = random.choice(locations).id

# Assign random customer to each purchase
for purchase in purchases:
    purchase.customer_id = random.choice(customers).id

# Save the data to the database
session.add_all(customers)
session.add_all(locations)
session.add_all(purchases)
session.commit()

