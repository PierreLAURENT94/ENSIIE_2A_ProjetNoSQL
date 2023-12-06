import streamlit as st
import pymongo
import psycopg2
from bson import ObjectId

clientMongoDB = pymongo.MongoClient("mongodb://mongodb:27017/")

clientPostgreSQL = psycopg2.connect(dbname="app", user="admin", password="123", host="postgres")

def addEleveMongoDB(eleve):
    db = clientMongoDB["app"]
    collection = db["eleves"]
    collection.insert_one(eleve)

def addElevePostgreSQL(eleve):
    cur = clientPostgreSQL.cursor()
    cur.execute("""INSERT INTO eleves (nom, prenom, note, matiere_id) VALUES (%s, %s, %s, %s)""", (eleve['nom'], eleve['prenom'], eleve['note'], eleve['matiere_id']))
    clientPostgreSQL.commit()
    cur.close()

def getElevesPostgreSQL():
    cur = clientPostgreSQL.cursor()
    cur.execute("SELECT nom, prenom, note, intitule FROM eleves LEFT JOIN matieres ON (matieres.id = eleves.matiere_id)")
    eleves = cur.fetchall()
    cur.close()
    return eleves

def getElevesMongoDB():
    db = clientMongoDB["app"]
    collection = db["eleves"]
    return collection.find()

def addMatiereMongoDB(matiere):
    db = clientMongoDB["app"]
    collection = db["matieres"]
    collection.insert_one(matiere)

def addMatierePostgreSQL(eleve):
    cur = clientPostgreSQL.cursor()
    cur.execute("""INSERT INTO matieres (intitule, prof) VALUES (%s, %s)""", (eleve['intitule'], eleve['prof']))
    clientPostgreSQL.commit()
    cur.close()

def getMatieresPostgreSQL():
    cur = clientPostgreSQL.cursor()
    cur.execute("SELECT * FROM matieres")
    eleves = cur.fetchall()
    cur.close()
    return eleves

def getMatieresMongoDB():
    db = clientMongoDB["app"]
    collection = db["matieres"]
    return collection.find()

def getMatiereByIdMongoDB(id):
    db = clientMongoDB["app"]
    collection = db["matieres"]
    return collection.find_one({'_id': ObjectId(id)})

# Streamlit

tabEnregistrerEleve, tabListeEleve, tabEnregistrerMatiere, tabListeMatiere = st.tabs(["Enregistrer un Élève", "Liste des Élèves", "Enregistrer une Matière", "Liste des Matières"])

with tabEnregistrerEleve:
    st.title("Enregistrer un Élève")
    nom = st.text_input("Nom :")
    prenom = st.text_input("Prénom :")
    note = st.slider('Note :', 0, 20, 10)

    colMatierePostgreSQL, colMatiereMongoDB = st.columns(2)

    with colMatierePostgreSQL:
        matierePostgreSQL = st.selectbox('Matière PostgreSQL', [str(matiere[0]) + ": " + matiere[1] + " • " + matiere[2] for matiere in getMatieresPostgreSQL()])
    with colMatiereMongoDB:
        matiereMongoDB = st.selectbox('Matière MongoDB', [str(matiere["_id"]) + ": " + matiere["intitule"] + " • " + matiere["prof"] for matiere in list(getMatieresMongoDB())])

    colEnregistrerMongoDB, colEnregistrerLesDeux, colEnregistrerPostgreSQL = st.columns(3)

    with colEnregistrerMongoDB:
        if st.button("Enregistrer sur MongoDB", type="secondary", use_container_width=True):
            eleveMongoDB = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matiereMongoDB.split(":")[0]}
            addEleveMongoDB(eleveMongoDB)
            st.success("Profil de l'élève enregistré sur MongoDB", icon="✅")
            st.balloons()
    
    with colEnregistrerLesDeux:
        if st.button("Enregistrer sur les deux", type="primary", use_container_width=True):
            eleveMongoDB = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matiereMongoDB.split(":")[0]}
            elevePostgreSQL = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matierePostgreSQL.split(":")[0]}
            addEleveMongoDB(eleveMongoDB)
            addElevePostgreSQL(elevePostgreSQL)
            st.success("Profil de l'élève enregistré sur MongoDB et PostgreSQL", icon="✅")
            st.snow()

    with colEnregistrerPostgreSQL:
        if st.button("Enregistrer sur PostgreSQL", type="secondary", use_container_width=True):
            elevePostgreSQL = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matierePostgreSQL.split(":")[0]}
            addElevePostgreSQL(elevePostgreSQL)
            st.success("Profil de l'élève enregistré sur PostgreSQL", icon="✅")
            st.balloons()  

