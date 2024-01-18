import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def add_bessem():
  final_value = calulate_besem()
  users = anvil.users.get_user()
  if users:
    email = users['email']
    data = app_tables.fin_user_profile.search(email_user=email)
    if data:
      data[0]['bessem_value']=final_value


def calulate_besem():
  return 80


def fetch_bessem(email):
  users = app_tables.fin_user_profile.search(email_user=email)
  if users:
    bessem_values = users[0]['bessem_value']
    return bessem_values
  else:
    return 0