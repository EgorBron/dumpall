# dumpall
Simple Discord group dumper for selfbots

## Usage
### Installation:
```sh
git clone https://github.com/EgorBron/dumpall.git
cd dumpall
```
Edit `token.txt`: paste here token of your account.

Install dependencies:
```sh
pip3 install -r requirements.txt
```
Run the bot:
```sh
python3 dumpall.py
```
If yo see `Connected!` in console, all ok.

In summary:
```sh
git clone https://github.com/EgorBron/dumpall.git
cd dumpall
pip3 install -r requirements.txt
python3 dumpall.py
```
### Dumping:
Open Discord, then group what you need to dump and copy ID of it. Then send `dump GROUPID GUILDID_or_NEW CHANNELID_or_NEW` to console. After that, dump process will be started. Script will create a new server with all messages from target group and folder contains JSON file with same data (and as bonus all downloaded files).
### Restoring
Search for needed group folder in script folder. Then send `restore GROUPID GUILDID_or_NEW CHANNELID_or_NEW` to console. After that, restore process will be started. Script will create a new server with all messages from target group.
### Examples:
No any examples for now :(
