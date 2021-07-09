# Mock API for Testing

## Background
In order to test data prior to integration, it is useful to be able to make actual API calls to test call functionality in flutter/dart. Additionally, it is useful to be able to use properly formatted data which will look the same as it will when integration happens later on with other modules. In order to simulate that behavior, you can use a "mock JSON API" to make calls and return proper data.

## Setup 
- Install JSON-Server NPM Package with command: `npm install -g json-server`
- Create a `db.json` file with some mock data
    - Example data can be found in the `db.json` in this directory
- Start JSON Server with command: `json-server --watch db.json`
- View server data at localhost:3000

## Resources
[Link to JSON-Server Github Repo](https://github.com/typicode/json-server)
[Link to Web-Based version of JSON-Server](https://my-json-server.typicode.com/)
[Link to Web-Based version of JSON-Server with data already provided](https://jsonplaceholder.typicode.com/)