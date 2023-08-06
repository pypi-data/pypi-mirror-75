aiogmailsender
==============
This is an asynchronous Gmail client that can send emails currently.

Quickstart
--------------
.. code-block:: python

    import asyncio
    import logging
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    import aiogmailsender

    async def arun():
        sender = await aiogmailsender.create('<gmailusername>',
                                             '<gamilpassword>',
                                             rate_limit=60, # How many emails sender sends within a minute
                                             pool_size=2, # How many clients are kept in pool
                                             retry=5, # How many times sender retries to send a message, when sending fails
                                             backoff=30, # How long sender sleep before retry (unit. seconds)
                                             backoff_limit=300 # Max backoff (everytime sender retries, the backoff time increases exponentially and the time can't be over this limit.)
                                             )

        tasks = []
        for i in range(10):
            message = MIMEMultipart('alternative')
            message["From"] = 'test'
            message["To"] = '<targetemail>'
            message["Subject"] = f'test {i}'

            part = MIMEText('test', 'html')
            message.attach(part)
            tasks.append(sender.send(message))

        await asyncio.gather(*tasks)


    if __name__ == '__main__':
        logging.basicConfig(format="%(asctime)s %(levelname)s:%(name)s:%(message)s", level=logging.DEBUG)
        asyncio.run(arun())
