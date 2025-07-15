## Setup Instructions

For the setup you can follow [Setup Guide](setup.md).

> **Note**:
> Please use **Python 3.11 or later**. Ensure your installation includes support for the `venv` module.

To set up the environment and run the scripts:

1. Navigate to the `chatbot-core` directory:
    ```bash
    cd chatbot-core
    ```

2. Create a Python virtual environment
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment
    - Linux/macOS
        ```bash
        source venv/bin/activate
        ```
    - Windows
        ```bash
        .\venv\Scripts\activate
        ```
4. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```
5. Set the `PYTHONPATH` to the current directory(`chatbot-core/`):
    ```bash
    export PYTHONPATH=$(pwd)
    ```
