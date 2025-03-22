from .database import DatabaseManager

class BaseModel:
    table_name = None
    primary_key = 'id'
    
    def __init__(self, **kwargs):
        self.db = DatabaseManager()
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def get_by_id(cls, id_value):
        db = DatabaseManager()
        query = f"SELECT * FROM {cls.table_name} WHERE {cls.primary_key} = %s"
        results = db.execute_query(query, (id_value,))
        if results:
            return cls(**results[0])
        return None
    
    @classmethod
    def get_all(cls, where_clause=None, params=None):
        db = DatabaseManager()
        query = f"SELECT * FROM {cls.table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        results = db.execute_query(query, params)
        return [cls(**result) for result in results]
    
    def save(self):
        """Save or update the model instance"""
        try:
            self.db.start_transaction()
            
            if hasattr(self, self.primary_key) and getattr(self, self.primary_key) is not None:
                result = self._update()
            else:
                result = self._create()
            
            self.db.end_transaction()
            return result
            
        except Exception as e:
            self.db.end_transaction()
            raise
    
    def _create(self):
        """Insert a new record"""
        fields = []
        values = []
        placeholders = []
        
        for key, value in vars(self).items():
            if key != 'db' and not key.startswith('_') and value is not None:
                fields.append(key)
                values.append(value)
                placeholders.append('%s')
        
        query = f"""
            INSERT INTO {self.table_name} 
            ({', '.join(fields)}) 
            VALUES ({', '.join(placeholders)})
        """
        
        # Execute the insert and commit immediately
        result = self.db.execute_query(query, tuple(values))
        
        # Verify using the same database connection
        verify_query = f"SELECT * FROM {self.table_name} WHERE {self.primary_key} = %s"
        verify_result = self.db.execute_query(verify_query, (getattr(self, self.primary_key),))
        
        if not verify_result:
            raise Exception(f"Failed to create record in {self.table_name}")
        
        # Update the current instance with any default values from the database
        for key, value in verify_result[0].items():
            setattr(self, key, value)
        
        return True
    
    def _update(self):
        """Update an existing record"""
        updates = []
        values = []
        
        for key, value in vars(self).items():
            if key != 'db' and not key.startswith('_') and key != self.primary_key:
                updates.append(f"{key} = %s")
                values.append(value)
        
        # Add the primary key value for the WHERE clause
        values.append(getattr(self, self.primary_key))
        
        query = f"""
            UPDATE {self.table_name} 
            SET {', '.join(updates)}
            WHERE {self.primary_key} = %s
        """
        
        return self.db.execute_query(query, tuple(values))
    
    def delete(self):
        """Delete the record"""
        if not hasattr(self, self.primary_key):
            raise ValueError(f"Cannot delete without {self.primary_key}")
            
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = %s"
        return self.db.execute_query(query, (getattr(self, self.primary_key),)) 