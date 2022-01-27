from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user 
from flask import flash


class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.user = user.User.get_by_id({"id": data["user_id"]})

    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (user_id, name, description, created_at, updated_at, date_made, under_30) VALUES (%(user_id)s, %(name)s, %(description)s, NOW(), NOW(), %(date_made)s, %(under_30)s);"
        return connectToMySQL("recipes").query_db(query, data)


    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, under_30, date_made, user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(under_30)s,%(date_made)s,%(user_id)s);"
        return connectToMySQL("recipes").query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL("recipes").query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL("recipes").query_db(query,data)
        return cls( results[0] )


    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30=%(under_30)s, date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL("recipes").query_db(query,data)
    
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL("recipes").query_db(query,data)


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters","recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","recipe")
        if recipe['date_made'] == "":
            is_valid = False
            flash("Please enter a date","recipe")
        return is_valid
