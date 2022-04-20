from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Recipe:
    db = "recipes"
    def __init__(self,data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.users_id = data['users_id']

    @classmethod
    def create(cls,data):
        query = "INSERT into recipes (name, description, instructions, under_30, date_made, users_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(under_30)s,%(date_made)s,%(users_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if results: 
            return cls(results[0]) 

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def update(cls, data):
        query="UPDATE recipes SET name=%(name)s, description=%(description)s,instructions=%(instructions)s, updated_at=NOW(), users_id=%(users_id)s WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db(query,data)



    @staticmethod
    def is_valid_recipe(recipes):
        is_valid = True
        if len(recipes['name']) < 1:
            is_valid = False
            flash("Must have a Name.", "create_recipe")
        if len(recipes['description']) < 20:
            is_valid = False
            flash("Must have a brief description", 'create_recipe')
        if len(recipes['instructions']) < 20:
            is_valid = False
            flash("Must have instructions", 'create_recipe')
        if recipes['date_made'] == '':
            is_valid = False
            flash("Please fill out a creation date", 'create_recipe')
        return is_valid 

    
