#!/usr/bin/env python3

from sqlalchemy import create_engine
from models import session, Company, Dev, Freebie  # Import session

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    import ipdb; ipdb.set_trace()
