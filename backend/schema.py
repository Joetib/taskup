from backend.database import Project, Task, User, Message
from backend import ma

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')
class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        #fields = ('id', 'name', 'manager_id', )
        include_fk = True
    contributors = ma.List(ma.Nested(UserSchema))
    manager = ma.Nested(UserSchema)

# Init Schema

class ProjectListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        #fields = ('id', 'name', 'manager_id', )
        include_fk = True
    contributors = ma.List(ma.Nested(UserSchema))
    manager = ma.Nested(UserSchema)

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
    created_by = ma.Nested(UserSchema)

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        include_fk = True
    created_by = ma.Nested(UserSchema)

class TaskDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
    created_by = ma.Nested(UserSchema)
    project = ma.Nested(ProjectListSchema)
    messages = ma.List(ma.Nested(MessageSchema))

task_schema = TaskSchema()

class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        #fields = ('id', 'name', 'manager_id', )
        include_fk = True
    contributors = ma.List(ma.Nested(UserSchema))
    manager = ma.Nested(UserSchema)
    tasks = ma.List(ma.Nested(TaskSchema))

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
