import psycopg2

clientPostgreSQL = psycopg2.connect(dbname="app", user="admin", password="123", host="postgres")

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