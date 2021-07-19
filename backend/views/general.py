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

def has_project_permission(project, user):
    permission =  project.manager == user or project.contributors.any(id=user.id)
    if not permission:
        abort(404, {
            'success': False,
            'message': f"Permission denied.",
        } )
    return permission
    
# Tasks Routes----------------------------------------------------------------------------------------------------------------------

# Create tasks
@mod.post("/project/<int:project_id>/task/")
@requires_api_login
def create_task(project_id):
    data = request.get_json()
    name = data['name']
    description = data['description']
    completion_status = data['completion_status']
    created_date = data['created_date']
    deadline_date = data['deadline_date']
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    else:
        permission = has_project_permission(project, g.user)
        task = Task(
            name=name, description=description, completion_status=completion_status,
            created_date = created_date, deadline_date = deadline_date, project_id=project_id, created_by=g.user)
        db_session.add(task)
        db_session.commit()
        return {
            'success': True,
            'result': task_schema.dump(task),
            'message': "Task Successfully Created.",
        }

# Route to get list of tasks associated with a project
@mod.get('/project/<int:project_id>/task/')
@requires_api_login
def get_tasks_list(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    permission = has_project_permission(project, g.user)
    return jsonify({
        "success": True,
        "result": {
            'created_tasks': tasks_schema.dump(Task.query.filter_by(created_by_id=g.user.id).all()),
            'tasks_you_work_on': tasks_schema.dump(g.user.tasks).all(),
            'all': tasks_schema.dump(Task.query.filter(or_(Task.created_by_id==g.user.id, Task.project_id==g.user.project.id)).all()),
        },
        "message": "Successfully fetched all tasks.",
    })

#  Route to update tasks
@mod.put('/project/<int:project_id>/task/<int:task_id>')
@requires_api_login
def update_task(project_id,task_id):
    """
        Since there is no default update query method in the Flask-SqlAlchemy Orm,
        check to see if task exist and then delete it as well as post new content with same ID
    """
    data = request.get_json()
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    permission = has_project_permission(project, g.user)
    old_task = Task.query.filter_by(id=task_id).first_or_404(description= f'There is no task with ID of {task_id}.')
    if old_task:
        db_session.delete(old_task)
        db_session.commit()
        name = data['name']
        project_id = data['project_id']
        description = data['description']
        completion_status = data['completion_status']
        created_date = data['created_date']
        deadline_date = data['deadline_date']
        new_task = Task(
            name=name, description=description, completion_status=completion_status,
            created_date = created_date, deadline_date = deadline_date, project_id=project_id, created_by=g.user)
        db_session.add(new_task)
        db_session.commit()
        return {
            'success': True,
            'result': task_schema.dump(new_task),
            'message': "Successfully Updated the Task.",
        }

# Route to delete tasks
@mod.delete('/project/<int:project_id>/task/<int:task_id>')
@requires_api_login
def delete_task(project_id, task_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    permission = has_project_permission(project, g.user)
    task = Task.query.filter_by(id=task_id).first_or_404(description= f'There is no task with ID of {task_id}')
    if task:
        db_session.delete(task)
        db_session.commit()
        return {
            'success': True,
            'result': tasks_schema.dump(g.user.tasks).all(),
            'message': "Task Deleted Successfully.",
        }

# Route to edit completion status of tasks
@mod.put('/project/<int:project_id>/task/<int:task_id, string:completion_status>')
@requires_api_login
def update_status(project_id, task_id, completion_status):
    """
        User with permissions can replace completion status of task if it exists and is part of the project
    """
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    permission = has_project_permission(project, g.user)
    task = Task.query.filter_by(id=task_id).first_or_404(description=f'There is no task with ID of {task_id}.')
    if task:
        task.completion_status = completion_status
        db_session.add(task)
        db_session.commit()
        return {
            'success': True,
            'result': task_schema.dump(task),
            'message': f"Successfully Updated the Completion Status of {task.name}."
        }

# Route to edit timelines of tasks
@mod.put('/project/<int:project_id>/task/<int:task_id, datetime:deadline_date>')
@requires_api_login
def update_status(project_id, task_id, deadline_date):
    """
        Follows the same logic as the update_status route
    """
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    permission = has_project_permission(project, g.user)
    task = Task.query.filter_by(id=task_id).first_or_404(description=f'There is no task with ID of {task_id}.')
    if task:
        task.deadline_date = deadline_date
        db_session.add(task)
        db_session.commit()
        return {
            'success': True,
            'result': task_schema.dump(task),
            'message': f"Successfully Updated the Deadline of {task.name}."
        }
# End of Tasks Routes-------------------------------------------------------------------------------------------------------------

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
