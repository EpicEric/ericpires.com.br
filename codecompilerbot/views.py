from telegrambot.bot_views.generic import TemplateCommandView, ListDetailCommandView, \
    ListCommandView, DetailCommandView

class StartCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_start.txt"

class UnknownCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_unknown.txt"
