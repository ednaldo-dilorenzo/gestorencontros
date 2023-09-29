import csv
import psycopg2

conn = psycopg2.connect(
    dbname="encontros", user="master", password="secret", host="localhost", port="5432"
)
cur = conn.cursor()

with open("/home/edsf/Downloads/montagem-ecc-2023.csv", "r") as f:
    reader = csv.reader(f, delimiter=",", quotechar='"')
    for index, row in enumerate(reader):
        if index < 2:
            continue

        casal = row[1].split("\n")
        telefones = row[2].split("\n")
        cur.execute(
            "INSERT INTO pessoa (nome, apelido, telefone, id_paroquia) VALUES (%s, %s, %s, %s) RETURNING id",
            [casal[0].strip(), casal[0].strip(), telefones[0].strip(), 1],
        )
        id_marido = cur.fetchone()
        cur.execute(
            "INSERT INTO pessoa (nome, apelido, telefone, id_paroquia) VALUES (%s, %s, %s, %s) RETURNING id",
            [
                casal[1].strip(),
                casal[1].strip(),
                telefones[1].strip() if len(telefones) > 1 else "999999999",
                1,
            ],
        )
        id_esposa = cur.fetchone()
        cur.execute(
            "INSERT INTO casal (id_esposo, id_esposa, id_paroquia, extenso) VALUES (%s, %s, %s, %s) RETURNING id",
            [
                id_marido,
                id_esposa,
                1,
                f"{casal[0].strip().lower()} {casal[1].strip().lower()}",
            ],
        )
        print(casal)
        id_casal = cur.fetchone()
        cur.execute("SELECT id FROM equipe WHERE UPPER(nome) = %s", [row[3].upper()])
        id_equipe = cur.fetchone()[0]
        aceito = row[4].lower() == "sim"
        cur.execute(
            f"INSERT INTO equipe_encontro_casal (id_equipe, id_encontro, id_casal, coordenador, aceito) VALUES ({id_equipe}, 1, {id_casal[0]}, FALSE, {'TRUE' if aceito else 'FALSE'})"
        )

    conn.commit()
