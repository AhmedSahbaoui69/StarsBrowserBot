# Stars Browser WhatsApp Bot
![ad](https://i.ibb.co/dg6FSp4/Whats-App-Image-2024-01-14-at-11-00-32-PM-removebg-preview.png)

## Description

This WhatsApp bot helps you browse the web under ***6 restrictions**. It works like a **middleman** by fetching web content for you.  

You send **commands** on WhatsApp in the form of text messages and the bot does the browsing behind the scenes, then sends you a **complete** html file including **external CSS, JS and images**.

## Preview

![Bot Preview](preview.gif)

## Installation

### Before You Begin:
- Follow the [WhatsApp Business API documentation](https://developers.facebook.com/docs/whatsapp) to set up your WhatsApp Business Account and App, as well as your Access Token.  
- To run the bot, it needs to be hosted on a server with an SSL certificate. I recommend using [replit.com](https://replit.com/~) as it is free of charge and very simple to use.

### 1. Clone the Repository

```bash
git clone https://github.com/AhmedSahbaoui69/StarsBrowserBot.git
cd StarsBrowserBot
```
### 2. Install Dependencies

Ensure you have Python and pip installed. Then, run the following command to install the project dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Add add the following environment variables to your shell:

```bash
VERIFY_TOKEN=your_verify_token
PAGE_ACCESS_TOKEN=your_page_access_token
WHATSAPP_URL=your_whatsapp_url
```

### 4. Run the Bot on a Server
```bash
python3 main.py
```

## How to Use

- `/google <query>` Search Google for a specified query.  
  *Example: /google how to make a pipe bo*

- `/googleimage <query>` Search Google Images for a specified query.  
  *Example: /googleimage cute puppies*

- `/yahoo <query>` Search Yahoo for a specified query.  
  *Example: /yahoo www.google.com*

- `/url <url>` Retrieve the HTML content of a specified URL.  
  *Example: /url https://en.wikipedia.org/wiki/Adolf_Hitler*

- `/urban <term>` Get the Urban Dictionary definition of a term.  
  *Example: /urban amogus*
  
- `/spanish <expression>` Get the spanish translation and pronounciation of an expression.  
  *Example: /spanish I would like to get a pizza*

- `/tts <expression>` Generate text to speech of a phrase.  
  *Example: /tts hello your computer has virus*

## License

This project is licensed under the [MIT License](LICENSE).
