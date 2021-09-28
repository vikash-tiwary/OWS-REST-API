# Swagger
## What is Swagger?
[Swagger](https://swagger.io/) The goal of Swagger is to define a standard, language-agnostic interface to REST APIs which allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection. 
When properly defined via Swagger, a consumer can understand and interact with the remote service with a minimal amount of implementation logic. Use Swagger to describe: 
- Routes
- Parameters
- Example responses
- Header, query parameter, and post body validation schemas.
- [And much more ...](https://swagger.io/specification/)

## Why use Swagger?

When we have several developers working on a microservice, Swagger can help us agree on the API contract before development even begins. Doing this, we also unblock the consumer application (generally frontend code, but possibly another microservice) from waiting until the microservice is complete.

- It's a structured language instead of markdown or other open document format
- It's machine parse-able (more on that below)
- It acts as a contract between developers

## How can I write Swagger?

Swagger can be written in JSON, YAML or most any language, we are not linting or compiling Swagger in any way. This can lead to some messiness but we have some tools we can use.

#### Swagger Tools
A wide array of tools can be found for editing and viewing swagger specs [here](https://swagger.io/tools/).

#### Installing Swagger Web editor locally
The Swagger web editor can be installed from source on GitHub:
https://github.com/swagger-api/swagger-editor

More about how to install the web editor locally can be found here:
https://swagger.io/docs/swagger-tools/#swagger-editor-documentation-0