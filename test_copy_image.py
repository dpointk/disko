import getpass
import docker
from src.disko.image_management.image_controller import *
from src.disko.image_collector import *
from src.disko.sqlite import *
docker_client = docker.from_env()

# Create db from cluster
create_db = ImageCollector().collect_images("kind-cluster1")

# Import sqlite.py to use any function on my db file
sql = SQLiteCRUD("image_data.db")

# Import image_controller.py to use any function on my db file
ctl1 = ImageController("image_data.db")

# images = sql.select_all("kind-cluster1")
images = ["docker.io/kindest/local-path-provisioner:v0.0.22-kind.0"]

password = getpass.getpass("Enter your Password: ")
ctl1.copy_images(images, "ygalidan/test1", "v0.0.22-kind.0", "ygalidan", password)

docker_client.login("ygalidan", password)
pull = docker_client.images.pull("ygalidan/test1", "v0.0.22-kind.0")

assert pull is not None, "Success"

