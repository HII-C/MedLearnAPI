To build container:
    `docker build --build-arg DB_PASSWORD="exampleP@ssw0rd" {user}/{docker_repository}:{tag}`

To push:
    `docker push {user}/{docker_repository}:{tag}`

To run:
    `docker run -d -p {host_port}:{image_port (default=5000)} {user}/{docker_repository}:{tag}`
