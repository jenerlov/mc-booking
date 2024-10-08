from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, VARCHAR
from sqlalchemy.orm import sessionmaker, relationship,declarative_base
from datetime import datetime

Base = declarative_base()

# Tabellen för bokningar
class Booking(Base):
    __tablename__ = 'bookings'
    
    booking_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    service_id = Column(Integer, ForeignKey('services.service_id'))
    mechanic_id = Column(Integer, ForeignKey('mechanics.mechanic_id'))
    booking_date = Column(DateTime)
    status = Column(String)
    
    customer = relationship("Customer", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")
    mechanic = relationship("Mechanic", back_populates="bookings")
    orders = relationship("Order", back_populates="booking")
    payments = relationship("Payment", back_populates="booking")
    logistics = relationship("Logistic", back_populates="booking")

# Tabellen för beställningar
class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'))
    inventory_id = Column(Integer, ForeignKey('inventory.inventory_id'))
    item_name = Column(String)
    quantity = Column(Integer)
    status = Column(String)

    booking = relationship("Booking", back_populates="orders")
    inventory = relationship("Inventory", back_populates="orders")

class Service(Base):
    __tablename__ = 'services'

    service_id = Column(Integer, primary_key=True)
    service_name = Column(VARCHAR(255), nullable=False)
    description = Column(VARCHAR(255), nullable=False)
    cost = Column(Integer, nullable=False)

    bookings = relationship('Booking', back_populates='service')

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    address = Column(VARCHAR(255), nullable=False)
    phone = Column(String(20), nullable=False)  # Phone numbers should be stored as strings
    email = Column(VARCHAR(255), nullable=False)
    motorcycle_model = Column(VARCHAR(255), nullable=False)

    bookings = relationship('Booking', back_populates='customer')

class Payment(Base):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    payment_method = Column(VARCHAR(50), nullable=False)

    booking = relationship('Booking', back_populates='payments')
    

class Logistic(Base):
    __tablename__ = 'logistics'

    logistics_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.booking_id'), nullable=False)
    pickup_location = Column(String, nullable=False)
    dropoff_location = Column(String, nullable=False)
    pickup_date = Column(DateTime, nullable=False)
    dropoff_date = Column(DateTime, nullable=False)

    booking = relationship('Booking', back_populates='logistics')

class Inventory(Base):
    __tablename__ = 'inventory'

    inventory_id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)

    orders = relationship('Order', back_populates='inventory')  

class Mechanic(Base):
    __tablename__ = 'mechanics'

    mechanic_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialization = Column(String)

    bookings = relationship('Booking', back_populates='mechanic')

#skapa databas och engine
db = "sqlite:///bokningssystem.db"
engine = create_engine(db)
Base.metadata.create_all(bind=engine)

#skapa session
Session = sessionmaker(bind=engine)
session = Session()


#Lägg till ny bokning i Booking-tabellen
def add_booking(customer_id, service_id, mechanic_id, booking_date, status):
    # Skapa en ny bokning
    new_booking = Booking(
        customer_id=customer_id,
        service_id=service_id,
        mechanic_id=mechanic_id,
        booking_date=booking_date,
        status=status
    )

    # Lägg till bokningen i sessionen
    session.add(new_booking)
    
    # Spara ändringar i databasen
    session.commit()
    
    print("Bokningen har lagts till framgångsrikt!")

def add_mechanic(name, specialization):
    new_mechanic = Mechanic(
        name=name,
        specialization=specialization
    )

    session.add(new_mechanic)
    session.commit()
    print('Mekaniker har lagts till')

def add_logistic(booking_id, pickup_location,dropoff_location,pickup_date, dropoff_date):
    new_logistic = Logistic(
        booking_id=booking_id,
        pickup_location=pickup_location,
        dropoff_location=dropoff_location,
        pickup_date=pickup_date,
        dropoff_date=dropoff_date,
    )
    session.add(new_logistic)
    session.commit()
    print('Logistik har lagts till')

def add_inventory(item_name, quantity, unit_price):
    new_inventory = Inventory(
        item_name=item_name,
        quantity=quantity,
        unit_price=unit_price
    )
    session.add(new_inventory)
    session.commit()
    print('Lagerstatus har lagts till')

#Lägg till en ny beställning i Order-tabellen
def add_order(booking_id, inventory_id, item_name, quantity, status):
    # Skapa en ny beställning
    new_order = Order(
        booking_id=booking_id,
        inventory_id=inventory_id,
        item_name=item_name,
        quantity=quantity,
        status=status
    )
    
    # Lägg till beställningen i sessionen
    session.add(new_order)
    
    # Spara ändringar i databasen
    session.commit()
    
    print("Beställningen har lagts till framgångsrikt!")

#Lägg till data

#lägg till bokning
customer_id= 1
service_id= 1
mechanic_id= 1 
booking_date= datetime.strptime("2024-08-30", "%Y-%m-%d" ) #format?
status= "pågående"
add_booking(customer_id, service_id, mechanic_id, booking_date, status)


