# SudoPhish
A web server for GoPhish landing pages that allows you to use GoPhish without exposing the GoPhish server itself.

## Installation
1. git clone https://github.com/secw01f/sudophish
2. cd sudophish
3. pip3 install -r requirements.txt
4. python3 sudophish.py -h

## How-To

SudoPhish is relatively easy to use, but there is a few important steps need to be made when running SudoPhish for a campaign. Those steps are listed below:

1. If you wish to capture credentials, "Capture Submitted Data" must be selected in the GoPhish Landing Page form. If you wish to capture passwords as well, "Capture Passwords" must be selected. If these are not selected they will only be captured by SudoPhish and not passed along.
2. When setting up your campaign in GoPhish, the "URL" value must be set to the IP or domain of your GoPhish server. This only needs to be reachable by the server where you are hosting SudoPhish.
