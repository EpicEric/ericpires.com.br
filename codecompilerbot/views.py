import re
from django.core.exceptions import ObjectDoesNotExist
from telegrambot.models import Chat
from telegrambot.bot_views.generic import TemplateCommandView, ListDetailCommandView, \
    ListCommandView, DetailCommandView
from .models import Language, Code


class StartCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_start.txt"

class UnknownCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_unknown.txt"
    
    def get_context(self, bot, update, **kwargs):
        context = {} 
        try:
            unknown_command = re.search('^(\/\w+).*', update.message.text).group(1)
        except AttributeError:
            unknown_command = ''
        context['command'] = ' {}'.format(unknown_command) if unknown_command else ''
        return context


class LanguageListCommandView(ListCommandView):
    template_text = "codecompilerbot/command_language_list.txt"
    template_keyboard = "codecompilerbot/command_language_list_keyboard.txt"
    context_object_name = "languages"
    model = Language
    ordering = 'name'
    
    def get_context(self, bot, update, **kwargs):
        context = super(LanguageListCommandView, self).get_context(bot, update, **kwargs) or {}
        chat_id = update.message.chat.id
        try:
            context['current_language'] = Code.objects.get(chat__id=chat_id).language
        except ObjectDoesNotExist:
            context['current_language'] = None
        return context
    
class LanguageDetailCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_language_selected.txt"
    language = None

    def __init__(self, language):
        super(LanguageDetailCommandView, self).__init__()
        self.language = language

    def get_context(self, bot, update, **kwargs):
        context = {}
        chat_id = update.message.chat.id
        try:
            language = Language.objects.get(shortname=self.language)
            context['current_language'] = language
        except ObjectDoesNotExist:
            context['current_language'] = None
            return context
        code_set = Code.objects.filter(chat__id=chat_id)
        if code_set.filter(language__id=language.id).exists():
            code_text = code_set[0].code
            code_stdin = code_set[0].stdin
        else:
            code_text = ''
            code_stdin = ''
        code = Code.objects.update_or_create(
            chat__id=chat_id,
            defaults={'chat': Chat.objects.get(id=chat_id), 'language': language, 'code': code_text, 'stdin': code_stdin},
        )

class LanguageCommandView(ListDetailCommandView):
    list_view_class = LanguageListCommandView
    detail_view_class = LanguageDetailCommandView

