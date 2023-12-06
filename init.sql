\c app;

CREATE TABLE eleves (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    note INTEGER,
    matiere_id INTEGER REFERENCES matieres(id)
);

CREATE TABLE matieres (
    id SERIAL PRIMARY KEY,
    intitule VARCHAR(255),
    prof VARCHAR(255)
);