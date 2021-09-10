from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from backend.utils import check_password, has_project_permission, hash_password, requires_api_login
from backend.database import Invitation, Project, Task, db_session, User, Model, Message
from sqlalchemy import or_
from backend.schema import InvitationDetailSchema, InvitationListSchema, TaskDetailSchema, TaskSchema, UserSchema, project_schema, projects_schema, task_schema, tasks_schema
import datetime

mod = Blueprint('general', __name__)

# Beginnig of Projects Routes--------------------------------------------------------------------------------------------------------------

@mod.post('/project/')
@requires_api_login
def create_project():
    data = request.get_json()
    name = data['name']
    description = data["description"]

    project: Project = Project(name=name, description=description) # the rest of the fields for the object has default values in the database
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



@mod.post("/project/<int:project_id>/edit/")
@requires_api_login
def edit_project(project_id):
    project = Project.query.filter_by(id=project_id, manager_id=g.user.id).first()
    if not project:
        return {
            'success': False,
            'message': f"Project with id {project_id} Not Found."
        }
    data = request.get_json()
    project.name = data['name']
    project.description = data["description"]

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
        'is_project_manager': g.user.id == project.manager_id
    }


@mod.get('/project/')
@requires_api_login
def search_for_keyword_in_project():
    keyword = request.get_json()
    searched_projects = []
    for keyword in Project.query.split():
        results = Project.query.filter(
            or_(
                Project.name.contains(keyword),
                Project.description.contains(keyword),
                Project.tasks.contains(keyword)
            )
        ).all()

        for project in results:
            searched_projects.append(project.name)
    return {
        'success': True,
        'message': "Search results" if searched_projects else "None Found",
        'result': projects_schema.dump(searched_projects),
    }

@mod.get('/task/')
@requires_api_login
def get_tasks():
    tasks = Task.query.filter(Task.task_workers.any(id=g.user.id))
    return {
        'success': True,
        'message': "Tasks fetched.",
        'result': tasks_schema.dump(tasks),
    }


@mod.post("/project/<int:project_id>/remove-contributor/")
@requires_api_login
def remove_contributors_from_project(project_id: int):
    data = request.get_json()
    contributor_ids = data['contributors']
    project = Project.query.filter_by(id=project_id, manager_id=g.user.id).first()
    if not project:
        abort(405, "Not permitted")
    permission = is_project_manager(project, g.user)
    for contributor_id in contributor_ids:
        contributor = User.query.filter_by(id=contributor_id).first()
        if contributor:
            try:
                project.contributors.remove(contributor)
                invitation  = Invitation.query.filter_by(project=project, user=contributor).first()
                if invitation:
                    db_session.delete(invitation)
            except:
                print(f"Error occurred removing user f{contributor.id} from project {project.id}")
    db_session.add(project)
    db_session.commit()
    return {
        'success': True, 
        'result': project_schema.dump(project),
        'message': "Successfully updated project",
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
            existing_invitation = Invitation.query.filter_by(user=contributor, project=project).first()
            if existing_invitation:
                return {

                    'success': False,
                    'message': f"Invitation to {contributor.name} already exists.",
                    'result': None,
                }
            invite =Invitation(project=project, user=contributor)
            db_session.add(invite)
    db_session.commit()
    return {
        'success': True, 
        'result': project_schema.dump(project),
        'message': "Successfully updated project",
    }

@mod.get('/project/<int:project_id>/task/<int:task_id>/contributors/')
@requires_api_login
def get_contributors_for_task(project_id, task_id):
    project = Project.query.filter_by(id=project_id).first()
    has_project_permission(project, g.user)
    task = Task.query.filter_by(id=task_id, project=project).first()
    if not task:
        abort(404, "Not found")

    return {
        'success': True,
        'message': "Project Found",
        'result': UserSchema(many=True).dump(task.task_workers),
        'all_users': UserSchema(many=True).dump(project.contributors + [g.user]),
    }

@mod.post("/project/<int:project_id>/task/<int:task_id>/add-contributor/")
@requires_api_login
def add_contributors_to_task(project_id: int, task_id:int):
    data = request.get_json()
    contributor_ids = data['contributors']
    project = Project.query.filter_by(id=project_id).first()
    has_project_permission(project, g.user)
    task: Task = Task.query.filter_by(id=task_id, project=project).first()
    if not task:
        abort(404, "Not found")
    for contributor_id in contributor_ids:
        contributor = User.query.filter_by(id=contributor_id).first()
        if contributor:
            task.task_workers.append(contributor)
    db_session.add(task)

    db_session.commit()
    return {
        'success': True, 
        'result': task_schema.dump(task),
        'message': "Successfully updated project",
    }

@mod.get('/invitation/')
@requires_api_login
def get_invitations():
    invitations  = Invitation.query.filter_by(accepted=False, user_id=g.user.id)
    return {
        'success': True,
        'result': InvitationDetailSchema(many=True).dump(invitations),
        'message': "Successfully retrieved invitations",
    }

@mod.get('/invitation/<int:invitation_id>/decline/')
@requires_api_login
def decline_invitation(invitation_id):
    invitation: Invitation  = Invitation.query.filter_by(id=invitation_id).first()
    if (not invitation) :
        abort(404, f"Invitation with id {invitation_id} was not found.")
    if all([(g.user != invitation.user), (g.user != invitation.project.manager)]):
        print(g.user != invitation.user)
        print(g.user != invitation.project.manager)
        abort(405, "Permission denied")
    db_session.delete(invitation)
    db_session.commit()
    return {
        'success': True,
        'message': "Invitation deleted successfully.",
        
    }
    
@mod.get('/invitation/<int:invitation_id>/accept/')
@requires_api_login
def accept_invitation(invitation_id):
    invitation  = Invitation.query.filter_by(id=invitation_id, user_id=g.user.id).first()
    if not invitation:
        abort(404, f"Invitation with id {invitation_id} was not found.")
    invitation.accepted = True
    project = invitation.project
    project.contributors.append(g.user)
    db_session.add(invitation)
    db_session.add(project)
    db_session.commit()
    return {
        'success': True,
        "result": InvitationDetailSchema().dump(invitation),
        "message": "Successully accepted Invitation",
    }

def is_project_manager(project, user):
    if project.manager == user:
        return True
    else:
        abort(404, {
            'success': False,
            'message': f"Permission denied.",
        } )

@mod.get('/project/<int:project_id>/contributors/')
@requires_api_login
def get_contributors_for_project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': "Project Not Found",
        }
    else:
        return {
            'success': True,
            'message': "Project Found",
            'all_users': UserSchema(many=True).dump(User.query.all()),
            'results': UserSchema(many=True).dump(project.contributors),
            'invites': InvitationListSchema(many=True).dump(Invitation.query.filter_by(accepted=False, project_id=project.id))
        }

