from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.recipes_model import Recipe
from flask_app.models.user_model import User 

@app.route('/recipe')
def recipe_new():
    logged_in_user = User.get_by_id({'id':session['user_id']})
    return render_template('recipe.html', user = logged_in_user, recipes=Recipe)

@app.route('/recipe/create', methods=['POST'])
def recipe_create():
    if not Recipe.is_valid_recipe(request.form):
        return redirect('/recipe')
    data={
        **request.form,
        'users_id':session['user_id']
    }
    Recipe.create(data)
    return redirect('/dashboard')


# @app.route('/recipe/login', methods=['POST'])
# def recipe_login():
#     return render_template('/')

@app.route('/recipe/<int:id>/view')
def recipe_show(id):
    view = {
        'id':id
    }
    recipe = Recipe.get_by_id(view)
    logged_in_user = User.get_by_id({'id':session['user_id']})
    return render_template('view.html', user = logged_in_user, recipe=recipe)

@app.route('/recipe/<int:id>/edit')
def recipe_edit(id):
    update = {
        'id':id
    }
    info = Recipe.get_by_id(update)
    recipe = Recipe.update(update)
    return render_template('update.html', recipe =  id, info=info)

@app.route('/recipe/<int:id>/update', methods=['POST'])
def recipe_update(id):
    if not Recipe.is_valid_recipe(request.form):
        return redirect(f'/recipe/{id}/edit')
    update = {
        **request.form,
        'id':id
    }
    Recipe.update(update)
    return redirect('/', recipe = id)

@app.route('/recipe/<int:id>/delete')
def recipe_delete(id):
    destroy = {
        'id':id
    }
    Recipe.destroy(destroy)
    return redirect('/dashboard')
