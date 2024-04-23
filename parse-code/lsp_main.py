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

        self.thread = Thread(target=self.read_messages)
        self.thread.start()

        self.root_uri = "file://" + project_root
        self.diagnostics = []
        self.symbols = []
        self.foldings = []

        self.initialize()

    def send_message(self, request):
        request_json = json.dumps(request)
        content_length = len(request_json.encode('utf-8'))
        full_message = f"Content-Length: {content_length}\r\n\r\n{request_json}"
        self.process.stdin.write(full_message.encode('utf-8'))
        self.process.stdin.flush()

    def send_message(self, method, params, message_id):
        request = {
            "jsonrpc": "2.0",
            "id": message_id,
            "method": method,
            "params": params
        }
        request_json = json.dumps(request)
        content_length = len(request_json.encode('utf-8'))
        full_message = f"Content-Length: {content_length}\r\n\r\n{request_json}"
        self.process.stdin.write(full_message.encode('utf-8'))
        self.process.stdin.flush()

    def read_messages(self):
        while True:
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
        if "method" in message and message["method"] == "textDocument/publishDiagnostics":
            self.handle_diagnostics(message["params"]["diagnostics"])
        elif "result" in message and "id" in message:
            if message["id"] == 3:  # Assuming ID 3 is used for documentSymbol and foldingRange requests
                self.handle_document_symbols(message["result"])
            elif message["id"] == 4:  # Assuming ID 4 is used for foldingRange requests
                self.handle_folding_ranges(message["result"])
            else:
                open("response.jsonl", "a").write(
                    json.dumps(message, indent=4))
        else:
            open("error.jsonl", "a").write(json.dumps(message, indent=4))

    def handle_diagnostics(self, diagnostics):
        self.diagnostics.extend(diagnostics)

    def handle_document_symbols(self, symbols):
        self.symbols.extend(symbols)

    def handle_folding_ranges(self, foldings):
        self.foldings.extend(foldings)

    def start(self):
        thread = Thread(target=self.read_messages)
        thread.start()
        return thread

    def initialize(self):
        self.send_message("initialize", {
            "processId": None,
            "rootUri": self.root_uri,
            "capabilities": {}
        }, 1)
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
        }, 2)

    def request_document_symbols(self, document_path):
        document_path = convert_to_uri(self.root_uri, document_path)
        self.send_message("textDocument/documentSymbol", {
            "textDocument": {"uri": document_path}
        }, 3)

    def request_code_folding(self, document_path):
        document_path = convert_to_uri(self.root_uri, document_path)
        self.send_message("textDocument/foldingRange", {
            "textDocument": {"uri": document_path}
        }, 4)

    def request_call_hierarchy(self, document_path, position):
        document_path = convert_to_uri(self.root_uri, document_path)
        self.send_message("textDocument/prepareCallHierarchy", {
            "textDocument": {"uri": document_path},
            "position": position
        }, 5)

        self.send_message("callHierarchy/incomingCalls", {
            "item": {
                "name": "wrapProcessorInInterceptors(RouteContext, Processor) : Processor",
                "detail": "org.apache.camel.model.ProcessorType",
                "kind": 6,
                "uri": "file:///home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse-code/fold/ori.java",
                "range": {
                    "start": {
                        "line": 1522,
                        "character": 4
                    },
                    "end": {
                        "line": 1573,
                        "character": 5
                    }
                },
                "selectionRange": {
                    "start": {
                        "line": 1530,
                        "character": 24
                    },
                    "end": {
                        "line": 1530,
                        "character": 51
                    }
                }
            }
        }, 6)

        self.send_message("callHierarchy/outgoingCalls", {
            "item": {
                "name": "wrapProcessorInInterceptors(RouteContext, Processor) : Processor",
                "detail": "org.apache.camel.model.ProcessorType",
                "kind": 6,
                "uri": "file:///home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse-code/fold/ori.java",
                "range": {
                    "start": {
                        "line": 1522,
                        "character": 4
                    },
                    "end": {
                        "line": 1573,
                        "character": 5
                    }
                },
                "selectionRange": {
                    "start": {
                        "line": 1530,
                        "character": 24
                    },
                    "end": {
                        "line": 1530,
                        "character": 51
                    }
                }
            }
        }, 7)


if __name__ == "__main__":

    open("response.jsonl", "w").close()
    open("error.jsonl", "w").close()

    lsp_server_path = "/home/ferrero/files/Downloads/eclipse.jdt.ls-1.30.1/org.eclipse.jdt.ls.product/target/repository"
    root_uri = "fold"
    client = LSPClient(lsp_server_path, root_uri)

    client.open_document("ori.java")
    client.request_document_symbols("ori.java")
    client.request_code_folding("ori.java")

    time.sleep(5)  # Allow time for responses

    print('-'*100)
    print("Diagnostics:", client.diagnostics)
    print('-'*100)
    print("Foldings:", client.foldings)
    print('-'*100)
    print("Symbols:", client.symbols)
    print('-'*100)

    print('-'*100)

    client.request_call_hierarchy("ori.java", {"line": 109, "character": 20})
