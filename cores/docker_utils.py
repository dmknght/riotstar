import docker
import cores


class DockerImage(object):
    # Status:
    # 0. Running
    # 1. Not running
    # 2. Not installed
    def __init__(self, name, description, image):
        self.name = name
        self.description = description
        self.repo = image
        self.status = 2
        self.id = ""
        self.ports = ""
        self.up_time = ""
        self.ip = ""


class DockerClient(object):
    def __init__(self):
        self.client = docker.from_env()

    def pull(self, name):
        self.client.pull(name)

    def start(self, name):
        pass

    def kill(self, name):
        pass

    def get_images_status(self):
        # for x in self.client.containers.list():
        #     print(x.image.attrs)
        result = []
        for image in cores.lab_images:
            image_object = DockerImage(
                name=image[0],
                description=image[1],
                image=image[2],
            )
            try:
                image_status = self.client.images.get(image_object.repo)
                if image_status:
                    # Use API to show status of current image dirrectly
                    # We use repo name as filterer
                    # Return value is a list of dict
                    # Dict value to check: State: is running or not
                    # Status: Up time
                    container_status = self.client.api.containers(filters={"ancestor": image_object.repo})
                    try:
                        if container_status[0]["State"] == "running":
                            image_object.status = 0
                            image_object.ports = " ".join([f"{x['PrivatePort']}/{x['Type']}" for x in container_status[0]["Ports"]])
                            image_object.id = container_status[0]["Id"][:12]
                            image_object.uptime = container_status[0]["Status"]
                            image_object.ip = container_status[0]["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
                        else:
                            image_object.status = 1
                    except IndexError:
                        image_object.status = 1

            except docker.errors.ImageNotFound:
                image_object.status = 2

            result.append(image_object)
        return result
