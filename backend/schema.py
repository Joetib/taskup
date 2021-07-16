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


class TaskDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
    created_by = ma.Nested(UserSchema)
    project = ma.Nested(ProjectListSchema)
    messages = ma.List(ma.Nested(MessageSchema))


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description')
        include_fk = True
    created_by = ma.Nested(UserSchema)


# Init project schema
project_schema = ProjectSchema(strict=True)
projects_schema = ProjectSchema(strict=True, many=True)

# Init task schema
task_schema = TaskSchema(strict=True)
tasks_schema = TaskSchema(strict=True, many=True)