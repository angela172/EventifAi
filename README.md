# 📆 Welcome to our app _EventifAI_ 📆
by team Molten Core 🌋

_**Your Eventful future made easy**_
---

# About our app:

This is your one-stop app for seamlessly planning out all your events. 
Schedule 🌍 on-site and 💻 online events on 📆 Google Calendar, and send out personalized Invite 📧 Emails to your invitees, all with a simple prompt to our AI 🦙

---

- Our main app is _**run_app.py**_

- [Check out our app hosted on 👑Streamlit](https://moltencorehacktheloop-gzxkgpjrg7f7ibphws9pmx.streamlit.app/)

---

# 💡 Please go through these carefully to successfully run our app:

We make use of _Google API_ services to successfully help automate your event management. Ensure you have:
- A [Google Cloud Console Project](https://developers.google.com/workspace/guides/create-project) with valid API's and OAuth ClientID's which gives you a valid credentials (`configs.json` as referenced in our program)
  
- To Create an `API key and OAuth` , go to `API's & Services` =>  `Create Credentials` and Create a new API Key and a new OAuth Client ID.
  
- Enabled the Gmail and Google Calendar API (by searching it in the API Library and click `Enable`)
  with Scopes set to the following: https://www.googleapis.com/auth/calendar and https://www.googleapis.com/auth/gmail.send
  
- Download and add `configs.json` to this project directory => then run `autherizor_for_tokens.py` to generate a `token.json` file

- Add your API key in the `config.yaml` file
  
🎥 Check out [this video](https://youtu.be/B2E82UPUnOY) on how to create a project and get your keys and configs! _(credits: [NeuralNine](https://www.youtube.com/@NeuralNine))_ 


# We leverage Llama 3 8B as our llm 🦙

To run it using Ollama:
- Run Command Prompt as Administrator

- Update pip and install these dependencies:
```
pip install --upgrade pip
pip install ollama
```
- Install PyTorch
```
pip install torch torchvision torchaudio
```
With all the above installed, clone this repo and `streamlit run run_app.py`!

```
Post note:
Since we host Llama locally, and we utilize Google API's, there is some delay in the responses.
But a couple of patient retries should do the job 😊
```
_**Say goodbye to tedious scheduling, and say hello to an eventful future! 🦙🎉**_
 
