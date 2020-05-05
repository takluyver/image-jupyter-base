from nbconvert import HTMLExporter
import re

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


def to_html(
    nb, html_file, exporter=HTMLExporter(template_file="full"), code_folding=True
):
    """
	A simple function to convert a notebook to HTML.  For consistency in the output
    format it is used by both, the save hook and the execute & convert function.  The
    exporter is passed as an argument for increased performance (constructing it is time
    consuming) but any valid HTML exporter can be used.
    """
    body, resources = exporter.from_notebook_node(
        nb, resources={"ipywidgets_base_url": "https://unpkg.com/"}
    )
    with open(html_file, mode="w") as f:
        if code_folding:
            f.write(add_hide_code(body))
        else:
            f.write(body)
