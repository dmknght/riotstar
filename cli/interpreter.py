# https://github.com/threat9/routersploit/blob/master/routersploit/interpreter.py
# Modified by Nong Hoang "DmKnght" Tu for new RiotStar
"""
Copyright 2018, The RouterSploit Framework (RSF) by Threat9
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the
    following disclaimer. * Redistributions in binary form must reproduce the above copyright notice, this list of
    conditions and the following disclaimer in the documentation and/or other materials provided with the
    distribution. * Neither the name of RouterSploit Framework nor the names of its contributors may be used to
    endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The above licensing was taken from the BSD licensing and is applied to RouterSploit Framework as well.

Note that the RouterSploit Framework is provided as is, and is a royalty free open-source application.

Feel free to modify, use, change, market, do whatever you want with it as long as you give the appropriate credit.
"""
import readline
from cli.print_utils import *
from cores.docker_utils import DockerClient


class BaseInterpreter(object):
    global_help = ""

    def __init__(self):
        self.setup()
        self.banner = ""

    def refresh(self):
        pass

    def setup(self):
        """ Initialization of third-party libraries

        Setting interpreter history.
        Setting appropriate completer function.

        :return:
        """
        readline.parse_and_bind("set enable-keypad on")
        readline.set_completer(self.complete)
        readline.set_completer_delims(" \t\n;")
        readline.parse_and_bind("tab: complete")

    def parse_line(self, line):
        """ Split line into command and argument.

        :param line: line to parse
        :return: (command, argument)
        """
        command, _, arg = line.strip().partition(" ")
        return command, arg.strip()

    @property
    def prompt(self):
        """ Returns prompt string """
        return ">>>"

    def get_command_handler(self, command):
        """ Parsing command and returning appropriate handler.

        :param command: command
        :return: command_handler
        """
        try:
            command_handler = getattr(self, "command_{}".format(command))
        except AttributeError:
            raise AttributeError("Unknown command: '{}'".format(command))

        return command_handler

    def start(self):
        """ main entry point. Starting interpreter loop. """
        while True:
            import traceback
            try:
                command, args = self.parse_line(input(self.prompt))
                if not command:
                    self.refresh()
                if command == "exit" or command == "quit":
                    break
                command_handler = self.get_command_handler(command)
                command_handler(args)
                self.refresh()
            except KeyboardInterrupt:
                print("")
            except AttributeError:
                pass
            except:
                traceback.print_exc()
                pass

    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            original_line = readline.get_line_buffer()
            line = original_line.lstrip()
            stripped = len(original_line) - len(line)
            start_index = readline.get_begidx() - stripped
            end_index = readline.get_endidx() - stripped

            if start_index > 0:
                cmd, args = self.parse_line(line)
                if cmd == "":
                    complete_function = self.default_completer
                else:
                    try:
                        complete_function = getattr(self, "complete_" + cmd)
                    except AttributeError:
                        complete_function = self.default_completer
            else:
                complete_function = self.raw_command_completer

            self.completion_matches = complete_function(text, line, start_index, end_index)

        try:
            return self.completion_matches[state]
        except IndexError:
            return None

    def commands(self, *ignored):
        """ Returns full list of interpreter commands.

        :param ignored:
        :return: full list of interpreter commands
        """
        return [command.rsplit("_").pop() for command in dir(self) if command.startswith("command_")]

    def raw_command_completer(self, text, line, start_index, end_index):
        """ Complete command w/o any argument """
        return [command for command in self.suggested_commands() if command.startswith(text)]

    def default_completer(self, *ignored):
        return []

    def suggested_commands(self):
        """ Entry point for intelligent tab completion.

        Overwrite this method to suggest suitable commands.

        :return: list of suitable commands
        """
        return self.commands()


