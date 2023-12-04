import discord
import spacy
import patterns_data
import os
import bot

client = bot.client
patterns = patterns_data.patterns
# Load the spaCy English language model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
finally:
    nlp = spacy.load("en_core_web_sm")
with open("constants.txt", "r") as f:
    Content = f.readlines()
    Token = Content[0].replace("TOKEN:", "")
    general_channel = int(Content[1].replace("GENERAL_CHANNEL:", ""))
    support_channel = int(Content[2].replace("SUPPORT_CHANNEL:", ""))
    logging_channel = int(Content[3].replace("LOGGING_CHANNEL:", ""))
    faq_channel = int(Content[4].replace("FAQ_CHANNEL:", ""))
    staff_role_id = int(Content[5].replace("STAFF_ROLE:", ""))
    supporter_role_id = int(Content[6].replace("SUPPORTER_ROLE:", ""))
    developer_role_id = int(Content[7].replace("DEVELOPERS_ROLE:", ""))
    report_channel_id = int(Content[8].replace("REPORT_CHANNEL:", ""))
    rp_log_channel_id = int(Content[9].replace("RP_LOG_CHANNEL:", ""))
