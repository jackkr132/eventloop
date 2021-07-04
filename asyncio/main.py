import asyncio
import sqlite3
import aiosmtplib
from email.message import EmailMessage


async def send_email(name, email_to, index):
    message = EmailMessage()
    message["From"] = "root@localhost"
    message["To"] = email_to
    message["Subject"] = "Hello World!"
    message.set_content(
        f"Уважаемый {name}!\nСпасибо, что пользуетесь нашим сервисом объявлений."
    )

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=465,
        use_tls=True,
        username='user@gmail.com',
        password='app_password'
    )
    print(f'Task {index} end')


async def main():
    tasks = []
    con = sqlite3.connect('contacts.db')
    cur = con.cursor()
    for index, row in enumerate(cur.execute(
            'SELECT first_name, last_name, email FROM contacts'
    )):
        name = row[0] + ' ' + row[1]
        email_to = row[2]
        print(f'Starting task {index} - <{email_to}>')
        task = asyncio.create_task(send_email(name, email_to, index))
        tasks.append(task)

    for task in tasks:
        await task

if __name__ == '__main__':
    asyncio.run(main())