class Interpreter(BaseInterpreter):
    def __init__(self):
        super(Interpreter, self).__init__()
        self.raw_prompt_template = None
        self.module_prompt_template = None
        self.not_installed = ()
        self.installed = ()
        self.running = ()
        self.show_commands = (
            "all",
            "running",
            "installed",
        )
        self.main_commands = (
            ("show", "Show information about images / containers"),
            ("run", "Start docker containers"),
            ("kill", "Kill running docker containers"),
            ("killall", "Kill all running docker containers"),
            ("pull", "Pull images"),
            ("help", "Show help menu"),
            ("exit", "Exit program"),
        )
        self.manager = DockerClient()
        self.refresh()

    def refresh(self):
        self.running, self.installed, self.not_installed = (), (), ()
        for image in self.manager.get_images_status():
            if image.status == 0:
                self.running += (image, )
            elif image.status == 1:
                self.installed += (image, )
            else:
                self.not_installed += (image, )

    @property
    def prompt(self):
        """ Returns prompt string based on current_module attribute.
        Adding extras prefix (extras.name) if current_module attribute is set.
        :return: prompt string with appropriate extras prefix.
        """

        p = f"┌[Installed: {color('cyan')}{len(self.installed) + len(self.running)}{color('rs')}"
        p += f"]-[Running: {color('purple')}{len(self.running)}{color('rs')}]\n"
        p += f"└╼{color('lblue')}RiotStar{color('rs')}> "
        return p

    def command_help(self, *args, **kwargs):
        for command, descriptions in self.main_commands:
            print(f"  {command:15}  {descriptions}")

    def command_run(self, *args, **kwargs):
        if not args[0]:
            error("Image name is required to start")
        else:
            self.refresh()
            for name in args[0].split():
                repo = [image.repo for image in self.installed if image.name == name]
                if repo:
                    self.manager.run(repo[0])
                    # info("Containers created in background")
                    if self.manager.is_running(repo[0]):
                        info("Container started")
                    else:
                        error(f"Failed to start {name}")
                else:
                    if name in [x.name for x in self.running]:
                        warn(f"{name} is running")
                    elif name in [x.name for x in self.not_installed]:
                        warn(f"{name} is not installed. Pulling...")
                        self.command_pull(name)
                        # print("To prevent infinity loop, program doesn't run this image. Please do it manually.")
                        self.command_run(name)
                    else:
                        error(f"Invalid name {name}.")

    def command_kill(self, *args, **kwargs):
        if not args[0]:
            error("Container names are required to kill")
        else:
            for name in args[0].split():
                target_id = [x.id for x in self.running if x.name == name]
                if target_id:
                    self.manager.kill(target_id[0])
                else:
                    error(f"Invalid name {name} to kill")

    def command_killall(self, *args, **kwargs):
        for image in self.running:
            self.manager.kill(image.id)

    def command_pull(self, *args, **kwargs):
        if not args[0]:
            error("Image names are required to pull")
        else:
            for name in args[0].split():
                repo = [image.repo for image in self.not_installed if image.name == name]
                if repo:
                    info(f"Pulling {name} from {repo[0]}. Please wait...")
                    self.manager.pull(repo[0])
                else:
                    error(f"Invalid name {name}")

    def command_prune(self, *args, **kwargs):
        self.manager.prune()
        info("Completed")

    def command_remove(self, *args, **kwargs):
        if not args[0]:
            error("Image names are required to remove")
        else:
            for name in args[0].split():
                repo = [image.repo for image in self.installed if image.name == name]
                if repo:
                    self.manager.remove(repo[0])
                else:
                    error(f"Invalid name {name} to remove")

    def command_restart(self, *args, **kwargs):
        if not args[0]:
            error("Image name is required to restart")
        else:
            self.refresh()
            for name in args[0].split():
                repo = [image.repo for image in self.running if image.name == name]
                if repo:
                    result = self.manager.restart(repo[0])
                    if not result:
                        error(f"Failed to restart {name}")
                    else:
                        info("Containers restarted")
                else:
                    error(f"Invalid name {name}.")

    def _show_all(self):
        self.refresh()
        headers = ("Name", "Status", "Description")
        status_all = [(x.name, "Running", x.description) for x in self.running]
        status_all += [(x.name, "Stopped", x.description) for x in self.installed]
        status_all += [(x.name, "N/A", x.description) for x in self.not_installed]
        print_table(headers, *status_all)

    def _show_installed(self):
        self.refresh()
        if len(self.installed + self.running) == 0:
            warn("No images were installed")
        else:
            all_installed = [(x.name, x.description, "Stopped", x.size) for x in self.installed]
            all_installed += [(x.name, x.description, "Running", x.size) for x in self.running]
            headers = ("Name", "Description", "Status", "Size")
            print_table(headers, *all_installed)

    def _show_running(self):
        self.refresh()
        if len(self.running) == 0:
            warn("No containers is running")
        else:
            headers = ("Name", "ID", "IP", "Port", "Up time")
            print_table(headers, *[(x.name, x.id, x.ip, x.ports, x.uptime) for x in self.running])

    # def _show_status(self, *args, **kwargs):
    #     # show current status of an image
    #     pass

    def command_show(self, *args, **kwargs):
        sub_command = args[0]
        try:
            getattr(self, f"_show_{sub_command}")()
        except AttributeError:
            error(f"Unknown 'show' sub-command '{sub_command}'. What do you want to show?\n")

    def complete_show(self, text, *args, **kwargs):
        if text:
            return [command for command in self.show_commands if command.startswith(text)]
        else:
            return self.show_commands

    def complete_run(self, text, *args, **kwargs):
        suggestions = [x.name for x in self.installed]
        if text:
            return [command for command in suggestions if command.startswith(text)]
        else:
            return suggestions

    def complete_pull(self, text, *args, **kwargs):
        suggestions = [x.name for x in self.not_installed]
        if text:
            return [command for command in suggestions if command.startswith(text)]
        else:
            return suggestions

    def complete_kill(self, text, *args, **kwargs):
        suggestions = [x.name for x in self.running]
        if text:
            return [command for command in suggestions if command.startswith(text)]
        else:
            return suggestions

    def complete_remove(self, text, *args, **kwargs):
        suggestions = [x.name for x in self.installed]
        if text:
            return [command for command in suggestions if command.startswith(text)]
        else:
            return suggestions

    def complete_restart(self, text, *args, **kwargs):
        return self.complete_kill(text, *args, **kwargs)
