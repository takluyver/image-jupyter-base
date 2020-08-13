import re

from jupyter_contrib_nbextensions.nbconvert_support import EmbedHTMLExporter

hide_code_script = """
<script>
  // Initiate with code visible
  codeVisible=true;
  // toggle code function
  var codeToggle = function code_toggle() {
    if (codeVisible){
      $('div.input').hide('500');
      $('div.output_stderr').hide('500');
    } else {
      $('div.input').show('500');
      $('div.output_stderr').show('500');
    }
    codeVisible = !codeVisible;
    return codeVisible;
  }
</script>
"""


def add_hide_code(body):
    return re.sub("<body>", "<body>" + hide_code_script, body)


def to_html(nb, html_file, exporter=None, code_folding=True):
    """
    A simple function to convert a notebook to HTML.  For consistency in the output
    format it is used by both, the save hook and the execute & convert function.  The
    exporter is passed as an argument for increased performance (constructing it is time
    consuming) but any valid HTML exporter can be used.

    Parameters
    ----------
    nb : Path
        Path to the ipynb inut file
    html_file : Path
        Path to the html output file
    exporter : nbconvert exporte, optional
        The exporter to use, by default EmbedHTMLExporter(template_file="full")
    code_folding : bool, optional
        Whether to include the code folding cuntion or not, by default True
    """
    res = {
        "metadata": {
            "path": html_file.parent
        },  # required to embed images correctly, otherwise wrong working directory
        "ipywidgets_base_url": "https://unpkg.com/",  # required to embed widgets correctly
    }

    if exporter is None:
        exporter = EmbedHTMLExporter(template_file="full")

    body, resources = exporter.from_notebook_node(nb, resources=res)
    with open(html_file, mode="w") as f:
        if code_folding:
            f.write(add_hide_code(body))
        else:
            f.write(body)
