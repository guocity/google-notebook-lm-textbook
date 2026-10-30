# NotebookLM textbook catalog

The `textbook-catalog` directory contains the exported catalog, filter definitions, and notes on source retrieval. `scripts/export_notebook_textbook.py` exports structured content from an accessible NotebookLM source using an existing playwright-cli session. See [source retrieval instructions](textbook-catalog/GETTING-SOURCE-FILES.md) for setup and limitations.

Browser session artifacts, imported book content, and raw responses are ignored by Git. The catalog metadata and reusable script are tracked.
