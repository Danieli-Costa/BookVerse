"""Script to seed database."""
import server
import model
import crud
import requests
import json
import os

# API keys
NYT_API_KEY = os.environ["NYT_API_KEY"]
GOOGLE_BOOKS_KEY = os.environ["GOOGLE_BOOKS_KEY"]

# Connect to database and create all tables
model.connect_to_db(server.app)
model.db.create_all()
