# opendns-updater

A docker based serivce that connects to and updates OpenDNS dynamic DNS service with the latest IP address obtained `ipify`.


## Starting the container

```bash
$ docker run --env username=foo --env token=1234 --env delay=500 birudagmawi/opendns-updater
```


## Environment variables
- `username` and `token` are required environment variables and are obtained from your OpenDNS configuration. 
- `delay` is an optional variable to denote the amount of delay, in seconds, to wait before each attempt to check and update the current IP adddress on OpenDNS


