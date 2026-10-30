# NotebookLM textbook catalog

This repository records the textbook directory available in NotebookLM’s **Add sources → Textbooks** picker and provides an experimental tool for exporting content from textbooks accessible in a signed-in notebook. The catalog was captured on **October 30, 2026**; it is a snapshot and may change.

The unfiltered response contained **665 unique textbook records** in two pages of 500 and 165. The last page had no continuation token. The catalog describes books and links to their providers; it does not contain the original textbook PDF files.

## Explore the catalog

- [Textbook list (CSV)](textbook-catalog/textbooks.csv) contains titles, authors, publication years, editions, provider labels, detail links, catalog groups, and descriptions.
- [Original catalog records (JSON)](textbook-catalog/textbooks-source.json) preserves the decoded source arrays and their field order.
- [Filter definitions (JSON)](textbook-catalog/filters-source.json) preserves the names and source IDs for Topic, Level, and Country filters.
- [Catalog notes](textbook-catalog/README.md) describe the export and list all filter IDs.

Each JSON textbook record is an array. Confirmed zero-based positions include `0` (catalog ID), `2` (title), `3` (description), `4` (cover thumbnail URL), `7` (authors), `10` (provider detail URL), `11` (year), `12` (edition), `14` (provider label), and `17` (catalog group). A cover URL points to an image; the image itself is not embedded. Some fields may be null. The CSV is a readable projection, while the JSON retains the original record structure.

## Catalog groups

These are the broad groups in the returned textbook records, with counts from the snapshot:

| Group | Textbooks |
| --- | ---: |
| Arts & Humanities | 163 |
| Sciences & Mathematics | 146 |
| Social Sciences & Law | 135 |
| Engineering & Technology | 126 |
| Business & Economics | 95 |
| **Total** | **665** |

These groups are distinct from the picker’s Topic filters. The exported records do not expose each book’s Topic, Level, or Country assignments, so the files cannot be used to reliably filter individual books by those attributes without querying the picker.

## Picker filters

The picker exposes these options:

| Filter | Available values |
| --- | --- |
| Topic | Business; Computer Science; Economics; Engineering; Health & Medicine; History & Philosophy; Languages & Writing; Law & Politics; Life Sciences; Mathematics; Physical Sciences; Psychology; Sociology & Culture; Student Success; Other |
| Level | Primary & Middle School; Secondary & High School; Higher Education; Other |
| Country | India; United States; Other |

The `Other` values are the picker’s labels; they should not be interpreted as specific countries, levels, or subjects.

## Provider labels

The counts below reflect the provider labels returned with records, not a guarantee that every title is freely downloadable or supplied in the same format.

| Provider label | Textbooks |
| --- | ---: |
| eCampusOntario Open Library | 247 |
| S Chand | 149 |
| Open Textbook Library | 147 |
| OpenStax | 41 |
| EMEA | 30 |
| Vikas Publishing House | 29 |
| LibreTexts | 8 |
| Milne Open Textbooks | 5 |
| Abakcus Free Physics Textbooks | 4 |
| California Digital Open Source Library (CDOSL) | 3 |
| CSU-MERLOT | 2 |

## Getting a textbook file

Open a textbook in NotebookLM and select **View details**, or follow the `url` in the CSV to the provider. If the provider offers a download, choose an available format and verify the saved file. Availability, licensing, and formats depend on the provider.

For the tested *360 Essentials*, the provider offered Digital PDF, Print PDF, and Pressbooks XML. NotebookLM’s import metadata identified the source as `application/pdf`, but it did not identify which provider variant was imported. A PDF download attempt timed out, so the original file was not recovered or verified. No universal NotebookLM endpoint for downloading the original PDF has been established.

## Export content from NotebookLM

The experimental [exporter](scripts/export_notebook_textbook.py) calls NotebookLM’s internal, session-authenticated `LoadSource` endpoint and writes the returned structured content and derived plain text. It was tested against two sources already added to the notebook: *360 Essentials* and *Software Engineering*. The response is not the original PDF; derived text does not preserve PDF layout or embedded images. The endpoint is undocumented and may change.

Requirements: Python 3, `playwright-cli`, an authenticated browser session, and access to the notebook and source. Select the notebook tab, run `playwright-cli requests`, and find a recent `rLM1Ne` request number for that notebook. Request numbers are specific to the session.

```bash
python3 scripts/export_notebook_textbook.py \
  --request-number REQUEST_NUMBER \
  --source-id SOURCE_UUID \
  --output textbook-catalog/exports/my-book
```

The output directory contains `response.txt`, `source.json`, and `textbook.txt`. The script also accepts `--catalog-id` to add a book before exporting it; that code path implements the observed import request but has not been independently tested through the script. Adding a source changes the notebook and is subject to NotebookLM limits. The tool keeps the session token in memory rather than writing it to its output files.

[Source retrieval and endpoint details](textbook-catalog/GETTING-SOURCE-FILES.md) document the request structure, tested results, and provider download steps.

## Repository layout

```text
README.md                             Overview and usage
scripts/export_notebook_textbook.py    Experimental content exporter
textbook-catalog/textbooks.csv         Readable catalog
textbook-catalog/textbooks-source.json  Decoded catalog records
textbook-catalog/filters-source.json  Filter definitions
textbook-catalog/README.md            Catalog details and filter IDs
textbook-catalog/GETTING-SOURCE-FILES.md  Retrieval findings
```

The `.gitignore` excludes browser artifacts, raw responses, local import tests, generated exports, PDFs, and Python cache files. Some evidence files mentioned in the detailed notes exist only in the local workspace and are not tracked in Git.
