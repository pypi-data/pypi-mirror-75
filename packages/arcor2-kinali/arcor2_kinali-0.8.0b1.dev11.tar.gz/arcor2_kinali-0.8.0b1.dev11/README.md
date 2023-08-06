
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
Use docker exec to attach to arserver container and run following scripts and restart arserver.
```bash
/root/arcor2_kinali/arcor2_kinali/services/upload.py
/root/arcor2_kinali/arcor2_kinali/object_types/upload.py
```


## Installation (for development without docker):
```bash
pip3 install -e arcor2_kinali
```

## Releasing a new version
 TBA
