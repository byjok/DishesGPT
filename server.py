from flask import Flask, render_template, request, session, redirect, url_for
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'
openai.api_key = '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'

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    if 'messages' not in session:
        session['messages'] = []
    messages_list = session['messages']      
    messages_list.append({"role": "user", "content": prompt})
    session['messages'] = messages_list
    response = openai.ChatCompletion.create(
        model ='gpt-3.5-turbo',
        messages=session['messages'],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
 #   print(response.choices[0].message.content)
    messages_list = session['messages'] 
    messages_list.append({"role": "assistant", "content": response.choices[0].message.content})
    session['messages'] = messages_list
    return render_template('index.html', response=response.choices[0].message.content)

@app.route('/view_messages')
def view_messages():
    messages = session.get('messages', [])
    return render_template('view_messages.html', messages=messages)

if __name__ == '__main__':
    app.run()
