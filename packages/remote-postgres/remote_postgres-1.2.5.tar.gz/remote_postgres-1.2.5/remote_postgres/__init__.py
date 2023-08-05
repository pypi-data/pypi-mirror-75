import psycopg2, psycopg2.extras
class RemotePostgres:
    def __init__(self, dsn):
        self.dsn = dsn
        self.con = psycopg2.connect(dsn)
    def __del__(self):
        self.con.close()
    def get_count(self, tbl_name):
        return self.select(f"""SELECT COUNT(*) FROM \"{tbl_name}\"""")[0]['count']
    def get_counts(self):
        tables = self.select("""SELECT tablename FROM pg_tables WHERE schemaname = 'public'""")
        return [{t['tablename']: self.get_count(t['tablename'])} for t in tables]
    def select(self, select_statement='SELECT * FROM pg_tables'):
        cur = self.con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(select_statement)
        records = [dict(row) for row in cur.fetchall()]
        return records
    def insert(self, tbl_name, records):
        cur = self.con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        for record in records:
            field_names = ','.join([f'"{k}"' for k in record.keys()])
            placeholders = ','.join(['%s' for k in record.keys()])
            insert_statement = f'INSERT INTO "{tbl_name}" ({field_names}) VALUES ({placeholders})'
            values = tuple(record.values())
            cur.execute(insert_statement, values)
        self.con.commit()
    def generate_create_table(self, tbl_name, records):
        columns = ', '.join([f'"{k}" TEXT' for k in records[0].keys()])
        return f'CREATE TABLE "{tbl_name}" ({columns})'