@mod.delete('/project/<int:project_id>/delete/')
@requires_api_login
def delete_project(project_id):
    """
        Project managers can delete a project
    """
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }

    else:
        if is_project_manager(project, g.user):
            # delete related tasks
            Task.query.filter_by(project=project).delete()
            #delete related invites
            Invitation.query.filter_by(project=project).delete()
            db_session.delete(project)
            db_session.commit()
            return {
                'success': True,
                'result': {},
                'message': "Project Deleted Successfully.",
            }

@mod.put('/project/<int:project_id>/completion-status/')
@requires_api_login
def update_project_status(project_id):
    
    """
        Project managers can replace completion status of the project
    """
    completion_status = request.get_json()['completion_status']
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }

    else:
        if is_project_manager(project, g.user):
            project.completion_status = completion_status
            db_session.add(project)
            db_session.commit()
            return {
                'success': True,
                'result': task_schema.dump(project),
                'message': f"Successfully Updated the Completion Status of {project.name}."
            }

@mod.put('/project/<int:project_id>/<deadline_date>')
@requires_api_login
def update_project_deadline(project_id, deadline_date):
    """
        Project managers can change deadlines of projects
    """
    deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d").date() # there is no out-of-box support for dates in url routing
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }

    else:
        if is_project_manager(project, g.user):
            project.deadline_date = deadline_date
            db_session.add(project)
            db_session.commit()
            return {
                'success': True,
                'result': task_schema.dump(project),
                'message': f"Successfully Changed the Deadline of {project.name}."
            }

# End of Project Routes-------------------------------------------------------------------------------------------------------------


# Beginnig of Task Routes----------------------------------------------------------------------------------------------------------------------

@mod.post("/project/<int:project_id>/task/")
@requires_api_login
def create_task(project_id):
    data = request.get_json()
    name = data['name']
    description = data['description']

    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }

    else:
        permission = has_project_permission(project, g.user)
        task = Task(
            name = name, description = description,
            project_id = project_id, created_by = g.user) # the rest of the fields for the object has default values in the database
        db_session.add(task)
        db_session.commit()

        return {
            'success': True,
            'result': task_schema.dump(task),
            'message': "Task Successfully Created.",
        }

