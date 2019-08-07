from nbconvert import HTMLExporter
import re

hide_code_script = """
<script>
  function code_toggle() {
    if (code_shown){
      $('div.input').hide('500');
      $('#toggleButton').val('Show Code')
    } else {
      $('div.input').show('500');
      $('#toggleButton').val('Hide Code')
    }
    code_shown = !code_shown
  }

  $( document ).ready(function(){
    code_shown=false;
    $('div.input').hide()
  });
</script>
<form action="javascript:code_toggle()">
<input type="submit" id="toggleButton" value="Show Code">
</form>
"""


def add_hide_code(body):
    return re.sub("<body>", "<body>" + hide_code_script, body)


def to_html(nb, html_file, exporter=HTMLExporter(template_file="full")):
    """A simple function to convert a notebook to HTML.  For consistency in the output
format it is used by both, the save hook and the execute & convert function.  The
exporter is passed as an argument for increased performance (constructing it is time
consuming) but any valid HTML exporter can be used.

    """
    body, resources = exporter.from_notebook_node(nb)
    with open(html_file, mode="w") as f:
        f.write(add_hide_code(body))
