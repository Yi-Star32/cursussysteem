from mijnproject import db
from mijnproject.models import Inschrijving, Les

def koppel_studenten_aan_lessen():
    # Haal alle lessen op
    lessen = Les.query.all()

    for les in lessen:
        # Zoek alle inschrijvingen voor de cursus van deze les
        inschrijvingen = Inschrijving.query.filter_by(cursus_id=les.id_cursus).all()

        for inschrijving in inschrijvingen:
            # Controleer of de student al gekoppeld is aan de les
            if les.id_klant != int(inschrijving.klant_id):
                # Voeg de student toe aan de les
                new_les = Les(
                    id_klant=int(inschrijving.klant_id) if isinstance(inschrijving.klant_id, str) else inschrijving.klant_id,
                    id_docent=int(les.id_docent) if isinstance(les.id_docent, str) else les.id_docent,
                    id_cursus=int(les.id_cursus) if isinstance(les.id_cursus, str) else les.id_cursus,
                    datetime=int(les.datetime),
                    locatie=les.locatie
                    )

                db.session.add(new_les)

    db.session.commit()