import streamlit as st
from mongoDB import *
from postgreSQL import *

tabEnregistrerResultat, tabListeResultat, tabEnregistrerMatiere, tabListeMatiere = st.tabs(["Enregistrer un Résultat", "Liste des Résultats", "Enregistrer une Matière", "Liste des Matières"])

with tabEnregistrerResultat:
    st.title("Enregistrer un Résultat")
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
            if matiereMongoDB != None:
                resultatMongoDB = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matiereMongoDB.split(":")[0]}
                addResultatMongoDB(resultatMongoDB)
                st.success("Résultat de l'élève enregistré sur MongoDB", icon="✅")
                st.balloons()
            else:
                st.error('Veuillez sélectionner une "Matière MongoDB"', icon="🚨")
    
    with colEnregistrerLesDeux:
        if st.button("Enregistrer sur les deux", type="primary", use_container_width=True):
            if matiereMongoDB == None:
                st.error('Veuillez sélectionner une "Matière MongoDB"', icon="🚨")
            elif matierePostgreSQL == None:
                st.error('Veuillez sélectionner une "Matière PostgreSQL"', icon="🚨")
            else:
                resultatMongoDB = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matiereMongoDB.split(":")[0]}
                resultatPostgreSQL = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matierePostgreSQL.split(":")[0]}
                addResultatMongoDB(resultatMongoDB)
                addResultatPostgreSQL(resultatPostgreSQL)
                st.success("Résultat de l'élève enregistré sur MongoDB et PostgreSQL", icon="✅")
                st.snow()

    with colEnregistrerPostgreSQL:
        if st.button("Enregistrer sur PostgreSQL", type="secondary", use_container_width=True):
            if matierePostgreSQL != None:
                resultatPostgreSQL = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matierePostgreSQL.split(":")[0]}
                addResultatPostgreSQL(resultatPostgreSQL)
                st.success("Résultat de l'élève enregistré sur PostgreSQL", icon="✅")
                st.balloons()
            else:
                st.error('Veuillez sélectionner une "Matière PostgreSQL"', icon="🚨")

with tabListeResultat:
    st.title("Liste des Résultats")
    colListeMongoDB, colListePostgreSQL = st.columns(2)

    with colListeMongoDB:
        st.header("MongoDB")
        resultats = getResultatsMongoDB()
        resultatsList = list(resultats)
        # st.write(resultats)
        if resultatsList:
            st.table([{"Nom": resultat['nom'], "Prénom": resultat['prenom'], "Note": resultat['note'], "Matière": getMatiereByIdMongoDB(resultat['matiere_id'])['intitule']} for resultat in resultatsList])
        else:
            st.warning("Aucun résultat trouvé dans MongoDB", icon="⚠️")

    with colListePostgreSQL:
        st.header("PostgreSQL")
        resultats = getResultatsPostgreSQL()
        # st.write(resultats)
        if resultats:
            st.table([{"Nom": resultat[0], "Prénom": resultat[1], "Note": resultat[2], "Matière": resultat[3]} for resultat in resultats]) 
        else:
            st.warning("Aucun résultat trouvé dans PostgreSQL", icon="⚠️")

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
