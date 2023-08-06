import argparse
import logging
import os
import configparser
import inquirer
import re

config_questions = [
    inquirer.List('library', choices=['mysql'],
                  message="Which library do you want to configure?")
]

mysql_questions = [
    inquirer.Text('username', message="Username", default="root"),
    inquirer.Text('password', message="Password", default="a123"),
    inquirer.Text('host', message="Host", default="127.0.0.1"),
    inquirer.Text('port', message="Port", default="3306"),
    inquirer.Text('schema', message="Schema", default="database-name"),
    inquirer.Text('minConnection', message="Min Connection", default="1"),
    inquirer.Text('maxConnection', message="Max Connection", default="10")
]

logger_questions = [
    inquirer.Text('name', message="Name", default="root"),
    inquirer.Text('file', message="File", default="./app.log")
]


def _check_exists_tag_name(filename, tag_name):
    if os.path.isfile(filename):
        parser = configparser.ConfigParser()
        parser.read(filename)
        exists_tag = set(parser.keys())
        if tag_name in exists_tag:
            return True

    return False


def _gen_config(default_tag_name, questions):
    config = {}
    try:
        tag_name = inquirer.prompt([
            inquirer.Text('tagname', message="Tag Name", default=default_tag_name)
        ])['tagname']

        if _check_exists_tag_name('config.ini', tag_name):
            logging.warning("Tag name already exists!")
            return

        config = inquirer.prompt(questions)
    except KeyboardInterrupt as e:
        logging.error("Process is killed by user!")
        return

    with open('config.ini', 'a') as f:
        f.write("[%s]\n" % tag_name)
        for key, value in config.items():
            f.write("%s=%s\n" % (key, value))


def main():

    answers = inquirer.prompt(config_questions)

    if answers['library'] == 'mysql':
        _gen_config("mysqldb", mysql_questions)
    else:
        logging.error("Unknown Error")
