# Telegram Image/GIF Generation Bot

This Telegram bot allows users to generate images and GIFs from text descriptions using a self-hosted Stable Diffusion Web UI (AUTOMATIC1111).

## Features
- Generate images from text prompts.
- Generate animated GIFs from text prompts.
- Integrates with a local Stable Diffusion instance for maximum content flexibility.
- Basic keyword filtering for prohibited content.

## Disclaimer
This bot uses a self-hosted Stable Diffusion model. While basic filters are implemented, you are solely responsible for the content you generate. Please use this bot responsibly and adhere to all applicable laws and ethical guidelines. Avoid generating illegal, harmful, or non-consensual content.




## Prerequisites

-   **Python 3.9+**
-   **pip** (Python package installer)
-   **Telegram Bot Token**: Obtain this from BotFather on Telegram. Search for `@BotFather` in Telegram, start a chat, and use the `/newbot` command to create a new bot. You will receive an API token.
-   **Stable Diffusion Web UI (AUTOMATIC1111)**: This bot requires a running instance of the AUTOMATIC1111 Stable Diffusion Web UI with the `--api` flag enabled. It is recommended to run this on a machine with a powerful GPU.




## Stable Diffusion AUTOMATIC1111 Web UI Setup (on Kali Linux)

This section provides instructions for setting up the AUTOMATIC1111 Stable Diffusion web UI on Kali Linux. This setup is crucial for generating images and GIFs with the Telegram bot.

**Prerequisites for Stable Diffusion:**
- Kali Linux installed (preferably with a GPU for faster generation).
- Basic familiarity with the Linux command line.
- `git` installed (`sudo apt install git`).
- `python3` and `python3-venv` installed (`sudo apt install python3 python3-venv`).

**Steps:**

1.  **Clone the AUTOMATIC1111 web UI repository:**
    ```bash
    cd /opt
    sudo git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
    sudo chown -R $USER:$USER stable-diffusion-webui
    cd stable-diffusion-webui
    ```

2.  **Download Stable Diffusion models:**
    You need to download Stable Diffusion model checkpoints. You can find various models on Hugging Face (e.g., `runwayml/stable-diffusion-v1-5`). Download the `.ckpt` or `.safetensors` files and place them in the `stable-diffusion-webui/models/Stable-diffusion/` directory.
    For example, to download `v1-5-pruned-emaonly.safetensors`:
    ```bash
    wget -c https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors -P models/Stable-diffusion/
    ```

3.  **Install dependencies and run the web UI:**
    The `webui.sh` script will set up a Python virtual environment and install all necessary dependencies. It will also download additional components like GFPGAN, CodeFormer, and Latent Diffusion models.
    ```bash
    ./webui.sh --api --listen
    ```
    -   `--api`: This flag enables the API, which is essential for our Telegram bot to interact with Stable Diffusion.
    -   `--listen`: This flag makes the web UI accessible from other devices on your network (if you need to access it from outside your Kali VM).

    The first run will take a considerable amount of time as it downloads all the necessary components. Once it's ready, you will see a local URL (e.g., `http://127.0.0.1:7860`) in your terminal. This is the address of your Stable Diffusion web UI.

4.  **Keep the web UI running:**
    For the Telegram bot to function, the Stable Diffusion web UI must be running. You can run it in a detached screen session or a separate terminal window.




## Telegram Bot Setup and Running

1.  **Install Python Dependencies:**
    Navigate to the bot's directory and install the required Python libraries:
    ```bash
    cd /path/to/telegram_image_bot
    pip install -r requirements.txt
    ```

2.  **Set Your Telegram Bot Token:**
    The bot requires your Telegram Bot Token. Set it as an environment variable:
    ```bash
    export TELEGRAM_BOT_TOKEN=\


3.  **Run the Bot:**
    ```bash
    python3 bot.py
    ```
    The bot will start polling for updates. Ensure your Stable Diffusion Web UI is running with the `--api` flag enabled.

## Content Responsibility and Safety Guidelines

This bot is designed to provide creative image and GIF generation. However, it is crucial to understand and adhere to the following:

-   **User Responsibility:** You are solely responsible for the content you generate using this bot. Ensure that all generated content complies with local laws, ethical standards, and Telegram's Terms of Service.
-   **Prohibited Content:** Do not use this bot to generate illegal, harmful, or non-consensual content, including but not limited to:
    -   Child sexual abuse material (CSAM)
    -   Hate speech or discriminatory content
    -   Content promoting violence or self-harm
    -   Non-consensual intimate imagery
    -   Content depicting illegal activities
-   **Stable Diffusion Safety Features:** Stable Diffusion models often include internal safety filters. While this bot implements basic keyword filtering, it is highly recommended to use models that have robust safety features enabled. Be aware that bypassing these features may lead to the generation of unintended or harmful content.
-   **Ethical Use:** Always consider the ethical implications of the content you create. Respect privacy, avoid misinformation, and do not generate content that could be used to harass, defame, or exploit others.

By using this bot, you agree to these terms and acknowledge your responsibility for the generated content.


