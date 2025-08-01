# Resources AI Chatbot Plugin

## Introduction

Beginners often struggle to take their first steps with Jenkins’ documentation and available resources. To address this challenge, this plugin integrates an **AI-powered assistant** directly into the Jenkins interface. It offers quick, intuitive support to users of all experience levels through a simple conversational UI.

The plugin is designed to reduce the learning curve for newcomers while also improving accessibility and productivity for experienced users.

This plugin was developed as part of a Google Summer of Code 2025 project.

## Getting started

To get up and running with the **AI Chatbot for Jenkins** plugin, this repository provides a set of `Makefile` targets that streamline key development flows such as running the data pipeline, launching the API, building the frontend, and executing tests.

If you're just getting started, the best way is to use the `Makefile` in the root directory. For example:

- Start the backend API server:
    ```bash
    make api
    ```

By default, the API will be available at `http://127.0.0.1:8000`. To check that everything is working as expected you can try creating a chat session by using the `/sessions` endpoint:
```bash
curl -X POST http://localhost:8000/api/chatbot/sessions
```

You should get returned the session id that have been created.

In case you encounter any issues in running make targets we suggest running:
```bash
make clean && make <desired_target>
```

For detailed instructions, deeper explanations of each target in the `Makefile`, please refer to [Doc README](docs/README.md).

> **Note:** For the necessary requirements you can check out the [setup-dedicated section](docs/setup.md).

## Developer Documentation

Development-related documentation can be found in the [`docs/`](docs/) directory.

## Contributing

Refer to our [contribution guidelines](https://github.com/jenkinsci/.github/blob/master/CONTRIBUTING.md)

## LICENSE

Licensed under MIT, see [LICENSE](LICENSE.md)

