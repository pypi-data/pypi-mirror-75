# WEB plugin for ExtensiveAutomation server

This plugin enable to interact with remote web server through the HTTP protocol.
This plugin is based on the `curl` command.

## Table of contents
* [Installing from pypi](#installing-from-pypi)
* [Installing from source](#installing-from-source)
* [About actions](#about-actions)
    * [http/curl.yml](#httpcurlyml)
* [About workflows](#about-workflows)
    * [http/httpbin.yml](#httphttpbinyml)
    * [http/jsonplaceholder.yml](#httpjsonplaceholderyml)
    
## Installing from pypi

1. Run the following command

        pip install extensiveautomation_plugin_web

2. Execute the following command to take in account this new plugin

        ./extensiveautomation --reload
        
3. Samples are deployed on data storage
   
## Installing from source

1. Clone the following repository 

        git clone https://github.com/ExtensiveAutomation/extensiveautomation-plugin-web.git
        cd extensiveautomation-plugin-web/src/ea/
        
2. Copy the folder `sutadapters` in the source code server and overwrite-it

        cp -rf sutadapters/ /<install_path_project>/src/ea/
        
3. Copy the folder `var` in the source code server and overwrite-it

        cp -rf var/ /<install_path_project>/src/ea/
        
4. Finally execute the following command to install depandencies

        cd /<install_path_project>/src/
        python3 extensiveautomation.py --install-adapter WEB
        python3 extensiveautomation.py --reload

## About actions

### http/curl.yml

Send http requests and analysing responses.

Parameter(s):
- agent (text): agent name

- curl-body (text): http request body

- curl-headers (text): additional headers for the request

- curl-hosts (text): remote address

- curl-proxy (text): proxy url 

- curl-method (text): http method

- curl-options (text): additional options for curl

- response-body-json (dict): expected json in http response with jsonpath expression

- response-body-text (text): expected string in http response

- response-body-xml (text): expected xml in http response with xpath expression

- response-body-xmlns (text): namespaces 

- response-code (integer): reponse code expected

- response-headers (text): list of expected headers in response

- response-phrase (text): response phrase expected

- response-version (text): http version expected in response

## About workflows

### http/httpbin.yml

This worflow show how to use the `curl` action and 
how to extract value from json response.

1. Reuse curl action

```yaml
- description: Get my origin IP
  file: Common:actions/http/curl.yml
```

2. Configure parameters

```yaml
- name: curl-hosts
 value: https://httpbin.org/ip
- name: response-body-json
 value: |
    origin -> [!CAPTURE:externalip:]
```

### http/jsonplaceholder.yml

This worflow show how to use the `curl` action and POST json data.

```yaml
- name: curl-hosts
 value: https://jsonplaceholder.typicode.com/posts
- name: curl-method
 value: POST
- name: curl-headers
 value: |
    Content-Type: application/json
- name: curl-body
 value:
  title: un exemple en français
  body: bonjour
  userId: 1
```
