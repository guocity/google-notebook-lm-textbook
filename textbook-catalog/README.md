# NotebookLM textbook directory

Exported October 30, 2026 using playwright-cli from the notebook’s Add sources → Textbooks catalog.

Total: 665 unique textbooks across two response pages (500 + 165). The final page has no continuation token.

## Source files

- `all-textbooks-response.txt` and `page-002-response.txt`: original server response bodies, unchanged.
- `all-textbooks-source.json` and `page-002-source.json`: decoded source arrays, preserving field order and nulls.
- `textbooks-source.json`: combined 665 source records, preserving each original array.
- `textbooks.csv`: readable catalog with titles, authors, years, publishers, links, descriptions and catalog groups.
- `filters-response.txt`: original filter response.
- `filters-source.json`: decoded original filter definitions, including IDs.

The source catalog records contain catalog groups but do not expose per-book Topic, Level or Country assignments in these responses. The complete available filter options follow.

## Topic

- Business (`SUBJECT_BUSINESS`)
- Computer Science (`SUBJECT_COMPUTER_SCIENCE`)
- Economics (`SUBJECT_ECONOMICS`)
- Engineering (`SUBJECT_ENGINEERING`)
- Health & Medicine (`SUBJECT_HEALTH_AND_MEDICINE`)
- History & Philosophy (`SUBJECT_HISTORY_AND_PHILOSOPHY`)
- Languages & Writing (`SUBJECT_LANGUAGES_AND_WRITING`)
- Law & Politics (`SUBJECT_LAW_AND_POLITICS`)
- Life Sciences (`SUBJECT_LIFE_SCIENCES`)
- Mathematics (`SUBJECT_MATHEMATICS`)
- Physical Sciences (`SUBJECT_PHYSICAL_SCIENCES`)
- Psychology (`SUBJECT_PSYCHOLOGY`)
- Sociology & Culture (`SUBJECT_SOCIOLOGY_AND_CULTURE`)
- Student Success (`SUBJECT_STUDENT_SUCCESS`)
- Other (`SUBJECT_OTHER`)

## Level

- Primary & Middle School (`EDUCATION_LEVEL_PRIMARY_AND_MIDDLE_SCHOOL`)
- Secondary & High School (`EDUCATION_LEVEL_HIGH_SCHOOL_AND_AP`)
- Higher Education (`EDUCATION_LEVEL_HIGHER_EDUCATION`)
- Other (`EDUCATION_LEVEL_OTHER`)

## Country

- India (`COUNTRY_INDIA`)
- United States (`COUNTRY_UNITED_STATES`)
- Other (`COUNTRY_OTHER`)

