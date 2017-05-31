import re
import requests
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from telegrambot.models import Chat
from telegrambot.bot_views.generic import TemplateCommandView, ListDetailCommandView, \
    ListCommandView, DetailCommandView
from .models import Language, Code


# /start: Show basic help and commands
class StartCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_start.txt"

    def get_context(self, bot, update, **kwargs):
        context = {}
        context['command'] = ''
        chat_id = update.message.chat.id
        try:
            context['current_language'] = Code.objects.get(chat__id=chat_id).language
        except ObjectDoesNotExist:
            context['current_language'] = None
        return context

# /?????: Display unknown command error message
class UnknownCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_unknown.txt"
    
    def get_context(self, bot, update, **kwargs):
        context = {} 
        try:
            unknown_command = re.search('^(\/\w+).*', update.message.text).group(1)
        except AttributeError:
            unknown_command = ''
        context['command'] = unknown_command.lower()
        return context

# /help: Show list of commands or detailed help on a specific one
class HelpCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_help.txt"
    
    def get_context(self, bot, update, **kwargs):
        context = {}
        try:
            command = re.search('^\s*/?(\w+).*', update.message.text[6:]).group(1)
            context['command'] = '/{}'.format(command.lower())
            help_dict = {
                'help': render_to_string('codecompilerbot/help/help.txt'), 
                'start': render_to_string('codecompilerbot/help/start.txt'),
                'reset': render_to_string('codecompilerbot/help/reset.txt'),
                'language': render_to_string('codecompilerbot/help/language.txt'),
                'code': render_to_string('codecompilerbot/help/code.txt'),
                'input': render_to_string('codecompilerbot/help/input.txt'),
                'run': render_to_string('codecompilerbot/help/run.txt'),
            }
            known_command = command in help_dict
            if known_command:
                context['command_desc'] = help_dict[command]
            else:
                context['command_desc'] = ''
        except AttributeError:
            context['command'] = ''
        return context

# /language: Display a list of languages for selection
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

# /language ?????: Select the provided language
class LanguageDetailCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_language_selected.txt"
    language = None

    def __init__(self, language):
        super(LanguageDetailCommandView, self).__init__()
        self.language = language.lower()

    def get_context(self, bot, update, **kwargs):
        context = {}
        chat_id = update.message.chat.id
        try:
            language = Language.objects.get(shortname=self.language)
            context['current_language'] = language
        except ObjectDoesNotExist:
            context['current_language'] = None
            return context
        try:
            code_set = Code.objects.filter(chat__id=chat_id).filter(language__id=language.id)
            if code_set.exists():
                code_text = code_set[0].code
                code_stdin = code_set[0].stdin
            else:
                code_text = ''
                code_stdin = ''
            code, created = Code.objects.update_or_create(
                chat__id=chat_id,
                defaults={'chat': Chat.objects.get(id=chat_id), 'language': language, 'code': code_text, 'stdin': code_stdin},
            )
            context['code'] = code
        except Exception:
            context['code'] = None
        return context

class LanguageCommandView(ListDetailCommandView):
    list_view_class = LanguageListCommandView
    detail_view_class = LanguageDetailCommandView

# /code: View current code or add new one
class CodeCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_code.txt"

    def get_context(self, bot, update, **kwargs):
        context = {}
        chat_id = update.message.chat.id
        try:
            code = Code.objects.get(chat__id=chat_id)
            if len(update.message.text) > 6:
                text_code = update.message.text[6:]
                default_code = bool(re.match('^\s*default', text_code))
                code.code = code.language.default_code if default_code else text_code
                code.save()
                context['default_code'] = default_code
                context['new_code'] = True
            context['has_code'] = len(code.code) > 0
            context['code'] = code
        except ObjectDoesNotExist:
            context['code'] = None
        return context

# /input: View current input or add new one
class InputCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_input.txt"

    def get_context(self, bot, update, **kwargs):
        context = {}
        chat_id = update.message.chat.id
        try:
            code = Code.objects.get(chat__id=chat_id)
            if len(update.message.text) > 7:
                code.stdin = update.message.text[7:]
                code.save()
                context['new_input'] = True
            context['has_input'] = len(code.stdin) > 0
            context['code'] = code
        except ObjectDoesNotExist:
            context['code'] = None
        return context

# /run: Code execution subroutine
class RunCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_run.txt"

    def get_context(self, bot, update, **kwargs):
        context = {}
        chat_id = update.message.chat.id
        try:
            code = Code.objects.get(chat__id=chat_id)
            context['code'] = code
            if len(code.code) > 0:
                context['has_code'] = True
                context['has_input'] = len(code.stdin) > 0
                
                try:
                    payload = {
                        'language': code.language.value,
                        'code': code.code,
                        'stdin': code.stdin if context['has_input'] else '',
                    }
                    url = "https://compile-public-low.remoteinterview.io/compile"
                    request = requests.post(url, data=payload)
                    response = request.json()
                    context['errors'] = response['errors']
                    context['output'] = response['output']
                    context['time'] = response['time']
                except (ConnectionError, HTTPError, requests.exceptions.RequestException) as e:
                    context['connection_error'] = e
 
        except ObjectDoesNotExist:
            context['code'] = None
        return context

# /reset: Allow removing user specific information
class ResetCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_reset.txt"

    def get_context(self, bot, update, **kwargs):
        context = {}
        confirm_reset = re.match('^/reset\s+yes', update.message.text)
        context['confirm_reset'] = confirm_reset
        if confirm_reset:
            chat_id = update.message.chat.id
            code = Code.objects.filter(chat__id=chat_id)
            code.delete()
        return context

