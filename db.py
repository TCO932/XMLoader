import cx_Oracle

class DB:
    def __init__(self, conn_str, table_name):
        self._connection = cx_Oracle.connect(conn_str)
        self._table_name = table_name

    def __del__(self):
        self._connection.close()

    def selectById(self, id):
        cursor = self._connection.cursor()
        sql = f"""SELECT * FROM {self._table_name} WHERE id = :id"""
        cursor.execute(sql, id=id)
        result = cursor.fetchone()
        # print(f'row selected: {cursor.rowcount}')
        return result

    def selectAll(self):
        cursor = self._connection.cursor()
        sql = f"""SELECT XML_NAME, id FROM {self._table_name}"""
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(f'rows selected: {cursor.rowcount}')
        return result

    def insert(self, name, xml_file):
        cursor = self._connection.cursor()
        sql = f"""INSERT INTO {self._table_name} (XML_NAME, XML) VALUES(:xml_name, xmltype(:xml))"""
        cursor.execute(sql, xml_name=name, xml=xml_file)
        self._connection.commit()
        # print(f'rows inserted: {cursor.rowcount}')

    def update(self, id, name, xml_file):
        cursor = self._connection.cursor()
        sql = f"""UPDATE {self._table_name} SET XML_NAME = :xml_name, XML = xmltype(:xml) WHERE id = :id"""
        cursor.execute(sql, id=id, xml_name=name, xml=xml_file)
        self._connection.commit()
        # print(f'row updated: {cursor.rowcount}')