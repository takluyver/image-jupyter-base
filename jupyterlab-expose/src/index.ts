import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from "@jupyterlab/application";

const extension: JupyterFrontEndPlugin<void> = {
  id: "jupyterlab-expose",
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    (window as any).labApp = app;
  },
};

export default extension;
