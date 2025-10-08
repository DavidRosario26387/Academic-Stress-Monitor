from dotenv import load_dotenv
import os
from responses import get_response
from discord import Intents,Client,Message
from analyse import predict
from llm_inference import Chain
from RAG import setup_rag
import logging
from datamodel import MongoHandler
import hashlib

load_dotenv()
DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# For logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

intents=Intents.default()
intents.message_content=True
client=Client(intents=intents)

# mongoDBD Connection
mongo = MongoHandler(
    uri=MONGO_URI,
    db_name="Hackathon",
    collection_name="Stress_logs"
)

async def send_message(message, user_message, llm_obj):
    if not user_message:
        logger.warning("Empty message received from user.")
        return
    try:
        response,label,category,score = get_response(user_message, llm_obj)
        if response and response.get("message"):
            await message.author.send(response["message"])
            logger.info(f"Sent response to {message.author}.")

            # Insert message into MongoDB asynchronously
            await mongo.insert_record(
                    {
                        "Username":hashlib.sha256(str(message.author).encode()).hexdigest(),
                        "Time_stamp":message.created_at,
                        "Message":str(user_message),
                        "Stress_label":str(label),
                        "Stress_category":str(category),
                        "Stress_Score":score,
                        "Recommendation_given":str(response["message"]),
                        "Stress_Reason":str(response["reason"])
                    }
                )
        else:
            logger.info(f"Message Classified as NO STRESS.")
            await mongo.insert_record(
                {
                    "Username":hashlib.sha256(str(message.author).encode()).hexdigest(),
                    "Time_stamp":message.created_at,
                    "Message":str(user_message),
                }
            )

        
    except Exception as e:
        logger.error(f"Error sending response: {e}", exc_info=True)

#handle the startup for our bot
@client.event
async def on_ready():
    logger.info(f"{client.user} Bot started!")

#handle incoming message
@client.event
async def on_message(message):
    if message.author==client.user:
        return
    username=str(message.author)
    user_message=str(message.content)
    channel=str(message.channel)
    logger.info(f"[{channel}] {username}: {user_message}")

    await send_message(message,user_message,llm_obj)

def main():
    client.run(token=DISCORD_TOKEN)

if __name__=='__main__':
    llm_obj=Chain()
    logger.info("LLM Initialized")
    setup_rag()
    logger.info("RAG initialized")
    main()