from telegrambot.handlers import command, unknown_command
from codecompilerbot.views import StartCommandView, UnknownCommandView

urlpatterns = [
    command('start', StartCommandView.as_command_view()),
    unknown_command(UnknownCommandView.as_command_view()),
]

bothandlers = urlpatterns
