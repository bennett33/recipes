from flask import render_template, redirect, request, session, url_for
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/recipes/new')
def new_recipe():
    if 'uuid' not in session:
        return redirect('/logout')
    data = {
        "id":session['uuid']
    }
    return render_template('new_recipe.html',user=User.get_by_id(data))


@app.route("/recipes/create", methods = ['POST'])
def create_recipe():
    if 'uuid' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "under_30": int(request.form["under_30"]),
        "user_id": session["uuid"]
    }
    Recipe.save(data)
    return redirect('/dashboard')


@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'uuid' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template("display_recipe.html",recipe=Recipe.get_by_id(data))


@app.route('/recipes/destroy/<int:id>')
def destroy_recipe(id):
    if 'uuid' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')


@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'uuid' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['uuid']
    }
    return render_template("edit_recipe.html",edit=Recipe.get_by_id(data),user=User.get_by_id(user_data))


@app.route('/recipes/update/<int:id>',methods=['POST'])
def update_recipe(id):
    if 'uuid' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30": int(request.form["under_30"]),
        "date_made": request.form["date_made"],
        "id": id
    }
    Recipe.update(data)
    return redirect('/dashboard')