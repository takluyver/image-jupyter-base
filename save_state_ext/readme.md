## Local development

* install jupyter (lab)
* create a new module `save_state_ext` within another directory (e.g. `jupyter_server_extension`)
* Tell jupyter to use this module (jupyter_notebook_configuration.json in `jupyter_server_extension`)
```
{
  "NotebookApp": {
    "nbserver_extensions": {
      "ext_test": true
    },
    "extra_nbextensions_path": ["C:/comma/FASTGenomics/jupyter_server_extension"]
  }
}
```
* start jupyter lab (e.g. within pyCharm), where you set the working directory to `jupyter_server_extension`


## Additional links

https://jupyter-notebook.readthedocs.io/en/stable/extending/handlers.html