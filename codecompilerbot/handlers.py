from telegrambot.handlers import command, unknown_command, regex, message
from codecompilerbot.views import StartCommandView, UnknownCommandView

urlpatterns = [
    command('start', StartCommandView.as_command_view()),
    message(UnknownCommandView.as_command_view()),
]

bothandlers = urlpatterns
