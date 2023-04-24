import database.database as db


import streamlit_authenticator as stauth
names     = ['']
usernames = ['']
passwords = ['']
roles = ['']
hashed_passwords = stauth.Hasher(passwords).generate()

for(username, name, hashed_password, role) in zip (usernames, names, hashed_passwords, roles):
    db.insert_user(username, name, hashed_password, role)