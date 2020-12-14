from py2neo.ogm import Model, RelatedFrom, RelatedTo, Property


class Mail(Model):
    __primarykey__ = "message_id"

    message_id = Property()
    body = Property()
    subject = Property()
    date = Property()

    sender = RelatedFrom("Recipient", "SENT")
    to = RelatedFrom("Recipient", "RECEIVED")


class Recipient(Model):
    __primarykey__ = "mail"

    mail = Property()

    sent = RelatedTo(Mail)
    received = RelatedTo(Mail)

