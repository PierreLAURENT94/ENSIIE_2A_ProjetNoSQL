\c app;

CREATE TABLE matieres (
    id SERIAL PRIMARY KEY,
    intitule VARCHAR(255),
    prof VARCHAR(255)
);

CREATE TABLE resultats (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    note INTEGER,
    matiere_id INTEGER REFERENCES matieres(id)
);
