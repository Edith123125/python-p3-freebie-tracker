from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie, CompanyDev

engine = create_engine("sqlite:///freebies.db")
Session = sessionmaker(bind=engine)
session = Session()

# Creating sample companies
company1 = Company(name="Google", founding_year=1998)
company2 = Company(name="Microsoft", founding_year=1975)

# Creating sample developers
dev1 = Dev(name="Alice")
dev2 = Dev(name="Bob")

# Creating sample freebies
freebie1 = Freebie(item_name="T-Shirt", value=10, company=company1, dev=dev1)
freebie2 = Freebie(item_name="Mug", value=5, company=company2, dev=dev2)

# Add the dev-company relationship explicitly for many-to-many
company1.devs.append(dev1)
company2.devs.append(dev2)

# Adding all the instances to the session
session.add_all([company1, company2, dev1, dev2, freebie1, freebie2])
session.commit()

print("✅ Database seeded successfully!")
