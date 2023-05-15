"""Script to seed database."""
import server
import model


# Connect to database and create all tables
model.connect_to_db(server.app)
model.db.create_all()
