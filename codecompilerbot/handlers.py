from telegrambot.handlers import command, unknown_command, regex, message
from codecompilerbot.views import StartCommandView, UnknownCommandView, \
    LanguageCommandView, CodeCommandView, InputCommandView, RunCommandView, \
    HelpCommandView, ResetCommandView

urlpatterns = [
    command('start', StartCommandView.as_command_view()),
    command('language', LanguageCommandView.as_command_view()),
    command('code', CodeCommandView.as_command_view()),
    command('input', InputCommandView.as_command_view()),
    command('run', RunCommandView.as_command_view()),
    command('help', HelpCommandView.as_command_view()),
    command('reset', ResetCommandView.as_command_view()),
    message(UnknownCommandView.as_command_view()),
]

bothandlers = urlpatterns