#Lägg till order
booking_id= 1
inventory_id= 1
item_name= "avgasrör"
quantity= 1
status= "skickad"
add_order(booking_id, inventory_id, item_name, quantity, status)


# Testdata för logistik (logistic)
add_logistic(
    booking_id=1,  # Kontrollera att detta booking_id finns i tabellen 'bookings'
    pickup_location="Kundens hem",
    dropoff_location="Verkstad",
    pickup_date=datetime.strptime("2024-09-01 08:00", "%Y-%m-%d %H:%M"),
    dropoff_date=datetime.strptime("2024-09-01 09:00", "%Y-%m-%d %H:%M")
)

add_logistic(
    booking_id=2,  # Kontrollera att detta booking_id finns i tabellen 'bookings'
    pickup_location="Garage",
    dropoff_location="Verkstad",
    pickup_date=datetime.strptime("2024-09-02 10:00", "%Y-%m-%d %H:%M"),
    dropoff_date=datetime.strptime("2024-09-02 11:30", "%Y-%m-%d %H:%M")
)

add_logistic(
    booking_id=3,  # Kontrollera att detta booking_id finns i tabellen 'bookings'
    pickup_location="Företagsparkering",
    dropoff_location="Verkstad",
    pickup_date=datetime.strptime("2024-09-03 07:30", "%Y-%m-%d %H:%M"),
    dropoff_date=datetime.strptime("2024-09-03 08:30", "%Y-%m-%d %H:%M")
)

# Testdata för mekaniker
add_mechanic("Erik Johansson", "Broms- och däckspecialist")
add_mechanic("Sara Nilsson", "Elektronikspecialist")
add_mechanic("Mikael Berg", "Kylsystem och klimatanläggning")

# Testdata för inventory (lager)
add_inventory("Bromsbelägg", 20, 300)
add_inventory("Tändstift", 50, 40)
add_inventory("Motorolja", 100, 150)

def add_service(service_name, description, cost):
    # Skapa en ny tjänst
    new_service = Service(
        service_name=service_name,
        description=description,
        cost=cost
    )

    # Lägg till tjänsten i sessionen
    session.add(new_service)
    
    # Spara ändringar i databasen
    session.commit()
    
    print("Tjänsten har lagts till framgångsrikt!")

def add_customer(first_name, last_name, address, phone, email, motorcycle_model):
    # Skapa en ny kund
    new_customer = Customer(
        first_name=first_name,
        last_name=last_name,
        address=address,
        phone=phone,
        email=email,
        motorcycle_model=motorcycle_model
    )

    # Lägg till kunden i sessionen
    session.add(new_customer)
    
    # Spara ändringar i databasen
    session.commit()
    
    print("Kunden har lagts till framgångsrikt!")


def add_payment(booking_id, amount, payment_date, payment_method):
    # Skapa en ny betalning
    new_payment = Payment(
        booking_id=booking_id,
        amount=amount,
        payment_date=payment_date,
        payment_method=payment_method
    )

    # Lägg till betalningen i sessionen
    session.add(new_payment)
    
    # Spara ändringar i databasen
    session.commit()
    
    print("Betalningen har lagts till framgångsrikt!")



# Example: Adding a new service
service_name = "Oil Change"
description = "Full oil change with synthetic oil"
cost = 120
add_service(service_name, description, cost)

service_name = "Tire Replacement"
description = "Complete tire replacement with balancing"
cost = 200
add_service(service_name, description, cost)

service_name = "Brake Inspection"
description = "Comprehensive brake system inspection"
cost = 85
add_service(service_name, description, cost)

# Example: Adding a new customer
first_name = "John"
last_name = "Doe"
address = "1234 Elm Street"
phone = "123-456-7890"
email = "john.doe@example.com"
motorcycle_model = "Harley Davidson"
add_customer(first_name, last_name, address, phone, email, motorcycle_model)

first_name = "Michael"
last_name = "Williams"
address = "9101 Oak Lane"
phone = "555-789-0123"
email = "michael.williams@example.com"
motorcycle_model = "Ducati Monster"
add_customer(first_name, last_name, address, phone, email, motorcycle_model)

first_name = "Emily"
last_name = "Johnson"
address = "5678 Maple Avenue"
phone = "987-654-3210"
email = "emily.johnson@example.com"
motorcycle_model = "Yamaha R1"
add_customer(first_name, last_name, address, phone, email, motorcycle_model)

# Example: Adding a new payment
booking_id = 1  # Assuming the booking with ID 1 already exists
amount = 120
payment_date = datetime.strptime("2024-08-31", "%Y-%m-%d")
payment_method = "Credit Card"
add_payment(booking_id, amount, payment_date, payment_method)

booking_id = 2  # Assuming the booking with ID 2 already exists
amount = 200
payment_date = datetime.strptime("2024-09-10", "%Y-%m-%d")
payment_method = "PayPal"
add_payment(booking_id, amount, payment_date, payment_method)

booking_id = 3  # Assuming the booking with ID 3 already exists
amount = 85
payment_date = datetime.strptime("2024-09-25", "%Y-%m-%d")
payment_method = "Cash"
add_payment(booking_id, amount, payment_date, payment_method)


