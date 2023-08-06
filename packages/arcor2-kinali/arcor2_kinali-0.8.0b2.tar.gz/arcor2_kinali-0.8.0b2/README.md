
## Running in docker:

### Prerequisites:

 - docker
 - docker-compose


### Run system 
#### Windows

It is recommended to use explicit stable version of each image instead of latest (as latest is considered unstable).

```bash
cd docker
$env:ARCOR2_VERSION="latest"
$env:ARCOR2_BUILD_VERSION="latest"
$env:ARCOR2_EXECUTION_VERSION="latest"
docker-compose up
```

For persistent variables, use this:

```bash
[Environment]::SetEnvironmentVariable("ARCOR2_VERSION", "latest", "User")
[Environment]::SetEnvironmentVariable("ARCOR2_BUILD_VERSION", "latest", "User")
[Environment]::SetEnvironmentVariable("ARCOR2_EXECUTION_VERSION", "latest", "User")
```
Restart powershell or open new window.
```
cd docker
docker-compose up
```


#### Linux

It is recommended to use explicit stable version of each image instead of latest (as latest is considered unstable).

```bash
cd docker
export ARCOR2_VERSION=latest
export ARCOR2_BUILD_VERSION=latest
export ARCOR2_EXECUTION_VERSION=latest
sudo -E docker-compose up
```

## Uploading services and object_types to project service
Use arcor2_upload_kinali image to upload all object types in this package to project service:
```bash
sudo docker run --rm --network="NAME_OF_PROJECT_SERVICE_NETWORK" --env ARCOR2_PERSISTENT_STORAGE_URL="http://NAME_OF_PROJECT_SERVICE:11000" arcor2/arcor2_upload_kinali:VERSION
```
NAME_OF_PROJECT_SERVICE_NETWORK and NAME_OF_PROJECT_SERVICE are defined in used docker-compose.yml file.

## Installation (for development without docker):
```bash
pip3 install -e arcor2_kinali
```

## Releasing a new version
 TBA
