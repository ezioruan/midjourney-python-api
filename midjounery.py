import pprint
import traceback
import re

import discum
from discum.utils.button import Buttoner
from discum.utils.slash import SlashCommander

pp = pprint.PrettyPrinter(depth=4)


class MidjouneryClient:
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

    def run(self):
        self.bot = discum.Client(token=self.token, log=False)
        self.slash_cmds = None
        self.add_message_hooks_if_needed()
        self.bot.gateway.run(auto_reconnect=True)

    def re_run(self):
        print("re_run")
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

    def parse_process_message(self, message):
        print("parse_process_message", message)
        match_with_progress_and_mode = re.search(
            r"\*\*(.*)\*\* - <@(.*)> \((.*)\) \((.*)\)", message
        )
        match_without_progress_and_mode = re.search(
            r"\*\*(.*)\*\* - <@(.*)>", message
        )

        if match_with_progress_and_mode:
            prompt = match_with_progress_and_mode.group(1)
            user_id = match_with_progress_and_mode.group(2)
            progress = match_with_progress_and_mode.group(3)
            mode = match_with_progress_and_mode.group(4)
        elif match_without_progress_and_mode:
            prompt = match_without_progress_and_mode.group(1)
            user_id = match_without_progress_and_mode.group(2)
            progress = ""
            mode = ""
        else:
            prompt = ""
            user_id = ""
            progress = ""
            mode = ""

        return {
            "prompt": prompt,
            "progress": progress,
            "mode": mode,
        }

    def parse_settings(self, message):
        """
        parse message from Adjust your settings here. Current suffix: ` --s 750 --v 5.1`
        """
        match = re.search(r"`(.*?)`", text)
        if match:
            settings = match.group(1)
            self.settings = settings

    def parse_command_message(self, message):
        """
        parse message like this: /imagine A sex girl
        """
        print("parse_command_message", message)
        match = re.search(r"/(\w+)\s+(.*)", message)

        if match:
            command = match.group(1)
            prompt = match.group(2)
        else:
            command = ""
            prompt = ""

        return {
            "command": command,
            "prompt": prompt,
        }

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

    def settings(self):
        cmd_name = "settings"
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
            pprint.pprint(user)
            print(
                "Logged in as {}#{}".format(
                    user.get("username"), user.get("discriminator")
                )
            )
            self.subscribeToGuildEvents()
            self.info()
            self.settings()

        if resp.event.message or resp.event.message_updated:
            message = resp.parsed.auto()
            message_id = message.get("id")
            guild_id = message.get("guild_id")
            channel_id = message.get("channel_id")
            timestamp = message.get("timestamp")
            application_id = message.get("application_id")
            components = message.get("components")
            attachments = message.get("attachments")
            message_reference = message.get("message_reference")
            message_type = message.get("type")
            content = message.get("content")
            # 20: updated message
            if (
                message_type
                not in [
                    "application_command",
                    "reply",
                    0,
                    19,
                    20,
                    "default",
                ]
                or channel_id != self.channel_id
            ):
                # only parse message in current channel
                return
            pprint.pprint(message)

            if message_type == "20" and content.startswith(
                "Adjust your settings here.Current suffix:"
            ):
                # settings message
                self.parse_settings_message(content)

            result = {
                "message_id": message_id,
                "channel_id": channel_id,
                "guild_id": guild_id,
                "timestamp": timestamp,
                "application_id": application_id,
                "components": components,
                "attachments": attachments,
                "message_reference": message_reference,
                "message_type": str(message_type),
            }
            embeds = message.get("embeds", [{}])
            embed = embeds[0] if embeds else {}
            footer_text = embed.get("footer", {}).get("text")
            if message_type in ["application_command", 20] and footer_text:
                # bland message
                result["status"] = "failed"
                result["content"] = embed.get("description")
                result["prompt"] = self.parse_command_message(footer_text).get(
                    "prompt"
                )
                self.message_handler(message_id, result)
                return

            result.update(self.parse_process_message(content))
            result["status"] = "success"
            result["content"] = content
            self.message_handler(message_id, result)

    def handle_task(self, task):
        if task.get("channel_id") != self.channel_id:
            return
        cmd = task.get("cmd")
        args = task.get("args", [])
        method = getattr(self, cmd)
        try:
            method(*args)
        except Exception:
            traceback.print_exc()
