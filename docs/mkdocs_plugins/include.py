# SPDX-Identifier: BSD-3-Clause
import logging

from markdown import Markdown
from pymdownx.superfences import SuperFencesBlockPreprocessor, highlight_validator

log = logging.getLogger("mkdocs.include_extension")


def include_file_format(source: str, _language: str, class_name: str, options: dict, md: Markdown, **kwargs):
    """
    Custom fence formatter that includes the contents of an external file
    into a fenced code block in a Markdown document.

    This is designed to work with `pymdownx.superfences` by defining a
    custom fence (e.g., `include`) and enabling file inclusion using
    a `path` option.

    Usage:
        Define a custom fence in mkdocs.yml:

            markdown_extensions:
              - pymdownx.superfences:
                  custom_fences:
                    - name: include
                      class: source
                      format: !!python/name:include.include_file_format

        Then use in Markdown like:

            ```include {language=python}
            snippets/example.py
            ```

        This will read `snippets/example.py` and render it as a highlighted
        code block.
    """

    fenced_preprocessor: SuperFencesBlockPreprocessor = md.preprocessors["fenced_code_block"]
    file_path = source.strip()
    log.debug(f"Processing file inclusion: {file_path}")
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as e:
            source = f"Error including file: {e}"
            log.error(f"Error reading file: {e}")
    language = options.pop('language', '')
    classes: list[str] = kwargs.setdefault('classes', [])
    classes.append(class_name)
    return fenced_preprocessor.highlight(source, language, options, md, **kwargs)


def include_file_validate(language, inputs, options, attrs, md):
    """
    Validation callback for the `include` custom fenced code block.

    This function is used with `pymdownx.superfences` to process and validate
    options for the `include` fence before the formatter is called.
    """
    options['language'] = inputs.pop('language', '')
    return highlight_validator(language, inputs, options, attrs, md)
