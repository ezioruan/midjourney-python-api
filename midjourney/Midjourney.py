import traceback

import discum
from discum.utils.button import Buttoner
from discum.utils.slash import SlashCommander
import threading


class MidjourneyClient:
    def __init__(
        self,
        name,
        token,
        application_id,
        guild_id,
        channel_id,
        message_handler=None,
    ):
        self.name = name
        self.token = token
        self.application_id = application_id
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.no_received_times = 0

        if not message_handler:
            self.message_handler = print
        else:
            self.message_handler = message_handler

    def run(self, log=False):
        self.bot = discum.Client(token=self.token, log=log)
        self.slash_cmds = None
        self.add_message_hooks_if_needed()
        # run the client in thread so it doesn't block
        client_thread = threading.Thread(target=self.bot.gateway.run)
        client_thread.start()

    def re_run(self):
        self.bot.gateway.close()
        self.bot.gateway._after_message_hooks = []
        self.run()

    def __str__(self):
        return f"<MidjouneryClient {self.name}> {self.channel_id}  "

    def subscribeToGuildEvents(self):
        try:
            self.bot.gateway.subscribeToGuildEvents(wait=1)
        except KeyError as e:
            pass
        except Exception as e:
            traceback.print_exc()

    def set_slash_cmds(self):
        if not self.slash_cmds:
            self.slash_cmds = {
                c["name"]: c
                for c in self.bot.getSlashCommands(self.application_id).json()
            }

    def get_slash_cmd(self, cmd_name):
        if not self.slash_cmds:
            self.set_slash_cmds()
        return self.slash_cmds.get(cmd_name)

    def add_message_hooks_if_needed(self):
        if not self.bot.gateway._after_message_hooks:
            self.bot.gateway.command(self.process_message)

    def execute_slash_cmd(self, cmd_name, inputs={}):
        slash_cmd = self.get_slash_cmd(cmd_name)
        s = SlashCommander(slash_cmd, application_id=self.application_id)
        data = s.get([cmd_name], inputs=inputs)
        self.add_message_hooks_if_needed()
        result = self.bot.triggerSlashCommand(
            applicationID=self.application_id,
            channelID=self.channel_id,
            guildID=self.guild_id,
            data=data,
        )

    def imagine(self, prompt):
        cmd_name = "imagine"
        inputs = {"prompt": prompt}
        self.execute_slash_cmd(cmd_name, inputs=inputs)

    def info(self):
        cmd_name = "info"
        inputs = {}
        self.execute_slash_cmd(cmd_name, inputs=inputs)

    def interact(self, message_id, label):
        message = self.bot.getMessage(self.channel_id, message_id)
        if not message:
            return
        data = message.json()[0]
        buttons = Buttoner(data["components"])
        result = self.bot.click(
            data["author"]["id"],
            channelID=data["channel_id"],
            guildID=self.guild_id,
            messageID=data["id"],
            messageFlags=data["flags"],
            sessionID=self.bot.gateway.session_id,
            data=buttons.getButton(label),
        )

    def process_message(self, resp):
        if resp.raw["op"] == 11 and not self.bot.gateway.READY:
            self.no_received_times += 1
            print(
                "op code 11 received by discord > ",
                resp.raw,
                self.no_received_times,
            )
            if self.no_received_times >= 3:
                print("op code 11 received 3 times, message idle, re_run")
                self.re_run()
            return
        if (
            resp.event.ready_supplemental
        ):  # ready_supplemental is sent after ready
            user = self.bot.gateway.session.user
            print(
                "Logged in as {}#{}".format(
                    user.get("username"), user.get("discriminator")
                )
            )
            self.subscribeToGuildEvents()

        if resp.event.message or resp.event.message_updated:
            message = resp.parsed.auto()
            self.message_handler(message)
