# BlumCryptoBot

BlumCryptoBot is a Telegram bot that helps you automate tasks on the Blum platform. It’s built with Python and uses the Pyrogram library.

## Features

### Main Features

- **Farming Management**: Automatically start farming tasks and claim rewards.

### Currently Paused Features

- **Play and Claim Game Rewards**: This feature is currently paused and not available for use.

## Setup Instructions

### Install `uv`

Before setting up the bot, you need to install `uv`. You can do this globally using pip. Run the following command in your terminal:

    pip install uv

### Using `uv`

1.  **Clone the Repository**: Open your terminal and run:

    ```
    clone <repository-url>
    cd <repository-directory>
    ```

2.  **Sync the Environment**: Run the following command to set up the environment with Python 3.10.2:

    ```
    uv sync --python 3.10.2

    ```

3.  **Create a `.env` File**: In the project folder, create a file named `.env` and add the following lines:

    ```
    SESSION_NAME=<your_session_name>
    API_ID=<your_api_id>
    API_HASH=<your_api_hash>
    REF_ID=<your_referral_id>
    ```

    - **`SESSION_NAME`**: Choose any name you like for your session. This helps the bot remember your login details. You could use something like your Telegram username.
    - **`API_ID`**: Get your `API_ID` from [my.telegram.org/auth?to=apps](https://my.telegram.org/auth?to=apps). Log in and create a new application. Your `API_ID` will be displayed after creation.
    - **`API_HASH`**: This will be shown alongside your `API_ID` after creating your application.
    - **`REF_ID`**: This is your referral ID. Generate it by visiting the Blum app and looking for your referral link. It will look like this:
      vbnet
      Copy code
      `https://t.me/blum/app?startapp=ref_pMt7QOvG1e`
      The `REF_ID` is the part after `startapp=`, so in this case, it's `ref_pMt7QOvG1e`.

4.  **Run the Bot**: Finally, start the bot by running:

    ```
    uv run main.py
    ```

### Alternative Setup Using `pip`

If you prefer using `pip` instead of `uv`, follow these steps:

1.  **Clone the Repository**:

    ```
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a Virtual Environment**:

    ```
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:

    - **Windows**:
      ```
      venv\Scripts\activate
      ```
    - **macOS/Linux**:

      ```
      source venv/bin/activate`
      ```

4.  **Install the Required Packages**:

    ```
    pip install -r requirements.txt
    ```

5.  **Create a `.env` File**: (same as above)
6.  **Run the Bot**:

    ```
    python main.py
    ```

## Why Use `uv`?

Using `uv` makes it easier to manage Python environments. It’s faster and simpler than traditional virtual environments. Here are some benefits:

- **Simplicity**: Easy setup for new projects.
- **Performance**: Quicker dependency management.
- **Consistency**: Helps avoid environment issues across different machines.

## Usage

- After running the bot, it will log in with your Telegram account and start managing your farming tasks.
- Check the logs to see the bot’s actions and any errors.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Let me know if there are any other changes you'd like!
