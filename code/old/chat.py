from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new instance of a ChatBot
chatbot = ChatBot(
    'ARCA',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Lo siento, no entendí.',
            'maximum_similarity_threshold': 0.90
        }
        #,
        #{
        #    'import_path': 'chatterbot.logic.SpecificResponseAdapter',
        #    'input_text': 'Help me!',
        #    'output_text': 'Ok, here is a link: http://chatterbot.rtfd.org'
        #},
        #{
        #    'import_path': 'chatterbot.logic.TimeLogicAdapter',
        #    'positive':
        #    ['¿Qué hora es?', '¿Me podrías dar la hora?']
        #}
        # ,
        # {
        #     'import_path':
        #     'chatterbot.logic.MathematicalEvaluation',
        #     'language': 'chatterbot.languages.ES'
        # }
    ],
    database_uri='sqlite:///database.db')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.spanish")

# Now we can export the data to a file
# trainer.export_for_training('./my_export.json')

while True:
    try:
        text = input()
        bot_input = chatbot.get_response(text)
        print(bot_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
