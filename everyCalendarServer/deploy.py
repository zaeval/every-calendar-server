import paramiko
import os

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect('52.78.156.205', username='ubuntu',
               key_filename='/Users/hongseung-ui/Desktop/amongsoftware.pem')


def mkdir_p(sftp, remote_directory):
    """Change to this directory, recursively making new folders if needed.
    Returns True if any folders were created."""
    if remote_directory == '/':
        # absolute path so change directory to root
        sftp.chdir('/')
        return
    if remote_directory == '':
        # top-level relative directory must exist
        return
    try:
        sftp.chdir(remote_directory)  # sub-directory exists
    except IOError:
        dirname, basename = os.path.split(remote_directory.rstrip('/'))
        mkdir_p(sftp, dirname)  # make parent directories
        sftp.mkdir(basename)  # sub-directory missing, so created it
        sftp.chdir(basename)
        return True

def recursive(sftp,path,remote_path):
    for root, directories, filenames in os.walk(path):
        current_path = os.path.join(remote_path,root.split(path)[1])
        for directory in directories:
            mkdir_p(sftp,os.path.join(current_path,directory))

        for filename in filenames:
            print(os.path.join(current_path, filename))
            try:
                sftp.put(os.path.join(root,filename),os.path.join(current_path, filename))
            except Exception as e:
                print(e)

sftp = client.open_sftp()

recursive(sftp,'/Users/hongseung-ui/every-calendar/server/every-calendar-server/everyCalendarServer/','/home/ubuntu/every-calendar-server/everyCalendarServer')
client.exec_command(
    'sudo service apache2 restart'
)
sftp.close()