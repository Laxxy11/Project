# Task-1

**Sending Email using FastAPI Framework in Python**

- **Installation of required pkg using poetry**
    
    The fastapi-mail is a simple lightweight mail system, for sending emails and attachments(individual && bulk).
    
    `In poetry shell`
    
    ```python
    poetry add fastapi-mail
    ```
    
    After installing the module and setting up your `FastApi` app:
    Main classes and packages are :
    `FastMail` `ConnectionConfig` `MessageSchema` `email_utils.DefaultChecker` `email_utils.WhoIsXmlApi`
    
- **Mailtrap**
    
    Email Delivery Platform for individuals and businesses to test, send and control email infrastructure in one place.
    
    By using mailtrap , we can perform Email Testing.
    
- **Create a .env file**
    
    ```python
    MAIL_USERNAME=<User_Name>
    MAIL_PASSWORD=<Password>
    MAIL_FROM="example@gmail.com"
    MAIL_PORT=2525
    MAIL_SERVER="sandbox.smtp.mailtrap.io"
    MAIL_FROM_NAME=<mai from name>
    ```