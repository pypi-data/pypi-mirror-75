import psycopg2 as sql


class PostgreSql:
    def __init__(self, db_host):
        self._connection = sql.connect(db_host, sslmode='require')
        self._cursor = self._connection.cursor()

    def fetchall(self, request: str):
        """
        Выполняем запрос `request`
        и возвращаем результат используя fetchall
        """

        self._cursor.execute(request)
        return self._cursor.fetchall()

    def execute(self, request: str):
        """ Выполняем запрос `request` """

        self._cursor.execute(request)

    def commit(self):
        self._connection.commit()

    def close(self):
        self._cursor.close()
        self._connection.close()
