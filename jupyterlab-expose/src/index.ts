import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

/**
 * Initialization data for the jupyterlab-expose extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-expose:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension jupyterlab-expose is activated!');
    (window as any).labApp = app;
  }
};

export default extension;
