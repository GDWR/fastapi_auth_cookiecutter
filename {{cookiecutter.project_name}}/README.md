# {{cookiecutter.project_name}}

Requirements:
- Docker
- DockerCompose

## Running the project

### Create a Environment file
Duplicate the `template.env` as `.env`. 
```shell
cp template.env .env
```

#### Development
```shell
docker-compose -f dev.docker-compose.yml up
```


#### Production
```shell
docker-compose up --detach
```
