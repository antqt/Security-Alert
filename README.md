# Security Alert
This bot will notify the new update of the URL on telegram. 

# Getting Started

- Create a bot on telegram
    
    Click [this link](https://telegram.me/BotFather) and it will open your telegram client and start a chat with the BotFather. Send the message “/newbot” (no quotes) and follow the instructions.
    
    ![Untitled](pictures/Untitled.png)
    
- Install telegram-send and link it to your bot
    
    To install, open a terminal and run `pip install telegram-send` followed by `telegram-send configure`
    
    `telegram-send` will ask for the token you got from the botfather, and then give you a password that you need to message to your new bot on Telegram.
    
    ![Untitled](pictures/Untitled_1.png)
    
    Create a **group** and add your bot then send the password.
    
    ![Untitled](pictures/Untitled_2.png)
    
    ![Untitled](pictures/Untitled_3.png)
    
    The bot added to your group can’t send messages, therefore we need to promote it to admin.
    
    ![Untitled](pictures/Untitled_4.png)
    
- Create the configuration file for the URL with the format:

```yaml
host: {The domain of the url}
tuple_location: {The head and tail the tuple}
link_location: {The location of the token to locate the link inside the tuple}
name_location: {The location of the token to locate the name inside the tuple}
pages: {The parameter of the pages, can leave blank if there only one page}
empty_page: {The string of the 404 page (to locate all the pages)}
report_location: {the location to save the record}
```

For example `github.yaml`:

```yaml
host: 'https://github.com' #the url
tuple_location: '"pull_request"(.*)</a>' #Between red boxs
link_location: 'href="(.*)"' #Between yellow boxs
name_location: '">(.*)' #Between green boxs
pages: '?page=' #In cyan box
empty_page: 'reports/github_report.yaml' #string in 404 page
report_location: 'reports/github_report.yaml' #location to save record
```

![Untitled](pictures/Untitled_5.png)

- Store the URL and the configuration in `links.yaml`

```yaml
#links : profile
'https://github.com/projectdiscovery/nuclei-templates/pulls' : 'github.yaml'
'https://wordpress.org/news/category/security/' : 'wordpress.yaml'
```

- Run the python file `app.py`

```bash
python3 app.py
```

If there is any new update, the bot will notify on your telegram

![Untitled](pictures/Untitled_6.png)