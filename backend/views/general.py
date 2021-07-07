from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from backend.utils import check_password, hash_password, requires_api_login
from backend.database import Project, db_session, User
from backend.schema import project_schema, projects_schema
mod = Blueprint('general', __name__)

@mod.post('/project')
@requires_api_login
def create_project():
    data = request.get_json()
    name = data['name']
    project: Project = Project(name=name)
    project.manager_id = g.user.id
    db_session.add(project)
    db_session.commit()

    return {
        'success': True,
        'message': "Project created successfully",
        "id": project.id,
        'name': project.name,
    }
    
@mod.get('/project')
@requires_api_login
def get_projects_list():
    return jsonify({
        'created_projects': projects_schema.dump(Project.query.filter_by(manager_id=g.user.id).all()),
        'projects_you_contribute_to': projects_schema.dump(g.user.projects),
        'all': projects_schema(g.user.projects | Project.query.filter_by(manager_id=g.user.id).all()),
    })


@mod.get('/project/<int:project_id>/')
@requires_api_login
def get_project_details(project_id: int):
    project = g.user.projects.filter_by(id=project_id)
    if not project:
        project = Project.query.filter_by(id=project_id, manager_id=g.user.id)
    
    return {
        'success': True,
        'result': project_schema.dump(project),
    }