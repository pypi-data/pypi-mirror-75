# nose2rt - nose2 data collector for Testgr

Plugin sends nose2 data to Testgr server.

### Setup

```pip install nose2rt```

Find your nose2 config file and configure as described below.

Example:

```
[unittest]
plugins = nose2rt.rt

[rt]
endpoint = http://127.0.0.1/loader  # Your Testgr service URL
show_errors = True # show POST errors

[test-result]
always-on = True
descriptions = True

```
### Launch
```
nose2 --rt -> will launch nose2 with nose2rt plugin.
```

Additional parameters: 

* --rte "your_environment" -> will launch nose2 and send your environment name as additional info to the Testgr server. 
* --rt-job-report - will send email after job finish.
* --rt-custom-data - will send any custom data to Testgr in Dict format. Example:
```
--rt-custom data='{"Git":"dev-branch"}'
```

## Authors

[**Andrey Smirnov**](https://github.com/and-sm)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details


