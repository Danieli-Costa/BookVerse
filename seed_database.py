"""Script to seed database."""



import crud
import model
import server


model.connect_to_db(server.app)
model.db.create_all()