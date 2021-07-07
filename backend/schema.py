from backend import ma

class ProjectSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'manager_id', 'contributors')

# Init Schema

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)