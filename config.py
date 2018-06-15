import string
import random

port = 8080
release = 'stretch'
preseed = 'test'

machine_config = {
        'hostname': 'test',
        'username': 'janne',
        # Empty passwords are not allowed
        'password': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(50)),
        'ssh_key': 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM35Bq87SBWrEcoDqrZFOXyAmV/PJrSSu3hl3TdVvo4C janne'
}
