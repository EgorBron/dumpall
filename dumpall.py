from asyncio import coroutines
import asyncio
from math import nan
import threading
import ujson, discord
from discord.ext import commands
from colorama import init as colorama_init, Fore, Back

colorama_init(False, True)

with open('token.txt') as tkf:
    tk = tkf.readline()

bt = commands.Bot(command_prefix='!', intents=discord.Intents.all(), self_bot=True)

title = f"""
{Back.LIGHTMAGENTA_EX}# DUMPALL #{Back.RESET}
{Fore.LIGHTMAGENTA_EX}Simple Discord group dumper/restorer for selfbots.{Fore.RESET}
#{Fore.RED}u{Fore.YELLOW}i{Fore.LIGHTYELLOW_EX}r{Fore.GREEN}-{Fore.LIGHTBLUE_EX}u{Fore.BLUE}i{Fore.MAGENTA}b{Fore.RESET}
{Fore.LIGHTMAGENTA_EX}This project is in public domain.{Fore.RESET}"""

sep = f"{Fore.MAGENTA}]>{Fore.RESET}"
dab = "https://discord.com/api/v9"
hd = {"Authorization": tk}

def log(level: str, msg: str):
    level = level.upper()
    fmt = Fore.GREEN if level == "SUCCESS" else Fore.YELLOW if level == "WARN" else Fore.RED if level == "ERROR" else Fore.MAGENTA if level == "CRITICAL" else Fore.WHITE
    print(f"{fmt}{level}: {msg}{Fore.RESET}")

def tryint(int_to_parse):
    try: return int(int_to_parse)
    except ValueError: return nan

def show_help(args):
    """help <cmd> \t\t ]> Show help
    where: cmd is the command to help be shown (not required)"""
    if len(args) == 0:
        print(f"""
{Back.LIGHTMAGENTA_EX}# HELP #{Back.RESET}
{Fore.BLUE}Command/Args{Fore.RESET} \t\t\t {Fore.CYAN}Description{Fore.RESET}
dump <trg> <gid|new> <chid|new> {sep} Dumps group to guild channel and JSON file
restore <trg> <gid|new> <chid|new> {sep} Restores group from JSON file to guild channel
help <cmd> \t\t {sep} Show help
exit \t\t\t {sep} Quit
""")
    else:
        print(f"""
{Back.LIGHTMAGENTA_EX}# HELP #{Back.RESET}
{cmd_list[args[0]].__doc__}""")

async def check(args):
    tid, gid, chid = None, None, None
    tid = tryint(args[0])
    if tid == nan: return log("error", "Target group id is NaN")
    tch: discord.DMChannel = bt.get_channel(tid)
    if args[1].lower() == "new": gid = await bt.create_guild(name=f"DA-{tid}")
    else:
        gid = tryint(args[1])
        if gid == nan: log("error", "Target guild id is NaN or not equals 'new'")
        gid = bt.get_guild(gid)
    if args[2].lower() == "new": chid = gid.create_text_channel(f"DA-{tid}")
    else:
        chid = tryint(args[1])
        if chid == nan: return log("error", "Target channel id is NaN or not equals 'new'")
        chid = gid.get_channel(chid)
    return tch, gid, chid

async def dump(args):
    """dump <trg> <gid|new> <chid|new> ]> Dumps group to guild channel and JSON file
    where: trg is target group ID; gid is target guild ID or "new" to create new guild; chid is target guild channel ID or "new" to create new channel"""
    tch, gid, chid = await check(args)
    tid = tch.id
    if tch is None or gid is None or chid is None: return log('error', f'Dump stopped (something of it is None: target channel - {tch}; guild - {gid}; channel - {chid})')
    td = []
    async for msg in tch.history(after=tch.created_at):
        todump = {'id': msg.id, 'content': msg.content, 'author': msg.author, 'reference': msg.to_message_reference_dict(), 'attachments': [att.url for att in msg.attachments if await att.save(f"./{tid}/attachments/") > 0]}
        td.append(todump)
    ujson.dump(obj:=open(f'./{tid}/messages.json', 'w'), ensure_ascii=False); obj.close()
    await restore([str(tid), str(gid.id), str(chid.id)])

async def restore(args):
    """dump <trg> <gid|new> <chid|new> ]> Dumps group to guild channel and JSON file
    where: trg is target group JSON file ID; gid is target guild ID or "new" to create new guild; chid is target guild channel ID or "new" to create new channel"""
    tch, gid, chid = await check(args)
    tid = tch.id
    if tch is None or gid is None or chid is None: return log('error', f'Dump stopped (something of it is None: target channel - {tch}; guild - {gid}; channel - {chid})')

exit.__doc__ = f"""exit \t\t\t {sep} Quit"""
cmd_list = {
    "dump": dump,
    "restore": restore,
    "help": show_help,
    "exit": exit
}

def main():
    print(title)
    show_help([])
    while 1:
        cmd = input("> ")
        if cmd:
            cmd = cmd.split(" ")
            if cmd[0] not in cmd_list:
                log('warn', f"Unknown command '{cmd[0]}'")
                continue
            else:
                (asyncio.run(cmd_list[cmd[0]](cmd[1:])) if asyncio.coroutines.iscoroutine(cmd_list[cmd[0]]) else cmd_list[cmd[0]](cmd[1:])) if cmd[0] != "exit" else exit()

@bt.event
async def on_ready():
    thread = threading.Thread(target=main)
    thread.start()
    thread.join()

bt.run(tk)