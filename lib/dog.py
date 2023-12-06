import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    all = []

    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO dogs(name, breed) VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog
    
    @classmethod
    def all(cls):
        sql = """
            SELECT * FROM dogs
        """
        all_dogs = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in all_dogs]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs WHERE name = ? LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(dog)


    @classmethod
    def find_by_id(cls, dog_id):
        sql = """
            SELECT * FROM dogs WHERE id = ? LIMIT 1
        """
        dog = CURSOR.execute(sql, (dog_id,)).fetchone()
        return cls.new_from_db(dog) if dog else None

    @classmethod
    def find_or_create_by(cls, name, breed):
     existing_dog = cls.find_by_name_and_breed(name, breed)

     if existing_dog:
        return existing_dog

     new_dog = cls(name, breed)
     new_dog.save()

     return new_dog
    
    def save(self):
     if self.id is None:
        # Insert a new row into the database
        sql = """
            INSERT INTO dogs(name, breed) VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()

        # Update the instance's ID
        self.id = CURSOR.lastrowid
     else:
        # Handle cases where save is called on an existing record
        pass
    
    def update(self):
     if self.id is not None:
        # Update the dog's name in the database
        sql = """
            UPDATE dogs SET name = ? WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()
     else:
        # Handle cases where update is called on an unsaved record
        pass

