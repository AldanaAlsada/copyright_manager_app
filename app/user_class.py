"""
this file deals with user name and role
"""

class user_class:
    """this class for a user with a role."""
    def __init__(self, user_name, user_role):
        self.username = user_name
        self.userrole = user_role

    def is_user_admin(self):
        """This function will be used to check if user is admin"""
        return self.userrole == "admin"
