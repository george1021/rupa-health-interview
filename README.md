## Local Installation

1. Clone the [repository](https://github.com/george1021/rupa-email-service):
```bash
git clone https://github.com/george1021/rupa-health-interview.git
cd rupa-health-interview
```

2. Create a separate Python environment for application and install required modules:

For Unix
```bash
pip3 install virtualenv
virtualenv app_env
source app_env/bin/activate
pip install -r requirements.txt
```
For Windows
```bash
pip3 install virtualenv
python -m virtualenv app_env
.\app_env\Scripts\activate
pip install -r .\requirements.txt
```

3. Check the config.yaml file. This file is where you may change the default email service used and it also 
   keeps track of the last service used so it is able to switch when redeployed
   

4. Finally run the application:
```bash
python main.py
```

5. Use the locally-hosted service by using an API platform such as Postman, or curl from the command line. 
   - curl
     ```bash
     curl -d "{\"to\":\"crgeorge1021@gmail.com\",\"to_name\":\"cg\",\"from\":\"chris@em8912.rupainterviewcg.com\",\"from_name\":\"chris\",\"subject\":\"test subject\", \"body\":\"test email body\"}" --header "Content-Type: application/json" -X POST http://127.0.0.1:5000
     ```
   - Postman: set up a POST request with the following settings
     - url = http://127.0.0.1:5000
     - body as JSON = ``` 
       {
            "to": "crgeorge1021@gmail.com",
            "to_name": "cg",
            "from": "chris@em8912.rupainterviewcg.com",
            "from_name": "chris",
            "subject": "test subject",
            "body": "test email body"
        }```


## Description
This service uses Python and Flask. I chose Python because I am very comfortable developing and debugging in 
that environment, and I knew Flask (a Python package used to host web servers), was a quick was to get a 
simple API up and running. The primary library is Flask, which builds the actual application routes and binds the
functions to those routes. Besides Flask, helper libraries are used such as html2text, to quickly decode the html to
readable text as the problem statement requires, requests to send the API requests to MailGun and SendGrid,
and dotenv to load environment variables used to make the API calls, among others.

## Issues
The services I signed up for are on the free trials, so there are limits to the amounts of requests that can be made.

One potential issue is that SendGrid only allows emails to come from a registered domain, so this will limit user input.
I registered a domain under em8912.rupainterviewcg.com to be used for
testing. For example, the "from" email should be "nick@em8912.rupainterviewcg.com" for SendGrid to send the email.

## Improvements
If I were to spend more time on the project, I could...
- Wrap up the "main.py" functions into a class. In this case,
there is not significant benefit, but could save a few lines of code.
- Hide my security keys if I had more time to make this a robust application hosted on a server instead of
running locally.
- Break out some of the helper functions into their own utils.py file to better organize the code and keep the
main file to the basic functionality
- Clean up the response codes and provide more detailed feedback for users based on API responses

## Time
I spent about 8 hours on the whole project. About 4 of those were spent setting up the domain and trying to debug
SendGrid, which ultimately was not working due to an account suspension after creation and before any emails 
were sent using the service.