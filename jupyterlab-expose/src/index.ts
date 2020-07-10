import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from "@jupyterlab/application";

const extension: JupyterFrontEndPlugin<void> = {
  id: "jupyterlab-expose",
  autoStart: true,
  activate: async (app: JupyterFrontEnd) => {
    (window as any).labApp = app;
  }
};

export default extension;
