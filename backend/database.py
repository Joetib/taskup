
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, \
     ForeignKey, event, Table
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base

import jwt

from flask import url_for
from sqlalchemy.sql.expression import desc
from backend import app

engine = create_engine(app.config['DATABASE_URI'],
                       convert_unicode=True,
                       **app.config['DATABASE_CONNECT_OPTIONS'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))



Model = declarative_base(name='Model')
Model.query = db_session.query_property()


def init_db():
    Model.metadata.create_all(bind=engine)

def clean_db():
    Model.metadata.drop_all(bind=engine)

class User(Model):
    __tablename__ = 'user'
    id = Column('user_id', Integer, primary_key=True)
    email = Column('email', String(50), index=True, unique=True)
    name = Column(String(200))
    password = Column(String(500))
    managed_projects = relationship('Project',back_populates="manager")
    #assigned_tasks = relationship('Task',back_populates="assigned_user",)

    

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def to_json(self):
        return dict(name=self.name, email=self.email)

    @property
    def is_admin(self):
        return self.openid in app.config['ADMINS']

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=12),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
            
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms= ['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        

association_table = Table('association', Model.metadata,
    Column('project_id', Integer, ForeignKey('project.project_id')),
    Column('user_id', Integer, ForeignKey('user.user_id'))
)

class Project(Model):
    __tablename__ = 'project'
    id = Column('project_id', Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(400))
    manager_id = Column(Integer, ForeignKey('user.user_id'))
    manager = relationship('User', back_populates='managed_projects')
    #tasks = relationship('Task', back_populates='project')

    contributors = relationship("User",
                    secondary=lambda: association_table,
                    backref="projects")

    slug = Column(String(50))

    def __init__(self, name, description=''):
        self.name = name
        self.description = description

    def to_json(self):
        return dict(name=self.name, slug=self.slug)


    @property
    def url(self):
        return url_for('general.projects', slug=self.slug)




""" class Task(Model):
    __tablename__ = 'task'

    id = Column('task_id', Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(300))
    project_id = Column(Integer, ForeignKey('project.project_id'))
    project = relationship(Project, back_populates="tasks")
    created_by_id = Column(Integer, ForeignKey('user.user_id'))
    created_by=relationship(User, back_populates="created_tasks", foreign_keys=created_by_id)
    assigned_user_id=Column(Integer, ForeignKey('user.user_id'), )
    assigned_user=relationship(User, back_populates="assigned_tasks", foreign_keys=assigned_user_id)
 """