![image](https://raw.githubusercontent.com/Al-Taie/quick-mailer/master/images/bsmala.png)

# Description
This Module help you to send fast Email.

And you can attach **image, audio, and other files easily.**

The Module support **Gmail** right now, but in the nearly future will support other mail services.

# Installation:
```cmd
pip install quick-mailer
```

[Github Link](https://github.com/Al-Taie/quick-mailer)

# Usage:
```py
from mailer import Mailer

mail = Mailer(email='someone@gamil.com'
              password='your_password')

mail.send(receiver='someone2@gmail.com',
          subject='First Message',
          message='Hello This Message From Python')
```
**Parameters**
```py
receiver: Email Address [Recuired]
subject: Message Title  [Optional]
message: Your Message   [Optional]
image: Image File Name  [Optional]
audio: Audio File Name  [Optional]
file: File Name         [Optional]
```
**Follow Me on Instagram: [@9_Tay](https://www.instagram.com/9_tay).**

# Thank You :)