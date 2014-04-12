import os
import urllib

import sublime, sublime_plugin

class CodeShareCommand(sublime_plugin.TextCommand):

    def getCode(self):
        sep = '\n\n# ' + '='*77 + '\n\n'
        code = sep.join( [self.view.substr(selection) for selection in self.view.sel() if not selection.empty()] )
        if not code:
            code = self.view.substr(sublime.Region(0, self.view.size()))
        return code

    def pasteCode(self, URL, requestData):
        data = urllib.parse.urlencode(requestData).encode('utf8')
        response = urllib.request.urlopen( URL, data )
        return response

    def parseUrl(self, response):
        return response.read().decode('utf8')[1:-1]

class CodeShareDpastedeCommand(CodeShareCommand):

    def run(self, edit):
        pasteApiUrl = 'http://dpaste.de/api/'
        code = self.getCode()
        requestData = { 'content': code }
        HttpResponse = self.pasteCode(pasteApiUrl, requestData)
        paste_url = self.parseUrl(HttpResponse)

        if paste_url:
            sublime.set_clipboard(paste_url)
            sublime.status_message('dpaste url ready to be pasted!')
        else:
            sublime.status_message('Something went wrong!')

        return
