import os
from app.AutoGit.data.config import REMOTE_URL, FOLDER_PATH
import subprocess

folder_command = f"cd /D {FOLDER_PATH}"
print(folder_command)


class AutoGit:

    @staticmethod
    def push():
        command_string = f"{folder_command} && git add -A"
        os.system(command_string)
        command_string = f'{folder_command} && git commit -m "AutoCommit"'
        os.system(command_string)
        command_string = f'{folder_command} && git push'
        output = subprocess.getoutput(command_string)
        if "git push --set-upstream origin master" in output:
            command_string = f'{folder_command} && git push --set-upstream origin master'
            os.system(command_string)

    @staticmethod
    def init():
        command_string = f'{folder_command} && git init'
        os.system(command_string)
        command_string = f'{folder_command} && git remote add origin {REMOTE_URL}'
        os.system(command_string)

    @staticmethod
    def clone():
        command_string = f'{folder_command} && git clone {REMOTE_URL}'
        os.system(command_string)

    @staticmethod
    def pull():

        split_folder_path = FOLDER_PATH.split("\\")
        split_folder_path.pop(-1)

        err = "detected dubious ownership in repository"
        command_string = f'{folder_command} && git pull'
        output = subprocess.getoutput(command_string)
        if err in output:
            re_folder_path = "\\".join(split_folder_path)
            new_folder_command = f"cd /D {re_folder_path}"

            command_string = f'{new_folder_command} && git clone {REMOTE_URL}'
            os.system(command_string)

