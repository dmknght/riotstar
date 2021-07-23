import docker
import cores


class DockerImage(object):
    # Status:
    # 0. Running
    # 1. Not running
    # 2. Not installed
    def __init__(self, name, description, link):
        self.name = name
        self.description = description
        self.link = link
        self.status = 2


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
        result = []
        for image in cores.lab_images:
            image_object = DockerImage(
                name=image[0],
                description=image[1],
                link=image[2],
            )
            try:
                if self.client.images.get(image_object.link):
                    # TODO check if it is running
                    image_object.status = 1
            except docker.errors.ImageNotFound:
                image_object.status = 2

            result.append(image_object)
        return result
