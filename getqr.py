import uuid
import qrcode
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Function to generate a QR code containing a UUID
def generate_qr_code(unique_id: str) -> BytesIO:
    # Create a QR code from the UUID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(unique_id)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a BytesIO object
    bio = BytesIO()
    bio.name = 'qr.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    
    return bio

# Function to save the UUID and arguments to a text file
def save_uuid_to_file(unique_id: str, args: str):
    with open("uuid_records.txt", "a") as file:
        file.write(f"UUID: {unique_id}, Args: {args}\n")

# Function to retrieve the arguments associated with a UUID from the file
# def get_args_from_uuid(unique_id: str) -> list:
#     with open("uuid_records.txt", "r") as file:
#         for line in file:
#             if line.startswith(f"UUID: {unique_id}"):
#                 # Extract the args part of the line
#                 args_part = line.split("Args: ", 1)[1].strip()
#                 # Return the args as a list, split by space
#                 return args_part.split()
#     return []

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Отправьте любое сообщение чтобы сгенерировать QR код.")

# /get_qr command handler
async def get_qr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Generate a UUID
    unique_id = str(uuid.uuid4())
    
    # Get the arguments passed with the command
    args = update.message.text if update.message.text else ""
    
    # Save the UUID and arguments to a text file
    save_uuid_to_file(unique_id, args)
    
    # Generate the QR code
    qr_image = generate_qr_code(f"https://t.me/clobsluzbot?start={unique_id}")

    # Send the QR code as an image
    await update.message.reply_photo(photo=qr_image, caption=f"Вот необходимый QR код.\nUUID: {unique_id}")

# /get_args command handler (to test get_args_from_uuid function)
# async def get_args(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the UUID from the command arguments
    # if context.args:
    #     uuid_to_lookup = context.args[0]
    #     args_list = get_args_from_uuid(uuid_to_lookup)
        
    #     if args_list:
    #         await update.message.reply_text(f"Arguments for UUID {uuid_to_lookup}: {', '.join(args_list)}")
    #     else:
    #         await update.message.reply_text(f"No arguments found for UUID {uuid_to_lookup}.")
    # else:
    #     await update.message.reply_text("Please provide a UUID to look up.")

def main():
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    application = Application.builder().token("6863119440:AAGRz9TQPNo6GeYVkLNa-WaQ2yqppwOoee8").build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_qr))
    # application.add_handler(CommandHandler("get_args", get_args))

    # Start the bot by polling Telegram for updates
    application.run_polling()

if __name__ == '__main__':
    main()
