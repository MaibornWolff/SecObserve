*This library has been copied from https://github.com/kHRISl33t/runtime-env-cra and the patch from https://github.com/kHRISl33t/runtime-env-cra/pull/11 has been applied.*

# Runtime-env-cra

A runtime environment handler for React.js apps that have been bootstraped using [create-react-app](https://github.com/facebook/create-react-app).

- [Usage](#usage)
- [Requirements](#requirements)
- [CLI Options](#cli-options)
- [Using in a Typescript app](#typescript-usage)
- [Usage in Docker](#usage-in-docker)
- [Examples](#examples)
- [Test Coverage](#test-coverage)
- [Contributors](#contributors)

## Usage

The `runtime-env-cra` package was meant to be used in Docker or VM based environments, where you have full control over how your application will start. Sadly, `runtime-env-cra` can not be used if you are using S3 or another static file serving solution.

- Supported node.js versions due to `yargs` is 12 or greater

- Installation

```sh
$ npm install runtime-env-cra
```

- Add the following to `public/index.html` inside the `<head>` tag:

```html
<!-- Runtime environment variables -->
<script src="%PUBLIC_URL%/runtime-env.js"></script>
```

- Modify your `start` script to the following in your `package.json`:

```json
...
"scripts": {
  "start": "NODE_ENV=development runtime-env-cra --config-name=./public/runtime-env.js && react-scripts start",
  ...
}
...
```

- If you are on windows, you need to use [cross-env](https://github.com/kentcdodds/cross-env)

```json
"scripts": {
  "start": "cross-env NODE_ENV=development runtime-env-cra --config-name=./public/runtime-env.js && react-scripts start",
  ...
}
```

The script parses everything based on your `.env` file and adds it to `window.__RUNTIME_CONFIG__`.
If you pass `NODE_ENV=development` for the script, it will use the values from your `.env`, but if you provide anything else than `development` or nothing for `NODE_ENV` it will parse environment variables from `process.env`. This way you can dynamically set your environment variables in production/staging environments without the need to rebuild your project.

## Requirements

This script uses your `.env` file by default to parse the environment variables to `window.__RUNTIME_CONFIG__`, so be sure to have one in your project! After modifying the `start` script and `public/index.html` described in the section above, you should be good to go!

## CLI options

- Display the help section.

```sh
$ runtime-env-cra --help | -h
```

- Relative path and file name that will be generated. Default is `./runtime-env.js`

```sh
$ runtime-env-cra --config-name | -cn
```

- Relative path and name of your `env` file. Default is `./.env`

```sh
$ runtime-env-cra --env-file | -ef
```

## Typescript usage

- Create `./src/types/globals.ts` file and pase the following (**modify the `__RUNTIME_CONFIG__` properties to match your environment**):

```typescript
export {};

declare global {
  interface Window {
    __RUNTIME_CONFIG__: {
      API_URL: string;
      NODE_ENV: string;
    };
  }
}
```

- Add `"include": ["src/types"]` to your `tsconfig.json`.

```json
{
  "compilerOptions": { ... },
  "include": ["src/types"]
}
```

## Usage in Docker

You must have an example of your `env` layout. A project usually have a `.env.example` which represents that and will not contain any sensitive information.
Inside a docker container we can lean on the `.env.example`. **Make sure your `.env.example` is always up to date!**

- Using in an alpine based container

```Dockerfile
# copy .env.example as .env to the container
COPY .env.example .env

# install nodejs & npm
RUN apk add --update nodejs
RUN apk add --update npm

# install runtime-env-cra package
RUN npm i -g runtime-env-cra

# start the app with the following CMD
CMD ["/bin/sh", "-c", "runtime-env-cra && nginx -g \"daemon off;\""]
```

## Examples

- Create react app with typescript template, including Dockerfile and docker-compose. ([source](/examples/runtime-env-example-ts))
- Create react app without typescript, including Dockerfile and docker-compose. ([source](/examples/runtime-env-example-js))

## Test coverage

```bash
-------------------|---------|----------|---------|---------|-------------------
File               | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
-------------------|---------|----------|---------|---------|-------------------
All files          |     100 |      100 |     100 |     100 |
 generateConfig.js |     100 |      100 |     100 |     100 |
 utils.js          |     100 |      100 |     100 |     100 |
-------------------|---------|----------|---------|---------|-------------------
Test Suites: 1 passed, 1 total
Tests:       5 passed, 5 total
Snapshots:   0 total
Time:        1.751 s
```

## Contributors

<table>
  <tr>
    <td align="center"><a href="https://github.com/kHRISl33t"><img src="https://avatars.githubusercontent.com/u/30027430?v=4" width="50px;" alt=""/><br /><sub><b>kHRISl33t</b></sub></a><br />
    <td align="center"><a href="https://github.com/peteyycz"><img src="https://avatars1.githubusercontent.com/u/7130689?v=4" width="50px;" alt=""/><br /><sub><b>peteyycz</b></sub></a><br />
    <td align="center"><a href="https://github.com/seanblonien"><img src="https://avatars.githubusercontent.com/u/33133478?v=4" width="50px;" alt=""/><br /><sub><b>seanblonien</b></sub></a><br />
  </tr>
</table>

**_If you find a bug or have a question about the usage, feel free to open an issue!_**
