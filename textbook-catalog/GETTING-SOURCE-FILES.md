# Getting original textbook source files

Inspected October 30, 2026 using playwright-cli in the signed-in NotebookLM browser session.

## Update: decoded content export endpoint

Further inspection of the loaded application code established a working content export endpoint:

```text
POST https://notebook.google.com/_/LabsTailwindUi/data/batchexecute?rpcids=hizoJc
Service: LabsTailwindOrchestrationService.LoadSource
Content-Type: application/x-www-form-urlencoded;charset=utf-8
```

The form contains `at` (the current session's anti-CSRF token) and `f.req`:

```json
[[["hizoJc", "[[\"SOURCE_UUID\"],[2],CONTEXT_ARRAY]", null, "generic"]]]
```

`CONTEXT_ARRAY` is copied from an observed request in the same signed-in session. The inner request is JSON encoded as a string. This is an internal, session-authenticated endpoint and may change. It is not a public unauthenticated file URL.

For both tested textbooks, the decoded response has source metadata at `[0]` and a structured document at `[3]`. Text runs within that document use `[startOffset, endOffset, [text, ...]]`. The original response and all structured data are preserved; plain text is a derived export that does not retain PDF layout or embedded images.

Verified examples:

| Textbook | Export result |
| --- | --- |
| 360 Essentials | 1,275 text runs; 204,001 text characters before adding line separators |
| Software Engineering | 1,313,139 characters in the derived plain-text export |

**This endpoint exports textbook content, not the original PDF bytes.** No universal original-PDF download endpoint has been verified. The catalog contains 665 books from 11 provider labels; only these two imports were tested with LoadSource.

### Reusable exporter

Use `scripts/export_notebook_textbook.py` from the repository root with the NotebookLM tab selected in playwright-cli. Run `playwright-cli requests` to find an `rLM1Ne` request from the intended notebook. Request number `330` was valid in this test session; it is not a permanent ID.

```bash
# Export an already-added textbook.
python3 scripts/export_notebook_textbook.py \
  --request-number 330 \
  --source-id cf3aaf4c-3bb7-481f-8526-465b100f83e0 \
  --output textbook-catalog/exports/software-engineering

# Add a catalog textbook to the selected notebook, then export its content.
# This modifies the notebook by adding a source. Notebook source limits apply.
python3 scripts/export_notebook_textbook.py \
  --request-number 330 \
  --catalog-id 4a140300e4362143 \
  --output textbook-catalog/exports/360-essentials
```

The existing-source export was tested on Software Engineering. The catalog-ID import option implements the observed `izAoDd` request schema but has not been separately run through this script. The earlier UI import of 360 Essentials succeeded. Do not assume all 665 books can be added to one notebook or that every provider permits the same content export.

Output files are `response.txt` (original response), `source.json` (decoded structured content), and `textbook.txt` (derived text). Session tokens and cookies are not written to those files. The tool uses your existing browser session; it does not provide access to books outside your account's authorization.

## Do the responses include the PDF source file?

Not in the responses inspected in this test. A response that contains `application/pdf` can be metadata describing a PDF; that string does not mean the response contains the file.

Only one textbook import was tested: **360 Essentials : A Beginner’s Guide to Immersive Video Storytelling**. This does not establish the behavior of every textbook or PDF source.

| Response | Observed contents | Original PDF included? |
| --- | --- | --- |
| Textbook catalog (`mVtEUb`) | Catalog arrays with titles, descriptions, cover URLs, authors, publisher and provider links | No PDF file in the exported catalog responses |
| Add textbook (`izAoDd`) | Source ID and metadata, including MIME type `application/pdf` | No PDF bytes, base64 PDF, or direct PDF download URL in the tested response |
| Notebook data (`rLM1Ne`) | Notebook and source metadata | No PDF file in the tested response |

The catalog cover image is a URL at zero-based index `4` of each record in `textbooks-source.json`. It is not an embedded image or a textbook download link.

## Get the source file from the provider

1. In NotebookLM, open the added textbook source.
2. In its details dialog, choose **View details** to open the provider's page. Alternatively, use the provider URL at zero-based index `10` of the catalog record in `textbooks-source.json`, or the `url` column in `textbooks.csv`.
3. On the provider page, choose **Download**, if available.
4. Select the original format offered by that provider, then save the downloaded file.
5. Verify the saved file's type and contents. A provider may offer multiple editions or formats; a matching title alone does not prove it is byte-for-byte identical to NotebookLM's imported file.

For the tested book, the provider is:

[360 Essentials — eCampusOntario](https://openlibrary.ecampusontario.ca/item-details/?id=ad6090e5-8820-48e5-a283-55de896d8ca4)

Its Download panel offered:

| Format | Displayed size |
| --- | --- |
| Digital PDF | 4.1 MB |
| Print PDF | 5.9 MB |
| Pressbooks XML | 502 KB |

The Digital PDF download was attempted, but Playwright did not receive a download event before timing out. No PDF was saved or verified in this test. The options above were observed in the provider UI; a completed download remains to be verified.

The inspected NotebookLM source menu offered **Remove source** and **Rename source**, with no direct download action. This is an observation of this textbook source, not a claim about every NotebookLM source type.

## Decode NotebookLM's response without confusing metadata with a file

The saved Google batchexecute responses are text envelopes with an anti-XSSI prefix, frame lengths, and JSON frames. For a frame whose first element is `wrb.fr`, its third element is another JSON string. Decode that string to obtain the source arrays.

The tested import is already decoded in `import-test/add-source.json`. The MIME value is at `[0][0][2][19]`; its value is `application/pdf`. This is a metadata field, not a PDF payload.

If inspecting another import with playwright-cli:

1. Run `playwright-cli requests` and locate the request generated by adding that source. Request numbers are session-specific.
2. Use `playwright-cli response-body <request-number>` to inspect that response, then decode its JSON layers.
3. Check whether the response actually contains binary file data or an explicit file URL. Do not interpret a MIME type, source ID, thumbnail URL, or extracted text as the original file.
4. If a file request is observed, inspect its response headers and body. A PDF file commonly has a `%PDF-` signature near its beginning. Verify the saved file with a PDF reader; a `.pdf` filename alone is insufficient.

No NotebookLM original-file retrieval endpoint was established in this test. There is no verified procedure here for reconstructing the original PDF from the source ID or extracted text.

## Evidence saved locally

- `import-test/add-response.txt`: original add-source response body.
- `import-test/add-source.json`: decoded import metadata.
- `import-test/notebook-response.txt`: subsequent notebook response body.
- `import-test/notebook-source.json`: decoded notebook metadata.
- `textbooks-source.json`: combined catalog source records.
- `textbooks.csv`: readable catalog and provider links.
