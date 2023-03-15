# REST API

SecObserve is build with an API first approach, every functionality needed to use SecObserve is covered by the REST API.

## Authentication

#### JWT

[JWT](https://jwt.io) authentication is used by SecObserve's frontend.

|                                         |                                     |
|-----------------------------------------|-------------------------------------|
| **Endpoint**                            | `/api/authentication/authenticate/` |
| **Validity duration for regular users** | 7 days / 168 hours  ^1)^            |
| **Validity duration for superusers**    | 1 day / 24 hours  ^1)^              |
| **HTTP header**                         | `Authorization: JWT `*`token`*      |

 ^1)^ Values can be changed by the administrators.

#### API token

API tokens are used for other integration scenarios, e.g. to call the REST API from a CI/CD pipeline to import observations. An API token for a user can only been seen once, when it is created. Afterwards there is no way to see that API token again. If it is lost it needs to be revoked and a new one has to be created, as only one API token is allowed per user.

|                                  |                                         |
|----------------------------------|-----------------------------------------|
| **Endpoint to create API token** | `/api/authentication/create_api_token/` |
| **Endpoint to revoke API token** | `/api/authentication/revoke_api_token/` |
| **Validity**                     | Until revokation                        |
| **HTTP header**                  | `Authorization: APIToken `*`token`*     |

## Interactive API documentation

The full documentation of the REST API is available at `<BACKEND_URL>/api/oa3/swagger-ui`.
