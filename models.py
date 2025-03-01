from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Defining metadata 
convention = {"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

# Setting up the database engine
engine = create_engine('sqlite:///freebies.db')

# Creating a session factory
Session = sessionmaker(bind=engine)
session = Session()  

# Association Table for Many-to-Many relationship
class CompanyDev(Base):
    __tablename__ = 'company_dev'
    
    company_id = Column(Integer(), ForeignKey('companies.id'), primary_key=True)
    dev_id = Column(Integer(), ForeignKey('devs.id'), primary_key=True)

    company = relationship('Company', backref=backref('company_devs'))
    dev = relationship('Dev', backref=backref('company_devs'))

# Models
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", backref="company")
    devs = relationship("Dev", secondary="company_dev", backref="companies")

    def give_freebie(self, dev, item_name, value):
        """Creates a new Freebie instance associated with this company and the given dev."""
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(new_freebie)
        session.commit()

    @classmethod
    def oldest_company(cls):
        """Returns the company with the earliest founding year."""
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    freebies = relationship("Freebie", backref="dev")

    def received_one(self, item_name):
        """Returns True if the dev has received a freebie with the given item_name."""
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        """Transfers a freebie to another dev if the freebie belongs to this dev."""
        if freebie in self.freebies:
            freebie.dev = dev
            session.commit()

    def __repr__(self):
        return f'<Dev {self.name}>'

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    def __repr__(self):
        return f'<Freebie {self.item_name} (Value: {self.value})>'
