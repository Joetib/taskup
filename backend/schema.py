from backend.database import Project, User
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

# Init Schema

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)