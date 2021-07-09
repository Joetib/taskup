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
        'all': projects_schema.dump([*g.user.projects  ,*Project.query.filter_by(manager_id=g.user.id).all()]),
    })


@mod.get('/project/<int:project_id>/')
@requires_api_login
def get_project_details(project_id: int):
    print(dir(g.user.projects))
    projects = list(filter(lambda item: item.id == project_id, g.user.projects))
    if projects:
        project = projects[0]
    else:
        project = Project.query.filter_by(id=project_id, manager_id=g.user.id).first()
    print(project)
    return {
        'success': bool(project),
        'result': project_schema.dump(project) ,
        'message': "Found" if project else "Not Found",
    }

@mod.post("/project/<int:project_id>/add-contributor/")
@requires_api_login
def add_contributors_to_project(project_id: int):
    data = request.get_json()
    contributor_ids = data['contributors']
    project = Project.query.filter_by(id=project_id, manager_id=g.user.id).first()
    if not project:
        abort(405, "Not permitted")
    for contributor_id in contributor_ids:
        contributor = User.query.filter_by(id=contributor_id).first()
        if contributor:
            project.contributors.append(contributor)
    db_session.add(project)
    db_session.commit()
    return {
        'success': True, 
        'result': project_schema.dump(project),
        'message': "Successfully updated project",
    }

