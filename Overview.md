# Introduction #

There are many cases when a message must be reliably delivered to receiver:
  * Alert on some predefined event
  * Appointment cancellation
  * Schedule change
  * Emergency of some kind

The project tries to deliver the message using ways that are defined by the receiver using several options:
  * EMail
  * Instant message over popular IM services (Jabber, AIM, etc)
  * SMS to certain phone numbers in a given order
  * Voice phone call with transcription of the message

Each communication method will provide a way (one-time http link?) to for receiver to acknowledge message arrival confirmation.

# SMS sending #

There is no single SMS provider that works perfectly in every country in the world. Thus, for attaining truly global SMS coverage, one must use several SMS providers.

The application automatically detects best available SMS provider for a given phone number and uses it to send the SMS.

# Commercial offerings #

Company [TeleMessage](http://www1.telemessage.com) might have some or all features of the project.