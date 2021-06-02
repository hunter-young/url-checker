import aiosmtplib
import asyncio
from typing import List
from email.message import EmailMessage
from . import validations

settings = validations.EnvironmentSettings()
   
server_conf = {
    'hostname': settings.smtp_server,
    'username': settings.smtp_username,
    'password': settings.smtp_password,
    'port': settings.smtp_port,
    'use_tls': settings.smtp_use_tls
}

async def send_admin_alert(check_definition: validations.Check):
    message = EmailMessage()
    message['From'] = settings.sender_email
    message['To'] = settings.admin_email
    message['Subject'] = f'{check_definition.url} is in a failure state for 3 or more times'
    message.set_content(f'CheckId {check_definition.id} for URL {check_definition.url}' 
                        'has failed 3 or more times. Admin attention may be required to ensure no issue is present')
    await aiosmtplib.send(message, **server_conf)

async def send_alert(check_definition: validations.Check, receivers: List[str]):
    message = EmailMessage()
    message['From'] = settings.sender_email
    message['Subject'] = f'{check_definition.url} check has failed'
    message.set_content(f'CheckId {check_definition.id} for URL {check_definition.url}' 
                        'is in a failure state.')
    for email_address in receivers:
        message['To'] = email_address
        await aiosmtplib.send(message, **server_conf)


if __name__ == '__main__':
    message = EmailMessage()
    message["From"] = settings.sender_email
    message["To"] = settings.admin_email
    message["Subject"] = "E-mail configuration"
    message.set_content("Success! E-mail is properly configured")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aiosmtplib.send(message, **server_conf))
