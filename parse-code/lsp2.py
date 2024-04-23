from monitors4codegen.multilspy import SyncLanguageServer
from monitors4codegen.multilspy.multilspy_config import MultilspyConfig
from monitors4codegen.multilspy.multilspy_logger import MultilspyLogger

# Also supports "python", "rust", "csharp"
config = MultilspyConfig.from_dict({"code_language": "java"})
logger = MultilspyLogger()
lsp = SyncLanguageServer.create(
    config, logger, "/home/ferrero/Desktop/Projects/Academic/Software-Fault-Prediction/parse-code/fold")

with lsp.start_server():
    # result = lsp.request_definition(
    #     # Filename of location where request is being made
    #     "code.java",
    #     163,  # line number of symbol for which request is being made
    #     4  # column number of symbol for which request is being made
    # )
    # result2 = lsp.request_completions(
    #     ...
    # )
    # result3 = lsp.request_references(
    #     ...
    # )
    result4 = lsp.request_document_symbols(
        "code.java"
    )
    print(result4)
    # result5 = lsp.request_hover(
    #     ...
    # )
    # ...
