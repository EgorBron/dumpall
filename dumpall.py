with open('token.txt') as tkf:
    tk = tkf.readline()

import discum     
me = discum.Client(token=tk, log=False)

@bot.gateway.command
def evt(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = me.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
    if resp.event.message:
        msg = resp.parsed.auto()
        if msg['content'].lower().strip() == 'dumpall':
            ... # we will create some magic soon

me.gateway.run(auto_reconnect=True)
