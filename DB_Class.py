import sqlite3

class RealEstateDB:
    def __init__(self):
        self.conn = sqlite3.connect('filteredlistings.db')
        self.cur = self.conn.cursor()

        # Create table
        self.cur.execute('''CREATE TABLE IF NOT EXISTS listings_realestatecomau
                        (
                            listing_id INTEGER, title TEXT, type TEXT, address TEXT,
                            bed_rooms INTEGER, bond INTEGER, rent INTEGER, rent_per_room INTEGER,
                            agency TEXT, agent_name TEXT, agent_mail TEXT, url TEXT, 
                            mail_text TEXT, mail_subject TEXT, mail_confirmed_by_human BOOLEAN
                            PRIMARY KEY (listing_id)
                        )''')

        # Create temporary table
        self.cur.execute('''CREATE TEMPORARY TABLE listings_realestatecomau_temp
                            (
                                listing_id INTEGER, title TEXT, type TEXT, address TEXT,
                                bed_rooms INTEGER, bond INTEGER, rent INTEGER, rent_per_room INTEGER,
                                agency TEXT, agent_name TEXT, agent_mail TEXT, url TEXT, 
                                mail_text TEXT, mail_subject TEXT, mail_confirmed_by_human BOOLEAN
                                PRIMARY KEY (listing_id)
                            )''')

    def insert_listing(self, listing):

        sql_query = """INSERT INTO listings_realestatecomau_temp(
            listing_id, 
            title, 
            type, 
            address, 
            bed_rooms, 
            bond, 
            rent, 
            rent_per_room, 
            agency, 
            agent_name, 
            agent_mail, 
            url, 
            mail_text, 
            mail_subject
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        # Extract values from dictionary and insert into table
        values = (listing['listing_id'], listing['title'], listing['type'], listing['address_str'], listing['bed_rooms'], listing['bond'], listing['rent'], listing['rent_per_room'], listing['agency'], listing['agent_name'], listing['agent_mail'], listing['url'], listing['mail_text'], listing['mail_subject'])
        self.cur.execute(sql_query, values)

        # Insert only new rows into main table
        self.cur.execute('''INSERT OR IGNORE INTO listings_realestatecomau
                            (title, type, address, bed_rooms, bond, rent, rent_per_room,
                            agency, agent_name, agent_mail, url, listing_id)
                            SELECT title, type, address, bed_rooms, bond, rent, rent_per_room,
                            agency, agent_name, agent_mail, url, listing_id FROM listings_realestatecomau_temp''')

        self.conn.commit()

    
    def get_confirmed_rows(self):
        # retrieve all rows where mail_confirmed_by_human is true
        self.cur.execute("SELECT * FROM realestatecomau WHERE mail_confirmed_by_human = 1")
        rows = self.cur.fetchall()
        return rows
