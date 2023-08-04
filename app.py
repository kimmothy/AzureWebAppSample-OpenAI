import os
from dotenv import load_dotenv
import openai

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def getAOAIResponse(message):
    try: 

        # Get configuration settings 
        load_dotenv()
        azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
        azure_oai_key = os.getenv("AZURE_OAI_KEY")
        azure_oai_model = os.getenv("AZURE_OAI_MODEL")
        
        # Read text from file
        text = message
        
        # Set OpenAI configuration settings
        openai.api_type = "azure"
        openai.api_base = azure_oai_endpoint
        openai.api_version = "2023-03-15-preview"
        openai.api_key = azure_oai_key

        # Send request to Azure OpenAI model
        print("Sending request for summary to Azure OpenAI endpoint...\n\n")
        response = openai.ChatCompletion.create(
            engine=azure_oai_model,
            temperature=0.7,
            max_tokens=120,
            messages=[
            {"role": "system", "content": "You are a freindly AI. Answer my questions kindly."},
                {"role": "user", "content": text}
            ]
        )

        return response
        

    except Exception as ex:
        print(ex)

@app.route('/hello', methods=['POST'])
def hello():
   message = request.form.get('message')

   if message:
       print('Request for hello page received with message=%s' % message)
       response = getAOAIResponse(message)["choices"][0]["message"]["content"]
       return render_template('hello.html', response = response)
   else:
       print('Request for hello page received with no message or blank message -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
