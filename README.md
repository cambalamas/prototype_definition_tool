<p align="center"> <img src="Src/Icons/logo.png" height="350" width="350"> </p>

	# See `TODO.md` file to knows project status ☕.

## WITH [Docker](https://www.docker.com/what-docker).

> ***INSIDE THE CLONED DIRECTORY ...***

```shell
# first, build the docker image. (Can take a long time)
docker build -t sncdtool .
```

```shell
# windows (Powershell, and Xming or similar will be needed).
xming -ac -multiwindow -clipboard    # This open x11 server.
docker run -it `
	-v "$((Get-Location).path):/app" `
	-e DISPLAY="$((Get-NetAdapter "vEthernet (DockerNAT)" | Get-NetIPAddress).IPAddress):0" `
	sncdtool python3 /Src/Main.py
```

```shell
# linux (just works).
docker run -it \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd):/app \
    -e DISPLAY=$DISPLAY \
    sncdtool python3 /Src/Main.py
```



## WITHOUT [Docker](https://www.docker.com/what-docker).


### Requeriments.
- ***python3***

- **i18n**
- `pip install python-i18n[YAML]`

- **lxml**
- `pip3 install lxml` *or*
- `apt-get install -y python3-lxml`

- **pyqt5**
- `pip3 install PyQt5` *or*
- `apt-get install -y python3-pyqt5`



### Run locally from source.

> ***With the requirements installed correctly ...***

```shell
python3 EGui.py
```

