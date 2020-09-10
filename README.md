# Mailbot

Mailbot is a command-line email sending program, for use with Oath2 servers, such as Gmail.

## Install

This program can be installed by running `python setup.py install`.

Mailbot can also be run from the docker image, using something like `docker run -v ~/.standard_files/config/mailbot/:/root/.config/mailbot/ --rm -it mailbot`.

## Config

Mailbot stores it's configs in ~/.config/mailbot. This directory includes tokens for authenticated email addresses and the client_id.json file used for connecting to Gmail. To obtain this, you need to generate one at `https://console.developers.google.com/apis/api/gmail.googleapis.com`.

