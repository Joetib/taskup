# Api Documentation

- `/auth/login/`  api_login
    
    Requirements:
    * email
    * password

    returns
    * success
    * message
    * name
    * email
    * token
----
- `/auth/signup` Create a new user
    
    methods allowed:
    * POST

    requirements:
    * name
    * email
    * password

    returns:
    * success
    * message
    * token
    * name
    * email
    * id
----
- `/auth/users/` Gets all users

    methods allowed:
    * GET

    returns:
    * success
    * message
    * results
------

- `/project/` create a project or get a list of projects related to the current user

    requires authentication

    methods allowed:
    * GET
    * POST

    requirements:
    * name
    * description
    * deadline_date

    returns
    * success
    * message
    * new_project [`Post only`] : The project that was just created
    * result : A query of all projects
---

- `/project/<int:project_id>/` Get project details

    methods allowed:
    * POST

    returns:
    * success
    * result
    * message
----
- `/project/<int:project_id>/add-contributor/`
    
    requires login

    methods allowed:
    * post

    returns:
    * success
    * result
    * message
    
---
- `/project/<int:project_id>/delete/`

   requires login

   methods allowed:
   * delete

   returns:
   * success
   * message
   * result
---

- `/invitation/<int:invitation_id>/decline/`

    requires login

    methods allowed:
    * get

    returns:
    * success
    * result
    * message

---

- `/invitation/<int:invitation_id>/accept/`

   requires login

   method allowed
   * get

   returns
   * success
   * result
   * message

---
- `/project/<int:project_id>/<string:completion_status>`

   requires login

   methods allowed:
   * put

   returns:
   * success
   * message
   * result
---
- `/project/<int:project_id>/<deadline_date>`

   requires login

   methods allowed:
   * put

   returns:
   * success
   * message
   * result
---
- `/project/<int:project_id>/task/`

   requires login

   methods allowed:
   * post

    returns:
   * success
   * message
   * result
---

- `/project/<int:project_id>/task/`

    requires login

   methods allowed:
   * get

    returns:
   * success
   * message
   * result
---

- `/project/<int:project_id>/task/<int:task_id>`

    requires login

   methods allowed:
   * put

   returns:
   * success
   * message
   * result
---

- `/project/<int:project_id>/task/<int:task_id>/delete/`

   requires login
   
   methods allowed:
   * delete

   returns:
   * success
   * message
   * result
---

- `/project/<int:project_id>/task/<int:task_id>/<string:completion_status>`

    requires login
   
   methods allowed:
   * put

   returns:
   * success
   * message
   * result
---

- `/project/<int:project_id>/task/<int:task_id>/<deadline_date>`

   requires login

   meethods allowed:
   * put

   returns:
   * success
   * message
   * result
---

- `/project/<int:project_id>/task/<int:task_id>/`

   requires login

   meethods allowed:
   * get

   returns:
   * success
   * message
   * result
---

- `/project/<int:project_id>/task/<int:task_id>/message/`

   requires login

   meethods allowed:
   * post

   returns:
   * success
   * message
   * result
---


    










   
   


    

