import database as db


import streamlit_authenticator as stauth
names     = ['lorena', 'julio', 'juan', 'jose']
usernames = ['lorena', 'julio','juan', 'jose']
passwords = '12345678'
roles = ['full', 'operaciones', 'comercial', 'full']
hashed_passwords = stauth.Hasher([passwords]).generate()
print(hashed_passwords)
#for(username, name, hashed_password, role) in zip (usernames, names, hashed_passwords, roles):
#    db.insert_user(username, name, hashed_password, role)
print(db.fecth_all_users()) 