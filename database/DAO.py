from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country
                from customer c
                where c.Country is not null
                order by c.Country
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ select distinct al.*
                    from track t,album al 
                    where t.AlbumId =al.AlbumId 
 """
            cursor.execute(query)

            for row in cursor:
                result.append(Album(**row))

            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getBraniPerAlbum(idA):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct t.TrackId 
                    from album al, track t 
                    where al.AlbumId=%s and al.AlbumId =t.AlbumId  """

        cursor.execute(query, (idA,))
        for row in cursor:
            results.append(row["TrackId"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getBraniPerAlbum(idA):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct t.TrackId 
                       from album al, track t 
                       where al.AlbumId=%s and al.AlbumId =t.AlbumId  """

        cursor.execute(query, (idA,))
        for row in cursor:
            results.append(row["TrackId"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getGeneriPerAlbum(idA):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                    select distinct g.GenreId 
                    from album al, track t , genre g 
                    where al.AlbumId=%s and al.AlbumId =t.AlbumId
                     and g.GenreId =t.GenreId 
                         """

        cursor.execute(query, (idA,))
        for row in cursor:
            results.append(row["GenreId"])

        cursor.close()
        conn.close()
        return results