with tabListeEleve:
    st.title("Liste des Élèves")
    colListeMongoDB, colListePostgreSQL = st.columns(2)

    with colListeMongoDB:
        st.header("MongoDB")
        eleves = getElevesMongoDB()
        elevesList = list(eleves)
        # st.write(eleves)
        if elevesList:
            st.table([{"Nom": eleve['nom'], "Prénom": eleve['prenom'], "Note": eleve['note'], "Matière": getMatiereByIdMongoDB(eleve['matiere_id'])['intitule']} for eleve in elevesList])
        else:
            st.warning("Aucun élève trouvé dans MongoDB", icon="⚠️")

    with colListePostgreSQL:
        st.header("PostgreSQL")
        eleves = getElevesPostgreSQL()
        # st.write(eleves)
        if eleves:
            st.table([{"Nom": eleve[0], "Prénom": eleve[1], "Note": eleve[2], "Matière": eleve[3]} for eleve in eleves]) 
        else:
            st.warning("Aucun élève trouvé dans PostgreSQL", icon="⚠️")

with tabEnregistrerMatiere:
    st.title("Enregistrer une Matière")
    intitule = st.text_input("Intitulé :")
    prof = st.text_input("Prof :")

    colEnregistrerMongoDB, colEnregistrerLesDeux, colEnregistrerPostgreSQL = st.columns(3)

    with colEnregistrerMongoDB:
        if st.button("Enregistrer sur MongoDB", type="secondary", use_container_width=True, key="EnregistrerMongoDBMatiere"):
            idMatiere = len(list(getMatieresMongoDB()))
            matiere = {'id': idMatiere, 'intitule': intitule, 'prof': prof}
            addMatiereMongoDB(matiere)
            st.success("Matière enregistrée sur MongoDB", icon="✅")
            st.balloons()
    
    with colEnregistrerLesDeux:
        if st.button("Enregistrer sur les deux", type="primary", use_container_width=True, key="EnregistrerDeuxMatiere"):
            matiere = {'intitule': intitule, 'prof': prof}
            addMatiereMongoDB(matiere)
            addMatierePostgreSQL(matiere)
            st.success("Matière enregistrée sur MongoDB et PostgreSQL", icon="✅")
            st.snow()

    with colEnregistrerPostgreSQL:
        if st.button("Enregistrer sur PostgreSQL", type="secondary", use_container_width=True, key="EnregistrerPostgreSQLMatiere"):
            matiere = {'intitule': intitule, 'prof': prof}
            addMatierePostgreSQL(matiere)
            st.success("Matière enregistrée sur PostgreSQL", icon="✅")
            st.balloons()

with tabListeMatiere:
    st.title("Liste des Matières")
    colListeMongoDB, colListePostgreSQL = st.columns(2)

    with colListeMongoDB:
        st.header("MongoDB")
        matieres = getMatieresMongoDB()
        matieresList = list(matieres)
        if matieresList:
            st.table([{"Intitule": matiere['intitule'], "Prof": matiere['prof']} for matiere in matieresList])
        else:
            st.warning("Aucune matière trouvée dans MongoDB", icon="⚠️")

    with colListePostgreSQL:
        st.header("PostgreSQL")
        matieres = getMatieresPostgreSQL()
        if matieres:
            st.table([{"Intitule": matiere[1], "Prof": matiere[2]} for matiere in matieres]) 
        else:
            st.warning("Aucune matière trouvée dans PostgreSQL", icon="⚠️")
