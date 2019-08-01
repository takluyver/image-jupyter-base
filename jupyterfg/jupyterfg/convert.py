from nbconvert import HTMLExporter


def to_html(nb, html_file, exporter=HTMLExporter(template_file="full")):
    """A simple function to convert a notebook to HTML.  For consistency in the output
format it is used by both, the save hook and the execute & convert function.  The
exporter is passed as an argument for increased performance (constructing it is time
consuming) but any valid HTML exporter can be used.

    """
    body, resources = exporter.from_notebook_node(nb)
    with open(html_file, mode="w") as f:
        f.write(body)
