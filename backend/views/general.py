from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from backend.utils import check_password, hash_password, requires_api_login
from backend.database import Project, Task, db_session, User, Model, Message
from sqlalchemy import or_
from backend.schema import TaskDetailSchema, TaskSchema, project_schema, projects_schema, task_schema, tasks_schema
mod = Blueprint('general', __name__)

# Projects Routes-------------------------------------------------------------------------------------------------------------
@mod.post('/project/')
@requires_api_login
def create_project():
    data = request.get_json()
    name = data['name']
    description = data["description"]
    project: Project = Project(name=name, description=description)
    project.manager_id = g.user.id
    db_session.add(project)
    db_session.commit()

    return {
        'success': True,
        'message': "Project created successfully",
        "new_project": project_schema.dump(project),
        "result": {
            'created_projects': projects_schema.dump(Project.query.filter_by(manager_id=g.user.id).all()),
            'projects_you_contribute_to': projects_schema.dump(g.user.projects),
            'all': projects_schema.dump(set([*g.user.projects  ,*Project.query.filter_by(manager_id=g.user.id).all()])),
        },
    }

@mod.get('/project/')
@requires_api_login
def get_projects_list():
    return jsonify({
        "success": True,
        "message": "Successfully fetched projects.",
        "result": {
            'created_projects': projects_schema.dump(Project.query.filter_by(manager_id=g.user.id).all()),
            'projects_you_contribute_to': projects_schema.dump(g.user.projects),
            'all': projects_schema.dump(Project.query.filter(or_(Project.manager_id==g.user.id , Project.contributors.any(id=g.user.id))).all()),
        },
    })


@mod.get('/project/<int:project_id>/')
@requires_api_login
def get_project_details(project_id: int):
    projects = list(filter(lambda item: item.id == project_id, g.user.projects))
    if projects:
        project = projects[0]
    else:
        project = Project.query.filter_by(id=project_id, manager_id=g.user.id).first()
    return {
        'success': bool(project),
        'result': project_schema.dump(project),
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
   
# End of Project Routes-------------------------------------------------------------------------------------------------------------

# Tasks Routes----------------------------------------------------------------------------------------------------------------------

# Create tasks
@mod.post("/project/<int:project_id>/task/")
@requires_api_login
def create_task(project_id):
    data = request.get_json()
    name = data['name']
    description = data['description']
    project = Project.query.filter_by(id=project_id).first()
    if project:
        task = Task(name=name, description=description, project=project,created_by=g.user)
        db_session.add(task)
        db_session.commit()
        return {
            'success': True,
            'result': task_schema.dump(task),
            'message': "successfully created task.",
        }

# Route to get list of tasks
@mod.get('/task/')
@requires_api_login
def get_tasks_list():
    return jsonify({
        "success": True,
        "result": {
            'created_tasks': tasks_schema.dump(Task.query.filter_by(created_by_id=g.user.id).all()),
            'tasks_you_work_on': tasks_schema.dump(g.user.tasks).all(),
            'all': tasks_schema.dump(Task.query.filter(or_(Task.created_by_id==g.user.id, Task.project_id==g.user.project.id)).all()),
        },
        "message": "Successfully fetched all tasks.",
    })

#  Route to update old tasks
@mod.put('/task/<int:task_id>')  # @mod.route(('/task/<int:task_id>'), methods=['PUT'])
@requires_api_login
def update_task(task_id):
    """
        Since there is no defaual update query method in the SqlAlchemy Orm,
        check to see if task exist and then delete it as well as post new content with same ID
    """ 
    data = request.get_json()
    task_id = data['task_id']
    old_task = Task.query.filter_by(id=task_id).first_or_404(description='There is no task with ID of {}'.format(task_id))
    if old_task:
        db_session.delete(old_task)
        db_session.commit()
        name = data['name']
        project_id = data['project_id']
        description = data['description']
        new_task = Task(name=name, description=description, project_id=project_id, created_by=g.user)
        db_session.add(new_task)
        db_session.commit()
        return {
            'success': True,
            'result': task_schema.dump(new_task),
            'message': "Successfully Updated the Task.",
        }

# Route to delete completed tasks
@mod.delete('/task/<int:task_id>')   # @mod.route(('/task/<int:task_id>'), methods=['DELETE'])
@requires_api_login
def delete_task(task_id):
    data = request.get_json()
    task_id = data['task_id']
    task = Task.query.filter_by(id=task_id).first_or_404(description='There is no task with ID of {}'.format(task_id))
    if task:
        db_session.delete(task)
        db_session.commit()
        return {
            'success': True,
            'result': tasks_schema.dump(g.user.tasks).all(),
            'message': "Task Deleted Successfully.",
        }

# End of Tasks Routes-------------------------------------------------------------------------------------------------------------

def has_project_permission(project, user):
    permission =  project.manager == user or project.contributors.any(id=user.id)
    if not permission:
        abort(404, {
            'success': False,
            'message': f"Permission denied.",
        } )
    return permission

# Added by PM: Later sort it out to see if functionality conflicts with get_task_list route
@mod.get('/project/<int:project_id>/task/<int:task_id>/')
@requires_api_login
def get_task_details(project_id, task_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    permission = has_project_permission(project, g.user)
    task = Task.query.filter_by(project=project, id=task_id).first()
    if not task:
        return {
            'success': False,
            'message': f'Task with id {task_id} not found.'
        }
    return {
        'success': True,
        'message': 'Task found.',
        'result': TaskDetailSchema().dump(task),
    }


@mod.post('/project/<int:project_id>/task/<int:task_id>/message/')
@requires_api_login
def create_message(project_id, task_id):
    message_content = request.get_json()['message']
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    permission = has_project_permission(project, g.user)
    task = Task.query.filter_by(project=project, id=task_id).first()
    if not task:
        return {
            'success': False,
            'message': f'Task with id {task_id} not found.'
        }
    message = Message(message=message_content, created_by=g.user, task=task)
    db_session.add(message)
    db_session.commit()
    return {
        'success': True,
        'message': 'Message created Successfully.',
        'result': {'message': message.message}
    }
