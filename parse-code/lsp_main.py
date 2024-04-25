import subprocess
import json
import time
from threading import Thread

import os
from urllib.parse import urljoin, urlparse
from pathlib import Path


def convert_to_uri(root_uri, path):
    """
    Convert a potentially relative path to a full URI based on the root URI.

    :param root_uri: The root URI to which the path should be appended if relative.
    :param path: The path that needs to be converted to a URI.
    :return: A fully qualified URI.
    """
    # Normalize the root URI to ensure it ends with a slash
    if not root_uri.endswith('/'):
        root_uri += '/'

    # Check if the path is already a full URI or an absolute path
    if os.path.isabs(path) or urlparse(path).scheme:
        # It's an absolute path or a full URI, ensure it's a URI
        if not urlparse(path).scheme:
            # It's an absolute path but not a URI
            path = urljoin('file://', path)
        return path
    else:
        # It's a relative path, combine with root_uri
        # Use urljoin to intelligently concatenate paths
        full_uri = urljoin(root_uri, path)
        return full_uri


class LSPClient:

    def __init__(self, server_path, project_root):
        # convert paths to absolute paths
        server_path = str(Path(server_path).resolve())
        project_root = str(Path(project_root).resolve())

        self.process = subprocess.Popen([
            "java",
            "-Declipse.application=org.eclipse.jdt.ls.core.id1",
            "-Dosgi.bundles.defaultStartLevel=4",
            "-Declipse.product=org.eclipse.jdt.ls.core.product",
            "-Dlog.level=ALL",
            "-noverify",
            "-Xmx1G",
            "-jar", f"{server_path}/plugins/org.eclipse.equinox.launcher_1.6.600.v20231106-1826.jar",
            "-configuration", f"{server_path}/config_linux",
            "-data", project_root,
            "--add-modules=ALL-SYSTEM",
            "--add-opens", "java.base/java.util=ALL-UNNAMED",
            "--add-opens", "java.base/java.lang=ALL-UNNAMED"
        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.alive = True
        self.thread = Thread(target=self.read_messages)
        self.thread.start()

        self.root_uri = "file://" + project_root
        self.diagnostics = []
        self.symbols = []
        self.foldings = []
        self.read_handlers = {}
        self.responses = {}

        self.message_id = 0

        self.initialize()

    def read_response(self, message_id):
        timeout = 10
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            if response := self.responses.get(message_id):
                return response
            time.sleep(0.5)
        return None

    def send_message(self, method, params, handler=None):
        self.message_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.message_id,
            "method": method,
            "params": params
        }
        request_json = json.dumps(request)
        content_length = len(request_json.encode('utf-8'))
        full_message = f"Content-Length: {content_length}\r\n\r\n{request_json}"

        self.read_handlers[self.message_id] = handler

        self.process.stdin.write(full_message.encode('utf-8'))
        self.process.stdin.flush()

        return self.read_response(self.message_id)

    def read_messages(self):
        while self.alive:
            content_length = 0
            header = self.process.stdout.readline().decode('utf-8').strip()
            if header.startswith('Content-Length'):
                content_length = int(header.split(':')[1].strip())
            self.process.stdout.readline()
            if content_length:
                message_raw = self.process.stdout.read(
                    content_length).decode('utf-8')
                message = json.loads(message_raw)
                self.handle_message(message)

    def handle_message(self, message):
        open("response.jsonl", "a").write(json.dumps(message, indent=4))

        if "method" in message and message["method"] == "textDocument/publishDiagnostics":
            self.handle_diagnostics(message["params"]["diagnostics"])
        elif "id" in message:
            if "error" in message:
                self.responses[message["id"]] = None
            elif "result" in message:
                response = None
                if read_handler := self.read_handlers.get(message["id"]):
                    response = read_handler(message["result"])
                else:
                    response = message["result"]
                self.responses[message["id"]] = response

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.alive = False
        time.sleep(5)
        self.process.kill()

    def handle_diagnostics(self, diagnostics):
        self.diagnostics.extend(diagnostics)

    def handle_document_symbols(self, symbols):

        functions = []
        for symbol in symbols:
            if symbol["kind"] == 6:
                functions.append(symbol)

        self.symbols.extend(symbols)

        return functions

    def handle_folding_ranges(self, foldings):
        self.foldings.extend(foldings)
        return foldings

    def start(self):
        thread = Thread(target=self.read_messages)
        thread.start()
        return thread

    def initialize(self):
        self.send_message("initialize", {
            "processId": None,
            "rootUri": self.root_uri,
            "capabilities": {}
        })
        time.sleep(2)  # Wait for server to initialize

    def open_document(self, document_path):
        document_path = convert_to_uri(self.root_uri, document_path)
        text = open(Path(document_path.replace("file://", ""))).read()

        self.send_message("textDocument/didOpen", {
            "textDocument": {
                "uri": document_path,
                "languageId": "java",
                "version": 1,
                "text": text
            }
        })

    def request_document_symbols(self, document_path):
        document_path = convert_to_uri(self.root_uri, document_path)
        return self.send_message("textDocument/documentSymbol", {
            "textDocument": {"uri": document_path}
        }, self.handle_document_symbols)

    def request_code_folding(self, document_path):
        document_path = convert_to_uri(self.root_uri, document_path)
        return self.send_message("textDocument/foldingRange", {
            "textDocument": {"uri": document_path}
        }, self.handle_folding_ranges)

    def request_call_hierarchy(self, document_path, position):
        document_path = convert_to_uri(self.root_uri, document_path)
        return self.send_message("textDocument/prepareCallHierarchy", {
            "textDocument": {"uri": document_path},
            "position": position
        })

        # self.send_message("callHierarchy/incomingCalls", {
        #     "item": {
        #         "name": "wrapProcessorInInterceptors(RouteContext, Processor) : Processor",
        #         "detail": "org.apache.camel.model.ProcessorType",
        #         "kind": 6,
        #         "uri": "file:///home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse-code/fold/ori.java",
        #         "range": {
        #             "start": {
        #                 "line": 1522,
        #                 "character": 4
        #             },
        #             "end": {
        #                 "line": 1573,
        #                 "character": 5
        #             }
        #         },
        #         "selectionRange": {
        #             "start": {
        #                 "line": 1530,
        #                 "character": 24
        #             },
        #             "end": {
        #                 "line": 1530,
        #                 "character": 51
        #             }
        #         }
        #     }
        # }, 6)

        # self.send_message("callHierarchy/outgoingCalls", {
        #     "item": {
        #         "name": "wrapProcessorInInterceptors(RouteContext, Processor) : Processor",
        #         "detail": "org.apache.camel.model.ProcessorType",
        #         "kind": 6,
        #         "uri": "file:///home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse-code/fold/ori.java",
        #         "range": {
        #             "start": {
        #                 "line": 1522,
        #                 "character": 4
        #             },
        #             "end": {
        #                 "line": 1573,
        #                 "character": 5
        #             }
        #         },
        #         "selectionRange": {
        #             "start": {
        #                 "line": 1530,
        #                 "character": 24
        #             },
        #             "end": {
        #                 "line": 1530,
        #                 "character": 51
        #             }
        #         }
        #     }
        # }, 7)

    def get_function_blocks(self, document_path):
        document_path = convert_to_uri(self.root_uri, document_path)
        self.open_document(document_path)
        funcs = self.request_document_symbols(document_path)
        print(funcs)


if __name__ == "__main__":

    open("response.jsonl", "w").close()
    open("error.jsonl", "w").close()

    lsp_server_path = "/home/ferrero/files/Downloads/eclipse.jdt.ls-1.30.1/org.eclipse.jdt.ls.product/target/repository"
    root_uri = "./"
    with LSPClient(lsp_server_path, root_uri) as client:
        client.get_function_blocks("ori.java")
