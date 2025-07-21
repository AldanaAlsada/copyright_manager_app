"""
this file is for all the functions for artefact
upload_file, view_file, delete_file and rename
"""

import sqlite3
from pathlib import Path
import os
from app.encryption_decryption import encrypt_data, decrypt_data
from app.checksum import create_checksum
from app.timestamp import timestamp_current_today
from datetime import datetime

database_filepath = Path("database/artefact.db")
storefile_path = Path("artefacts_storage/")

class ArtefactManagerClass:
    """this class is for CRUD operations also I did encryption and rolebased in the same class."""

    def __init__(self, user):
        """This is for the user which logs in."""
        self.user = user

    def upload_file(self):
        """this function is for upload_file, I put mp3 and pdf and txt as well"""
        allowed_filetypes = {'.txt', '.pdf', '.mp3'}
        file_path = input("Enter the file path: ").strip() #remove any spaces
        path = Path(file_path)

        if not path.exists(): #if file not found
            print("The file path is not correct, check again.")
            return
        if path.suffix.lower() not in allowed_filetypes: #file extensions not allowed
            print(f"File type is invalid - allowed types are: {allowed_filetypes}")
            return
        if path.stat().st_size > 5 * 1024 * 1024: #file size not allowed
            print("File is big the allowed size maximum is 5MB.")
            return

        with open(path, "rb") as artefact:# read file
            artefact_content = artefact.read()

        artefact_title = input("Enter title for the artefact: ")
        artefact_identifier = f"{self.user['username']}_{artefact_title.replace(' ', '_')}" # for the ID I replace space with _
        encrypted_artefact = encrypt_data(artefact_content) # encryption w3school
        artefact_checksum = create_checksum(artefact_content) #checksum w3school
        artefact_timestamp = timestamp_current_today() #timestamp w3school

        encrypted_file_path = storefile_path / f"{artefact_identifier}{path.suffix}.enc" #create artefacts_storage path and add enc
        with open(encrypted_file_path, "wb") as artefactfile: #write encrypted file
            artefactfile.write(encrypted_artefact)

        with sqlite3.connect(database_filepath) as db_connection: #connection to db
            connection_cursor = db_connection.cursor()
            connection_cursor.execute(
                "INSERT INTO artefacts (title, owner_id, filename, checksum, timestamp) VALUES (?, ?, ?, ?, ?)",
                (artefact_title, self.user['id'], str(encrypted_file_path), artefact_checksum, artefact_timestamp)
            )
            db_connection.commit()

        print("Artefact uploaded and encrypted.")

    def view_file(self):
        """
        view_file , in this function admins can see everything and modify everything
        normal users can view_file all but modify only their files
        """
        with sqlite3.connect(database_filepath) as db_connection: #connection
            db_connection.row_factory = sqlite3.Row
            connection_cursor = db_connection.cursor()
            # join the query to get the username from user table
            connection_cursor.execute("""
                SELECT art.*, usr.username AS owner_name, usr.role AS owner_role
                FROM artefacts art
                JOIN users usr ON art.owner_id = usr.id
            """)
            results = connection_cursor.fetchall()

            #display the information for all artefacts
            for art in results:
                ownership = "Owned by you" if art['owner_id'] == self.user['id'] else "Read-only Access"
                print(f"ID = {art['id']} ({ownership})")
                print(f"Title = {art['title']}")
                print(f"Owner = {art['owner_name']} ({art['owner_role']})")
                print(f"Filename = {art['filename']}")
                print(f"Checksum = {art['checksum']}")
                print(f"Timestamp = {art['timestamp']}")
                try:
                    with open(art['filename'], "rb") as encrypted_file:
                        decrypted_file = decrypt_data(encrypted_file.read()) #decrypt database
                        print("Artefact Preview:", decrypted_file[:100].decode(errors='ignore'))
                except Exception as e:
                    print("Failed to decrypt:", e)
                print("-" * 40)

    def update_file(self):
        """
       This function will let user rename the title, but user can only rename their own.
        """
        artefact_id = input("Enter ID of the artefact to rename: ").strip()
        new_artefact_title = input("Enter new title: ").strip()

        with sqlite3.connect(database_filepath) as db_connection:
            connection_cursor = db_connection.cursor()

            # this query will check who is the owner of the file
            connection_cursor.execute("SELECT owner_id FROM artefacts WHERE id = ?", (artefact_id,))
            results = connection_cursor.fetchone()

            if not results:
                print("Artefact not found.")
                return

            artefact_owner = results[0] #if the user is different user and you are not admin then error
            if self.user['role'] != 'admin' and artefact_owner != self.user['id']:
                print("Your access is only readonly you can't modify it.")
                return

            # if everything is ok then update_file the title
            connection_cursor.execute("UPDATE artefacts SET title = ? WHERE id = ?", (new_artefact_title, artefact_id))
            db_connection.commit()
            print("Title updated successfully.")
    def delete_file(self):
        """only admins can delete_file"""
      #  if self.user['role'] != 'admin':
       #     print("This functionality is only restricted to admins.")
        #    return
        # user should only be able to delete their own files

        file_id = input("Enter the ID for the file you want to delete: ").strip()

        with sqlite3.connect(database_filepath) as db_connection:
            connection_cursor = db_connection.cursor()
            connection_cursor.execute("SELECT filename FROM artefacts WHERE id = ?", (file_id,))
            result = connection_cursor.fetchone()

            if result:
                connection_cursor.execute("SELECT owner_id FROM artefacts WHERE id = ?", (file_id,))
                results = connection_cursor.fetchone()
                artefact_owner = results[0]
                if self.user['role'] != 'admin' and artefact_owner != self.user['id']:
                    print("Your access is only readonly you can't modify it.")
                    return
                file_path = result[0]

                try:
                    os.remove(file_path)
                    print("The file has been deleted successfully.")
                except OSError:
                    print("File doesn't exist anymore or the wrong ID entered.")

                connection_cursor.execute("DELETE FROM artefacts WHERE id = ?", (file_id,))
                db_connection.commit()
                print("The file has been deleted from database successfully.")

                # log the username in the log file
                entry_for_log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Logged in user is: {self.user['username'] } - File ID is: {file_id}\n"
                with open("logs/deletion_logs.txt", "a", encoding="utf-8") as f:
                    f.write(entry_for_log)

            else:
                print("The ID is incorrect.")