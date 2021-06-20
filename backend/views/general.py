from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from backend.utils import check_password, hash_password, requires_login
from backend.database import Project, db_session, User

mod = Blueprint('general', __name__)