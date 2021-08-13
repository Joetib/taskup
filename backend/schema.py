from backend.database import Invitation, Project, Task, User, Message
from backend import ma


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')



class ProjectListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        #fields = ('id', 'name', 'manager_id', )
        include_fk = True
    contributors = ma.List(ma.Nested(UserSchema))
    manager = ma.Nested(UserSchema)


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        include_fk = True
    created_by = ma.Nested(UserSchema)

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'completion_status', 'created_by', 'project_id')
        include_fk = True
    created_by = ma.Nested(UserSchema)

class InvitationListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invitation
        include_fk = True
    user = ma.Nested(UserSchema)

class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        #fields = ('id', 'name', 'manager_id', )
        include_fk = True
    contributors = ma.List(ma.Nested(UserSchema))
    manager = ma.Nested(UserSchema)
    tasks = ma.List(ma.Nested(TaskSchema))
    invites = ma.List(ma.Nested(InvitationListSchema))


class TaskDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
    created_by = ma.Nested(UserSchema)
    project = ma.Nested(ProjectListSchema)
    messages = ma.List(ma.Nested(MessageSchema))

class InvitationDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invitation
        include_fk = True
    project = ma.Nested(ProjectListSchema)
    user = ma.Nested(UserSchema)

# Init project schema
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

# Init task schema
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


# Yet to initialize some schemas