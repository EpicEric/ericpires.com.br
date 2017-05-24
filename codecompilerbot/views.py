import re
from telegrambot.bot_views.generic import TemplateCommandView, ListDetailCommandView, \
    ListCommandView, DetailCommandView


class StartCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_start.txt"

class UnknownCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_unknown.txt"
    
    def get_context(self, bot, update, **kwargs):
        try:
            unknown_command = re.search('^(\/\w+).*', update.message.text).group(1)
        except AttributeError:
            unknown_command = ''
        context = {
            'command': ' {}'.format(unknown_command) if unknown_command else ''
        }
        return context
