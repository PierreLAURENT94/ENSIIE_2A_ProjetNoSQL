import streamlit as st
from mongoDB import *
from postgreSQL import *

tabEnregistrerEleve, tabListeEleve, tabEnregistrerMatiere, tabListeMatiere = st.tabs(["Enregistrer un Résultat", "Liste des Résultats", "Enregistrer une Matière", "Liste des Matières"])

with tabEnregistrerEleve:
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
                eleveMongoDB = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matiereMongoDB.split(":")[0]}
                addEleveMongoDB(eleveMongoDB)
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
                eleveMongoDB = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matiereMongoDB.split(":")[0]}
                elevePostgreSQL = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matierePostgreSQL.split(":")[0]}
                addEleveMongoDB(eleveMongoDB)
                addElevePostgreSQL(elevePostgreSQL)
                st.success("Résultat de l'élève enregistré sur MongoDB et PostgreSQL", icon="✅")
                st.snow()

    with colEnregistrerPostgreSQL:
        if st.button("Enregistrer sur PostgreSQL", type="secondary", use_container_width=True):
            if matierePostgreSQL != None:
                elevePostgreSQL = {'nom': nom, 'prenom': prenom, 'note': note, 'matiere_id': matierePostgreSQL.split(":")[0]}
                addElevePostgreSQL(elevePostgreSQL)
                st.success("Résultat de l'élève enregistré sur PostgreSQL", icon="✅")
                st.balloons()
            else:
                st.error('Veuillez sélectionner une "Matière PostgreSQL"', icon="🚨")

with tabListeEleve:
    st.title("Liste des Résultats")
    colListeMongoDB, colListePostgreSQL = st.columns(2)

    with colListeMongoDB:
        st.header("MongoDB")
        eleves = getElevesMongoDB()
        elevesList = list(eleves)
        # st.write(eleves)
        if elevesList:
            st.table([{"Nom": eleve['nom'], "Prénom": eleve['prenom'], "Note": eleve['note'], "Matière": getMatiereByIdMongoDB(eleve['matiere_id'])['intitule']} for eleve in elevesList])
        else:
            st.warning("Aucun résultat trouvé dans MongoDB", icon="⚠️")

    with colListePostgreSQL:
        st.header("PostgreSQL")
        eleves = getElevesPostgreSQL()
        # st.write(eleves)
        if eleves:
            st.table([{"Nom": eleve[0], "Prénom": eleve[1], "Note": eleve[2], "Matière": eleve[3]} for eleve in eleves]) 
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
