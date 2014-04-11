import urllib

import sublime, sublime_plugin


def dpaste(code, lexer):
    dpasteUrl = 'http://dpaste.de/api/'

    data = urllib.parse.urlencode({
        'content': code,
        # 'lexer': lexer
    }).encode('utf8')

    response = urllib.request.urlopen( dpasteUrl, data )
    return response.read()[1:-1].decode('utf8')

class CodeShareDpasteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        code = self.view.substr(sublime.Region(0, self.view.size()))
        lexer = self.view.settings().get('syntax').split('/')[2].split('.')[0]

        dpaste_url = dpaste(code, lexer)

        sublime.set_clipboard(dpaste_url)
        sublime.status_message('dpaste url ready to be pasted!')

        return
