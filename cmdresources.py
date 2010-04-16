from twisted.internet import protocol
from twisted.internet import reactor
from twisted.web import resource
from twisted.web.server import NOT_DONE_YET
import re
import cgi

class ShellHTTP(protocol.ProcessProtocol):
    def __init__(self, request):
        self.request = request
        self.data = ""
        self.css = "<style>body pre {margin: 10px; padding-top: 10px; font-family: 'Monaco', 'Deja Vu Sans Mono', 'Inconsolata' ,'Consolas',monospace; background:#111 none repeat scroll 0 0; color:#fff; font-size:10px;}</style>"
    def connectionMade(self):
        print "connectionMade!"
    def outReceived(self, data):
        # Write stdout data from process to HTTP request
        self.request.write(data)
    def errReceived(self, data):
        print "errReceived! with %d bytes!" % len(data)
    def inConnectionLost(self):
        print "inConnectionLost! stdin is closed! (we probably did it)"
    def outConnectionLost(self):
        print "outConnectionLost! The child closed their stdout!"
        self.request.write('\nDone\n')
        self.request.finish()
    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."
    def processExited(self, reason):
        print "processExited, status %d" % (reason.value.exitCode,)
    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"

class ShellResource(resource.Resource):
    def _responseFailed(self, err, process):
        process.signalProcess('KILL')

    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        cmd = cgi.escape(request.args["tool"][0])
        filename = cgi.escape(request.args["file"][0])
        term = cgi.escape(request.args["term"][0])
        shell = ShellHTTP(request)

        if cmd == 'tail':
           process = reactor.spawnProcess(shell, "tail", ["tail", "-f", filename], {})
        if cmd == 'grep':
           process = reactor.spawnProcess(shell, "grep", ["grep", term, filename], {})

        request.notifyFinish().addErrback(self._responseFailed, process)
        return NOT_DONE_YET

class Root(resource.Resource):
    def __init__(self, wsgi_resource):
        resource.Resource.__init__(self)
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource
