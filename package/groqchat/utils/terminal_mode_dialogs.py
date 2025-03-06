from groqchat import config
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import radiolist_dialog, checkboxlist_dialog


class TerminalModeDialogs:

    def __init__(self, parent) -> None:
        self.parent = parent

    def getValidOptions(
        self,
        options=[],
        descriptions=[],
        bold_descriptions=False,
        filter="",
        default="",
        title="Available Options",
        text="Select an option:",
    ):
        if not options:
            return ""
        filter = filter.strip().lower()
        if descriptions:
            descriptionslower = [i.lower() for i in descriptions]
            values = [
                (
                    option,
                    (
                        HTML(f"<b>{descriptions[index]}</b>")
                        if bold_descriptions
                        else descriptions[index]
                    ),
                )
                for index, option in enumerate(options)
                if (filter in option.lower() or filter in descriptionslower[index])
            ]
        else:
            values = [
                (option, option) for option in options if filter in option.lower()
            ]
        if not values:
            if descriptions:
                values = [
                    (
                        option,
                        (
                            HTML(f"<b>{descriptions[index]}</b>")
                            if bold_descriptions
                            else descriptions[index]
                        ),
                    )
                    for index, option in enumerate(options)
                ]
            else:
                values = [(option, option) for option in options]
        result = radiolist_dialog(
            title=title,
            text=text,
            values=values,
            default=default if default and default in options else values[0][0],
        ).run()
        if result:
            notice = f"You've chosen: {result}"
            splittedContent = notice.split(": ", 1)
            key, value = splittedContent
            print_formatted_text(
                HTML(
                    f"<{config.terminalPromptIndicatorColor2}>{key}:</{config.terminalPromptIndicatorColor2}> {value}"
                )
            )
            return result
        return ""

    def displayFeatureMenu(self, heading, features):
        values = [
            (
                command,
                (
                    command
                    if config.terminalDisplayCommandOnMenu
                    else self.parent.dotCommands[command][0]
                ),
            )
            for command in features
        ]
        result = radiolist_dialog(
            title=heading,
            text="Select a feature:",
            values=values,
            default=features[0],
        ).run()
        if result:
            self.parent.printRunningCommand(result)
            return self.parent.getContent(result)
        else:
            return self.parent.exitAction()
            # return ""

    def getMultipleSelection(
        self,
        title="Multiple Selection",
        text="Select item(s):",
        options=["ALL"],
        descriptions=[],
        default_values=["ALL"],
    ):
        if descriptions:
            values = [
                (option, descriptions[index]) for index, option in enumerate(options)
            ]
        else:
            values = [(option, option) for option in options]
        return checkboxlist_dialog(
            title=title,
            text=text,
            values=values,
            default_values=default_values,
        ).run()
