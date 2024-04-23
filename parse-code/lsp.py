import os
import subprocess
import json
import time

from threading import Thread


def send_message(process, request):
    request_json = json.dumps(request)
    content_length = len(request_json.encode('utf-8'))
    full_message = f"Content-Length: {content_length}\r\n\r\n{request_json}"
    process.stdin.write(full_message.encode('utf-8'))
    process.stdin.flush()


def read_messages(process):
    while True:
        content_length = 0
        # Read the Content-Length header
        header = process.stdout.readline().decode('utf-8').strip()
        if header.startswith('Content-Length'):
            content_length = int(header.split(':')[1].strip())
        # Read the following blank line
        process.stdout.readline()
        # Read the actual message content
        if content_length:
            message_raw = process.stdout.read(content_length).decode('utf-8')
            message = json.loads(message_raw)
            if message.get("method") == "textDocument/publishDiagnostics":
                handle_diagnostics(message["params"]["diagnostics"])
            elif message.get("id") == 3:  # Assuming ID 3 is for documentSymbol request
                print(message)
                handle_document_symbols(message["result"])


def handle_diagnostics(diagnostics):
    for diagnostic in diagnostics:
        print(f"Problem: {diagnostic['message']} at {diagnostic['range']}")


def handle_document_symbols(symbols):
    for symbol in symbols:
        if symbol['kind'] == 6:  # Symbol kind 6 is for Function
            print(
                f"Method: {symbol['name']} at range {symbol['location']['range']}")
        else:  # Symbol kind 13 is for Variable
            print(
                f"Variable: {symbol['name']} at range {symbol['location']['range']}")


command = [
    "java",
    "-Declipse.application=org.eclipse.jdt.ls.core.id1",
    "-Dosgi.bundles.defaultStartLevel=4",
    "-Declipse.product=org.eclipse.jdt.ls.core.product",
    "-Dlog.level=ALL",
    "-noverify",
    "-Xmx1G",
    "-jar", "/home/ferrero/files/Downloads/eclipse.jdt.ls-1.30.1/org.eclipse.jdt.ls.product/target/repository/plugins/org.eclipse.equinox.launcher_1.6.600.v20231106-1826.jar",
    "-configuration", "/home/ferrero/files/Downloads/eclipse.jdt.ls-1.30.1/org.eclipse.jdt.ls.product/target/repository/config_linux",
    "-data", "./fold",
    "--add-modules=ALL-SYSTEM",
    "--add-opens", "java.base/java.util=ALL-UNNAMED",
    "--add-opens", "java.base/java.lang=ALL-UNNAMED"
]
process = subprocess.Popen(
    command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

t = Thread(target=read_messages, args=(process,))
t.start()

# Send the initialize request
initialize_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "processId": None,
        "rootUri": "file:///home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse-code/fold",
        "capabilities": {}
    }
}
send_message(process, initialize_request)

# Wait for the server to be ready
time.sleep(2)

# Send the didOpen notification
did_open_notification = {
    "jsonrpc": "2.0",
    "method": "textDocument/didOpen",
    "params": {
        "textDocument": {
            "uri": "file:///home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse-code/fold/code.java",
            "languageId": "java",
            "version": 1,
            "text": open("fold/code.java").read()
        }
    }
}
send_message(process, did_open_notification)

time.sleep(5)

document_symbol_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "textDocument/documentSymbol",
    "params": {
        "textDocument": {
            "uri": "file:///home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse-code/fold/code.java"
        }
    }
}
send_message(process, document_symbol_request)

time.sleep(5)

code_folding_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "textDocument/foldingRange",
    "params": {
        "textDocument": {
            "uri": "file:///home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse-code/fold/code.java"
        }
    }
}

send_message(process, code_folding_request)

time.sleep(500)
exit(0)


# Start the server
command = [
    "java", "-jar", "/home/ferrero/files/Downloads/eclipse.jdt.ls-1.30.1/org.eclipse.jdt.ls.product/target/repository/plugins/org.eclipse.equinox.launcher_1.6.600.v20231106-1826.jar",
    "-configuration", "/home/ferrero/files/Downloads/eclipse.jdt.ls-1.30.1/org.eclipse.jdt.ls.product/target/repository/config_linux",
    "-data", "./fold"
]
process = subprocess.Popen(
    command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Prepare the initialize request
initialize_request = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "processId": None,
        "rootUri": "file:///home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse\ code/fold",
        "capabilities": {},
    }
})
length = len(initialize_request)
full_message = f"Content-Length: {length}\r\n\r\n{initialize_request}"

# Send the initialize request
process.stdin.write(full_message.encode('utf-8'))
process.stdin.flush()

# Read response
output = process.stdout.readline()
print(output.decode('utf-8'))


exit(0)


def start_lsp_server():
    command = [
        "java",
        "-Declipse.application=org.eclipse.jdt.ls.core.id1",
        "-Dosgi.bundles.defaultStartLevel=4",
        "-Declipse.product=org.eclipse.jdt.ls.core.product",
        "-Dlog.level=ALL",
        "-noverify",
        "-Xmx1G",
        "-jar", "/home/ferrero/files/Downloads/eclipse.jdt.ls-1.30.1/org.eclipse.jdt.ls.product/target/repository/plugins/org.eclipse.equinox.launcher_1.6.600.v20231106-1826.jar",
        "-configuration", "/home/ferrero/files/Downloads/eclipse.jdt.ls-1.30.1/org.eclipse.jdt.ls.product/target/repository/config_linux",
        "-data", input("Enter the path to the workspace: "),
        "--add-modules=ALL-SYSTEM",
        "--add-opens", "java.base/java.util=ALL-UNNAMED",
        "--add-opens", "java.base/java.lang=ALL-UNNAMED"
    ]
    print(command)
    process = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # output, error = process.communicate()
    # print(output, error)
    return process


def send_lsp_request(process, request):
    # Sending a JSON RPC request to the LSP server
    json_rpc = json.dumps(request).encode('utf-8')
    process.stdin.write(json_rpc + b'\n')
    process.stdin.flush()


def read_lsp_response(process):
    # Reading the response from the LSP server
    response = process.stdout.readline()
    print(response)
    return response


# Example usage
lsp_process = start_lsp_server()

# Wait for the server to be ready, handling initial handshake or setup messages as necessary
initialize_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "processId": os.getpid(),
        "rootUri": "file:///home/mtp/trying",
        "capabilities": {},  # Specify client capabilities here
    }
}
send_lsp_request(lsp_process, initialize_request)
response = read_lsp_response(lsp_process)
print("Initialization response:", response)

initialized_notification = {
    "jsonrpc": "2.0",
    "method": "initialized",
    "params": {}
}
send_lsp_request(lsp_process, initialized_notification)

did_open_notification = {
    "jsonrpc": "2.0",
    "method": "textDocument/didOpen",
    "params": {
        "textDocument": {
            "uri": "file:///home/mtp/trying/code.java",
            "languageId": "java",
            "version": 1,
            "text": open("code.java").read()
        }
    }
}
send_lsp_request(lsp_process, did_open_notification)
