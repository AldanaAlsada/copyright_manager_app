"""
This file is the main entry point of the project
developer: Aldana Alsada
"""

from app.auth import login_user
from app.artefact import ArtefactManagerClass

def main():
    """This the main method"""
    loggedin_user = login_user() #if logged in not user then return nothing
    if not loggedin_user:
        return
    artefact_manager_class_object = ArtefactManagerClass(loggedin_user) # create the object of the class
    while True:
        print("1. Upload artefact\n 2. View artefact\n 3. Delete artefact (admin)\n 4. Rename artefact title(update_file)\n 0. Exit the program")
        menu_option = input("Enter the number for your choice i.e. (1 or 2 or 3 or 4 or 0): ")
        if menu_option == '1':
            artefact_manager_class_object.upload_file()
        elif menu_option == '2':
            artefact_manager_class_object.view_file()
        elif menu_option == '3':
            artefact_manager_class_object.delete_file()
        elif menu_option == '4':
            artefact_manager_class_object.update_file()
        elif menu_option == '0':
            break

if __name__ == "__main__":
    main()
