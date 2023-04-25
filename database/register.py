import database as db


import streamlit_authenticator as stauth
names     = ['nelson']
usernames = ['nelson']
passwords = ['12345678']
roles = ['full']
hashed_passwords = stauth.Hasher(passwords).generate()

for(username, name, hashed_password, role) in zip (usernames, names, hashed_passwords, roles):
    db.insert_user(username, name, hashed_password, role)