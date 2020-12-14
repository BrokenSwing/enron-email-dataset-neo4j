import mailparser
import itertools
import os
from models import Mail, Recipient
import threading
from py2neo.ogm import Repository
import concurrent.futures


def parse_mail(filepath):
    mail = mailparser.parse_from_file(filepath)
    return mail


def convert_to_model(parsed_mail):
    mail = Mail()
    mail.message_id = parsed_mail.message_id
    mail.body = parsed_mail.body
    mail.subject = parsed_mail.subject
    mail.date = parsed_mail.date
    for recipient in recipients_from_list_of_tuples(parsed_mail.to, parsed_mail.cc, parsed_mail.bcc):
        mail.to.add(recipient)
    mail.from_ = recipient_from_tuple(parsed_mail.from_[0])
    return mail


def recipients_from_list_of_tuples(*parsed_recipients):
    return [recipient_from_tuple(r) for r in itertools.chain(*parsed_recipients)]


def recipient_from_tuple(recipient_tuple):
    recipient = Recipient()
    name, email = recipient_tuple
    recipient.mail = email
    return recipient


def file_path_to_model(args):
    filepath, repo = args
    parsed_mail = mailparser.parse_from_file(filepath)
    mail_model = convert_to_model(parsed_mail)
    repo.save(mail_model)
    return mail_model


def main():
    repo_url = os.getenv("NEO4J_URL")
    password = os.getenv("NEO4J_PASSWORD")
    print("Neo4j: {0}".format(repo_url))
    repo = Repository(repo_url, password=password)
    print("Connected to Neo4j !")

    pool = concurrent.futures.ThreadPoolExecutor()

    processed_count = 0
    for root, dirs, files in os.walk("D:/Downloads/enron_mail_20150507.tar/enron_mail_20150507/maildir/allen-p/"):
        pool.map(file_path_to_model, [(os.path.join(root, filepath), repo) for filepath in files])
        computed_now = len(files)
        processed_count += computed_now
        print("Processed {0} (+{1}) files. Continuing ...".format(processed_count, computed_now))

    print("Done !")


if __name__ == '__main__':
    main()
