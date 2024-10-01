from docker import DockerClient

from config import DOCKER_URL

docker_client = DockerClient(base_url=DOCKER_URL)
images, containers = docker_client.images, docker_client.containers

print(images.list(all=True))
print(containers.list(all=True))

# image = images.get()
# container = containers.get()
# print(container.attrs)

# container_python = client.containers.run(image_python, '/bin/bash', name='my_bash', detach=True, tty=True, stdin_open=True, stdout=True, stderr=True)



import time

from docker import DockerClient

from config import DOCKER_URL

docker_client = DockerClient(base_url=DOCKER_URL)
images, containers = docker_client.images, docker_client.containers

print(images.list(all=True))
print(containers.list(all=True))

container = containers.get('mygpu')
att = container.attach(stream=True)
print(att)
while True:
    line = next(att).decode()
    print(line, end='')
