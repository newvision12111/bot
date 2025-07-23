import logging
import os
import webuiapi
from PIL import Image
import io
import random

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Initialize webuiapi client
# Assuming Stable Diffusion web UI is running on http://127.0.0.1:7860
api = webuiapi.WebUIApi(host=\'127.0.0.1\', port=7860)

# List of prohibited keywords for basic filtering
PROHIBITED_KEYWORDS = [
    "child abuse", "child porn", "loli", "shota", "gore", "hate speech",
    "violence against minors", "non-consensual sexual content", "bestiality",
    "self-harm", "illegal activities", "drug manufacturing", "terrorism"
]

def contains_prohibited_keywords(text: str) -> bool:
    """Checks if the text contains any prohibited keywords."""
    text_lower = text.lower()
    for keyword in PROHIBITED_KEYWORDS:
        if keyword in text_lower:
            return True
    return False

def generate_image(prompt: str) -> bytes:
    """Generate an image using Stable Diffusion."""
    if contains_prohibited_keywords(prompt):
        raise ValueError("Prompt contains prohibited content.")
    try:
        # Generate image using txt2img
        result = api.txt2img(
            prompt=prompt,
            negative_prompt="low quality, blurry, bad anatomy, worst quality, low quality, low resolution, extra fingers, blur, blurry, ugly, wrong proportions, watermark, image artifacts",
            width=512,
            height=512,
            cfg_scale=7,
            steps=20,
            sampler_name="DPM++ 2M Karras"
        )
        
        # Convert PIL Image to bytes
        img_bytes = io.BytesIO()
        result.image.save(img_bytes, format=\'PNG\')
        img_bytes.seek(0)
        return img_bytes.getvalue()
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return None

def generate_gif(prompt: str, frames: int = 4) -> bytes:
    """Generate a GIF by creating multiple images with slight variations."""
    if contains_prohibited_keywords(prompt):
        raise ValueError("Prompt contains prohibited content.")
    try:
        images = []
        for i in range(frames):
            # Add slight variation to the prompt for each frame
            varied_prompt = f"{prompt}, frame {i+1}, slight variation"
            result = api.txt2img(
                prompt=varied_prompt,
                negative_prompt="low quality, blurry, bad anatomy, worst quality, low quality, low resolution, extra fingers, blur, blurry, ugly, wrong proportions, watermark, image artifacts",
                width=512,
                height=512,
                cfg_scale=7,
                steps=15,  # Fewer steps for faster generation
                sampler_name="DPM++ 2M Karras",
                seed=random.randint(1, 1000000)  # Random seed for variation
            )
            images.append(result.image)
        
        # Create GIF
        gif_bytes = io.BytesIO()
        images[0].save(
            gif_bytes,
            format=\'GIF\',
            save_all=True,
            append_images=images[1:],
            duration=500,  # 500ms per frame
            loop=0
        )
        gif_bytes.seek(0)
        return gif_bytes.getvalue()
    except Exception as e:
        logger.error(f"Error generating GIF: {e}")
        return None

async def start(update: Update, context) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! 🎨" + "\n\n"
        "I'm a bot that generates images and GIFs based on your text descriptions!\n\n"
        "**Important Disclaimer:** This bot uses a self-hosted Stable Diffusion model. While I have basic filters, you are solely responsible for the content you generate. Please use this bot responsibly and adhere to all applicable laws and ethical guidelines. Avoid generating illegal, harmful, or non-consensual content.\n\n"
        "Commands:\n"
        "/image <description> - Generate a single image\n"
        "/gif <description> - Generate an animated GIF\n"
        "/help - Show this help message\n\n"
        "Or just send me any text and I'll generate an image for you!"
    )

async def help_command(update: Update, context) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🎨 Image Generation Bot Commands:\n\n"
        "/image <description> - Generate a single image\n"
        "/gif <description> - Generate an animated GIF (4 frames)\n"
        "/start - Show welcome message\n"
        "/help - Show this help message\n\n"
        "**Important Disclaimer:** This bot uses a self-hosted Stable Diffusion model. While I have basic filters, you are solely responsible for the content you generate. Please use this bot responsibly and adhere to all applicable laws and ethical guidelines. Avoid generating illegal, harmful, or non-consensual content.\n\n"
        "You can also just send me any text description and I'll generate an image!\n\n"
        "Examples:\n"
        "• 'A beautiful sunset over mountains'\n"
        "• 'A cyberpunk city at night'\n"
        "• 'A cute cat wearing sunglasses'\n\n"
        "Note: Make sure Stable Diffusion WebUI is running on http://127.0.0.1:7860"
    )
    await update.message.reply_text(help_text)

async def generate_image_command(update: Update, context) -> None:
    """Handle the /image command."""
    if not context.args:
        await update.message.reply_text("Please provide a description after /image\nExample: /image a beautiful landscape")
        return
    
    prompt = " ".join(context.args)
    if contains_prohibited_keywords(prompt):
        await update.message.reply_text("❌ Your request contains prohibited keywords. Please revise your prompt.")
        return

    await update.message.reply_text(f"🎨 Generating image for: '{prompt}'\nPlease wait...")
    
    image_bytes = generate_image(prompt)
    if image_bytes:
        await update.message.reply_photo(photo=io.BytesIO(image_bytes), caption=f"Generated: {prompt}")
    else:
        await update.message.reply_text("❌ Sorry, I couldn't generate the image. Make sure Stable Diffusion WebUI is running.")

async def generate_gif_command(update: Update, context) -> None:
    """Handle the /gif command."""
    if not context.args:
        await update.message.reply_text("Please provide a description after /gif\nExample: /gif a dancing robot")
        return
    
    prompt = " ".join(context.args)
    if contains_prohibited_keywords(prompt):
        await update.message.reply_text("❌ Your request contains prohibited keywords. Please revise your prompt.")
        return

    await update.message.reply_text(f"🎬 Generating GIF for: '{prompt}'\nThis may take a moment...")
    
    gif_bytes = generate_gif(prompt)
    if gif_bytes:
        await update.message.reply_animation(animation=io.BytesIO(gif_bytes), caption=f"Generated GIF: {prompt}")
    else:
        await update.message.reply_text("❌ Sorry, I couldn't generate the GIF. Make sure Stable Diffusion WebUI is running.")

async def handle_text_message(update: Update, context) -> None:
    """Handle regular text messages by generating images."""
    prompt = update.message.text
    if contains_prohibited_keywords(prompt):
        await update.message.reply_text("❌ Your request contains prohibited keywords. Please revise your prompt.")
        return

    await update.message.reply_text(f"🎨 Generating image for: '{prompt}'\nPlease wait...")
    
    image_bytes = generate_image(prompt)
    if image_bytes:
        await update.message.reply_photo(photo=io.BytesIO(image_bytes), caption=f"Generated: {prompt}")
    else:
        await update.message.reply_text("❌ Sorry, I couldn't generate the image. Make sure Stable Diffusion WebUI is running.")

def main() -> None:
    """Start the bot."""
    # Get bot token from environment variable
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Please set it with: export TELEGRAM_BOT_TOKEN=\'your_bot_token_here\' ")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("image", generate_image_command))
    application.add_handler(CommandHandler("gif", generate_gif_command))

    # Add message handler for regular text (generates images)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Run the bot until the user presses Ctrl-C
    print("Starting bot...")
    print("Make sure Stable Diffusion WebUI is running on http://127.0.0.1:7860 with --api flag")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

