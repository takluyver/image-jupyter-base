import {
    showDialog, Dialog
} from '@jupyterlab/apputils';

import { ServerConnection } from '@jupyterlab/services';

import { URLExt } from '@jupyterlab/coreutils';

import {
    JupyterFrontEnd, JupyterFrontEndPlugin, IRouter
} from '@jupyterlab/application';

import { Widget } from '@phosphor/widgets';

import { ITopBar } from "jupyterlab-topbar";

import '@jupyterlab/application/style/buttons.css';

import '../style/index.css';

const extension: JupyterFrontEndPlugin<void> = {
    id: 'jupyterlab-quit',
    autoStart: true,
    requires: [IRouter, ITopBar],
    activate: async (
        app: JupyterFrontEnd,
        router: IRouter,
        topBar: ITopBar,
    ) => {
        let quit = document.createElement('a');
        quit.id = "quit";
        quit.innerHTML = "Quit";
        quit.addEventListener('click', function () {
            return showDialog({
                title: 'Shutdown confirmation',
                body: 'Please confirm you want to shut down JupyterLab.',
                buttons: [
                    Dialog.cancelButton(),
                    Dialog.warnButton({ label: 'Shut Down' })
                ]
            }).then(result => {
                if (result.button.accept) {
                    let setting = ServerConnection.makeSettings();
                    let apiURL = URLExt.join(setting.baseUrl, 'api/shutdown');
                    return ServerConnection.makeRequest(
                        apiURL,
                        { method: 'POST' },
                        setting
                    )
                        .then(result => {
                            if (result.ok) {
                                // Close this window if the shutdown request has been successful
                                let body = document.createElement('div');
                                body.innerHTML = `<p>You have shut down the Jupyter server. You can now close this tab.</p>
<p>To use JupyterLab again, you will need to relaunch it.</p>`;
                                void showDialog({
                                    title: 'Server stopped',
                                    body: new Widget({ node: body }),
                                    buttons: []
                                });
                                window.close();
                            } else {
                                throw new ServerConnection.ResponseError(result);
                            }
                        })
                        .catch(data => {
                            throw new ServerConnection.NetworkError(data);
                        });
                }
            });
        });

        const widget = new Widget({node: quit});
        widget.addClass('jp-Button-flat');
        topBar.addItem("quit-button", widget);
    }
};

export default extension;
