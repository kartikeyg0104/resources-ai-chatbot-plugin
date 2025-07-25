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

- Build the frontend chatbot UI:
    ```bash
    make build-frontend
    ```

- Run the plugin:
    ```bash
    mvn hpi:run
    ```

For detailed instructions, deeper explanations of each component, please refer to [Doc README](docs/README.md).

## Developer Documentation

Development-related documentation can be found in the [`docs/`](docs/) directory.

## Contributing

Refer to our [contribution guidelines](https://github.com/jenkinsci/.github/blob/master/CONTRIBUTING.md)

## LICENSE

Licensed under MIT, see [LICENSE](LICENSE.md)

