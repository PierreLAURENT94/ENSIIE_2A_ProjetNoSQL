import psycopg2

clientPostgreSQL = psycopg2.connect(dbname="app", user="admin", password="123", host="postgres")

def addResultatPostgreSQL(resultat):
    cur = clientPostgreSQL.cursor()
    cur.execute("""INSERT INTO resultats (nom, prenom, note, matiere_id) VALUES (%s, %s, %s, %s)""", (resultat['nom'], resultat['prenom'], resultat['note'], resultat['matiere_id']))
    clientPostgreSQL.commit()
    cur.close()

def getResultatsPostgreSQL():
    cur = clientPostgreSQL.cursor()
    cur.execute("SELECT nom, prenom, note, intitule FROM resultats LEFT JOIN matieres ON (matieres.id = resultats.matiere_id)")
    resultats = cur.fetchall()
    cur.close()
    return resultats

def addMatierePostgreSQL(resultat):
    cur = clientPostgreSQL.cursor()
    cur.execute("""INSERT INTO matieres (intitule, prof) VALUES (%s, %s)""", (resultat['intitule'], resultat['prof']))
    clientPostgreSQL.commit()
    cur.close()

def getMatieresPostgreSQL():
    cur = clientPostgreSQL.cursor()
    cur.execute("SELECT * FROM matieres")
    resultats = cur.fetchall()
    cur.close()
    return resultats