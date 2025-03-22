import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize database connection parameters from environment variables"""
        load_dotenv()
        self.host = os.getenv('MYSQL_HOST')
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.database = os.getenv('MYSQL_DATABASE')
        self.connection = None
        self.cursor = None
        self._transaction_depth = 0
    
    def connect(self):
        """Establish connection to the database"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                self.cursor = self.connection.cursor(dictionary=True, buffered=True)
                print("Successfully connected to the database")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("Database connection closed")
    
    def start_transaction(self):
        """Start a new transaction or increment the transaction depth"""
        self._transaction_depth += 1
        if self._transaction_depth == 1:
            self.connect()
    
    def end_transaction(self):
        """End a transaction or decrement the transaction depth"""
        if self._transaction_depth > 0:
            self._transaction_depth -= 1
            if self._transaction_depth == 0:
                self.connection.commit()
                self.disconnect()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            if self._transaction_depth == 0:
                self.connect()
            
            print(f"Executing query: {query}")
            print(f"With parameters: {params}")
            
            self.cursor.execute(query, params or ())
            
            if query.lower().strip().startswith('select'):
                result = self.cursor.fetchall()
            else:
                # Only commit if we're not in a transaction
                if self._transaction_depth == 0:
                    self.connection.commit()
                result = self.cursor.rowcount
            
            # Ensure all results are consumed
            while self.cursor.nextset():
                pass
            
            if self._transaction_depth == 0:
                self.disconnect()
            
            return result
            
        except Error as e:
            print(f"Error executing query: {e}")
            print(f"Query was: {query}")
            print(f"Parameters were: {params}")
            raise

    def execute_many(self, query, params_list):
        """Execute multiple queries with different parameters"""
        try:
            self.connect()
            self.cursor.executemany(query, params_list)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"Error executing multiple queries: {e}")
            raise
        finally:
            self.disconnect()

# Create tables if they don't exist
def initialize_database():
    db = DatabaseManager()
    
    # Players table
    create_players_table = """
    CREATE TABLE IF NOT EXISTS players (
        id BIGINT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        level INT DEFAULT 1,
        experience INT DEFAULT 0,
        coins INT DEFAULT 100,
        current_location VARCHAR(255) DEFAULT 'Whiskerton',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # Cats table (player's collected cats)
    create_cats_table = """
    CREATE TABLE IF NOT EXISTS cats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player_id BIGINT,
        name VARCHAR(255) NOT NULL,
        breed VARCHAR(255) NOT NULL,
        level INT DEFAULT 1,
        experience INT DEFAULT 0,
        health INT DEFAULT 100,
        attack INT DEFAULT 10,
        defense INT DEFAULT 10,
        speed INT DEFAULT 10,
        is_active BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (player_id) REFERENCES players(id)
    )
    """
    
    # Inventory table
    create_inventory_table = """
    CREATE TABLE IF NOT EXISTS inventory (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player_id BIGINT,
        item_id INT,
        quantity INT DEFAULT 1,
        FOREIGN KEY (player_id) REFERENCES players(id)
    )
    """
    
    # Items table
    create_items_table = """
    CREATE TABLE IF NOT EXISTS items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        type ENUM('weapon', 'armor', 'potion', 'material', 'misc') NOT NULL,
        rarity ENUM('common', 'uncommon', 'rare', 'epic', 'legendary') NOT NULL,
        value INT DEFAULT 0,
        image_path VARCHAR(255) DEFAULT 'images/items/eternal_scroll_of_meowgic.png'
    )
    """
    
    # Locations table
    create_locations_table = """
    CREATE TABLE IF NOT EXISTS locations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        region VARCHAR(255) NOT NULL,
        level_requirement INT DEFAULT 1,
        is_combat_zone BOOLEAN DEFAULT FALSE
    )
    """
    
    # Execute all create table queries
    tables = [
        create_players_table,
        create_cats_table,
        create_inventory_table,
        create_items_table,
        create_locations_table
    ]
    
    for table_query in tables:
        db.execute_query(table_query) 