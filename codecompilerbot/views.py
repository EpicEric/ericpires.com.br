import re
import requests
from django.core.exceptions import ObjectDoesNotExist
from telegrambot.models import Chat
from telegrambot.bot_views.generic import TemplateCommandView, ListDetailCommandView, \
    ListCommandView, DetailCommandView
from .models import Language, Code


class StartCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_start.txt"

class HelpCommandView(TemplateCommandView):
    template_text = "codecompilerbot/command_help.txt"

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
