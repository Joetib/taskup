from backend.database import Project, Task, User
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


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description')
        include_fk = True
    created_by = ma.Nested(UserSchema)


class ProjectSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Project
        #fields = ('id', 'name', 'manager_id', )
        include_fk = True
    contributors = ma.List(ma.Nested(UserSchema))
    manager = ma.Nested(UserSchema)
    tasks = ma.List(ma.Nested(TaskSchema))


# Init project schema
project_schema = ProjectSchema(strict=True)
projects_schema = ProjectSchema(strict=True, many=True)

# Init task schema
task_schema = TaskSchema(strict=True)
tasks_schema = TaskSchema(strict=True, many=True)