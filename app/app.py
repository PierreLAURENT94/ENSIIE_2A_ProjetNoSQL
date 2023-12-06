import streamlit as st
import pymongo
import psycopg2

clientMongoDB = pymongo.MongoClient("mongodb://mongodb:27017/")

clientPostgreSQL = psycopg2.connect(dbname="app", user="admin", password="123", host="postgres")

def addMongoDB(eleve):
    db = clientMongoDB["app"]
    collection = db["eleves"]
    collection.insert_one(eleve)

def addPostgreSQL(eleve):
    cur = clientPostgreSQL.cursor()
    cur.execute("""INSERT INTO eleves (nom, prenom, note) VALUES (%s, %s, %s)""", (eleve['nom'], eleve['prenom'], eleve['note']))
    clientPostgreSQL.commit()
    cur.close()

def getPostgreSQL():
    cur = clientPostgreSQL.cursor()
    cur.execute("SELECT * FROM eleves")
    eleves = cur.fetchall()
    cur.close()
    return eleves

def getMongoDB():
    db = clientMongoDB["app"]
    collection = db["eleves"]
    return collection.find()

# Streamlit

tabEnregistrer, tabListe = st.tabs(["Enregistrer un Élève", "Liste des Élèves"])

with tabEnregistrer:
    st.title("Enregistrer un Élève")
    nom = st.text_input("Nom :")
    prenom = st.text_input("Prénom :")
    note = st.slider('Note :', 0, 20, 10)

    colEnregistrerMongoDB, colEnregistrerLesDeux, colEnregistrerPostgreSQL = st.columns(3)

    with colEnregistrerMongoDB:
        if st.button("Enregistrer sur MongoDB", type="secondary", use_container_width=True):
            eleve = {'nom': nom, 'prenom': prenom, 'note': note}
            addMongoDB(eleve)
            st.success("Profil de l'élève enregistré sur MongoDB", icon="✅")
    
    with colEnregistrerLesDeux:
        if st.button("Enregistrer sur les deux", type="primary", use_container_width=True):
            eleve = {'nom': nom, 'prenom': prenom, 'note': note}
            addMongoDB(eleve)
            addPostgreSQL(eleve)
            st.success("Profil de l'élève enregistré sur MongoDB et PostgreSQL", icon="✅")

    with colEnregistrerPostgreSQL:
        if st.button("Enregistrer sur PostgreSQL", type="secondary", use_container_width=True):
            eleve = {'nom': nom, 'prenom': prenom, 'note': note}
            addPostgreSQL(eleve)
            st.success("Profil de l'élève enregistré sur PostgreSQL", icon="✅")
        

with tabListe:
    st.title("Liste des Élèves")
    colListeMongoDB, colListePostgreSQL = st.columns(2)

    with colListeMongoDB:
        st.header("MongoDB")
        eleves = getMongoDB()
        elevesList = list(eleves)
        # st.write(eleves)
        if elevesList:
            st.table([{"Nom": eleve['nom'], "Prénom": eleve['prenom'], "Note": eleve['note']} for eleve in elevesList])
        else:
            st.warning("Aucun élève trouvé dans MongoDB", icon="⚠️")

    with colListePostgreSQL:
        st.header("PostgreSQL")
        eleves = getPostgreSQL()
        # st.write(eleves)
        if eleves:
            st.table([{"Nom": eleve[1], "Prénom": eleve[2], "Note": eleve[3]} for eleve in eleves]) 
        else:
            st.warning("Aucun élève trouvé dans PostgreSQL", icon="⚠️")

# st.balloons()
# st.snow()