@mod.post("/project/<int:project_id>/task/<int:task_id>/edit/")
@requires_api_login
def edit_task(project_id, task_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }

    
    permission = has_project_permission(project, g.user)
    task: Task = Task.query.filter_by(id=task_id).first()
    if not task:
        abort(404, f'There is no task with ID of {task_id}.')
    data = request.get_json()
    task.name = data['name']
    task.description = data['description']
    db_session.add(task)
    db_session.commit()

    return {
        'success': True,
        'result': task_schema.dump(task),
        'message': "Task Successfully Created.",
    }


@mod.get('/project/<int:project_id>/task/')
@requires_api_login
def get_tasks_list(project_id):
    """ 
        Get list of tasks associated with a project
    """
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }

    else:
        permission = has_project_permission(project, g.user)
        return jsonify(
            {
                "success": True,
                "result": {
                    'created_tasks': tasks_schema.dump(Task.query.filter_by(created_by_id = g.user.id).all()),
                    'tasks_you_work_on': tasks_schema.dump(g.user.tasks).all(),
                    'all': tasks_schema.dump(Task.query.filter(or_(
                        Task.created_by_id==g.user.id, Task.project_id==g.user.project.id
                    )).all()),
                },
                "message": "Successfully fetched all tasks.",
            }
        )

@mod.put('/project/<int:project_id>/task/<int:task_id>')
@requires_api_login
def update_task(project_id,task_id):
    """
        There is no out-of-the-box query command to update in the Flask-SqlAlchemy Orm,
        check to see if task exist, delete it and commit the new content with same ID
    """
    data = request.get_json()
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }

    else:
        permission = has_project_permission(project, g.user)
        old_task = Task.query.filter_by(id=task_id)
        if not old_task:
                abort(404, f'There is no task with ID of {task_id}.')

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

@mod.delete('/project/<int:project_id>/task/<int:task_id>/delete/')
@requires_api_login
def delete_task(project_id, task_id):
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    else:
        permission = has_project_permission(project, g.user)
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            abort(404, f'There is no task with ID of {task_id}.')
        if task:
            db_session.delete(task)
            db_session.commit()
            return {
                'success': True,
                'result': tasks_schema.dump(g.user.tasks),
                'message': "Task Deleted Successfully.",
            }
    permission = has_project_permission(project, g.user)
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        abort(404, f'There is no task with ID of {task_id}.')
    if task:
        db_session.delete(task)
        db_session.commit()
        return {
            'success': True,
            'result': tasks_schema.dump(g.user.tasks),
            'message': "Task Deleted Successfully.",
        }



@mod.put('/project/<int:project_id>/task/<int:task_id>/completion-status/')
@requires_api_login
def update_task_status(project_id, task_id):
    """
        User with permissions can replace completion status of task if it exists and is part of the project
    """
    completion_status = request.get_json()['completion_status']

    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }
    
    else:
        permission = has_project_permission(project, g.user)
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            abort(404, f'There is no task with ID of {task_id}.')
        if task:
            task.completion_status = completion_status
            db_session.add(task)
            db_session.commit()
            return {
                'success': True,
                'result': task_schema.dump(task),
                'message': f"Successfully Updated the Completion Status of {task.name}."
            }

@mod.put('/project/<int:project_id>/task/<int:task_id>/<deadline_date>')
@requires_api_login
def update_task_deadline(project_id, task_id, deadline_date):
    """
        User with permissions can edit timelines of tasks
    """
    deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d").date() # there is no out-of-box support for dates in url routing
    project = Project.query.filter_by(id=project_id).first()
    if not project:
        return {
            'success': False,
            'message': f"No project with the specified id {project_id} found.",
        }

    else:
        permission = has_project_permission(project, g.user)
        task = Task.query.filter_by(id = task_id).first()
        if not task:
            abort(404, f'There is no task with ID of {task_id}.')
        
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
        'is_project_manager': g.user.id == project.manager_id

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


""" 
from werkzeug.routing import BaseConverter, ValidationError

class DateConverter(BaseConverter):
    #Extracts a ISO8601 date from the path and validates it.
    #Custom converter for dates in urls since there is no out-of-the-box support for dates in routes
    #Use later if lines in update_deadline routes for task and project not working

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError()
 
    def to_url(self, value):
        return value.strftime('%Y-%m-%d')


app.url_map.converters['date'] = DateConverter #allows <date:deadline_date>
 """