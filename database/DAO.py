from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNodes():
        # Carica tutti gli oggetti della tabella objects, restituendoli come lista di ArtObject.
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []  # Lista di ArtOjbect

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM objects o"""

        cursor.execute(query)

        for row in cursor:
            result.append(ArtObject(**row))  # --> OGNI RIGA DEL DB DIVENTA UN OGGETTO

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMapO):
        # Carica tutti gli oggetti della tabella objects, restituendoli come lista di ArtObject.
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []  # Lista di ArtOjbect

        cursor = conn.cursor(dictionary=True)
        query = """ select eo1.object_id as o1, eo2.object_id as o2, count(eo1.exhibition_id ) as peso
                    from exhibition_objects eo1, exhibition_objects eo2
                    where eo1.exhibition_id = eo2. exhibition_id 
                        and eo1.object_id > eo2.object_id 
                    group by eo1.object_id, eo2.object_id """

        cursor.execute(query)

        for row in cursor:
            o1=idMapO[row['o1']]
            o2=idMapO[row['o2']]
            peso=row['peso']
            result.append(Arco(o1, o2, peso))  # --> OGNI RIGA DEL DB DIVENTA UN OGGETTO

        cursor.close()
        conn.close()
        return result
