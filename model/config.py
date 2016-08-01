from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////home/pi/Codes/whoishome/devices.db', echo=True)
DBSession = sessionmaker(bind=engine)
