import { showDialog, Dialog } from "@jupyterlab/apputils";

import { ServerConnection } from "@jupyterlab/services";

import { URLExt } from "@jupyterlab/coreutils";

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
  IRouter,
} from "@jupyterlab/application";

import { Widget } from "@lumino/widgets";

import { ITopBar } from "jupyterlab-topbar";

import "@jupyterlab/application/style/buttons.css";

import "../style/index.css";

const extension: JupyterFrontEndPlugin<void> = {
  id: "jupyterlab-quit",
  autoStart: true,
  requires: [IRouter, ITopBar],
  activate: async (app: JupyterFrontEnd, router: IRouter, topBar: ITopBar) => {
    (window as any).labApp = app;
    let quit = document.createElement("a");
    quit.id = "quit";
    quit.innerHTML = "Quit";
    quit.addEventListener("click", function () {
      return showDialog({
        title: "Shutdown confirmation",
        body: "Do you really want to quit the interactive analysis?",
        buttons: [
          Dialog.okButton({ label: "Save and quit" }),
          Dialog.warnButton({ label: "Quit without saving" }),
          Dialog.cancelButton(),
        ],
        defaultButton: 0,
      }).then(async (result) => {
        if (result.button.accept) {
          if (result.button.displayType === "default")
            await app.commands.execute("docmanager:save-all");
          (app as any).status._dirtyCount = 0;
          let setting = ServerConnection.makeSettings();
          let apiURL = URLExt.join(setting.baseUrl, "api/shutdown");
          return ServerConnection.makeRequest(
            apiURL,
            { method: "POST" },
            setting
          )
            .then((result) => {
              if (result.ok) {
                let body = document.createElement("div");
                body.innerHTML = `<p>We are shutting down the interactive analysis.</p><br />
<p>You will be redirected to the results page in a moment.</p>`;
                showDialog({
                  title: "Server is shutting down",
                  body: new Widget({ node: body }),
                  buttons: [],
                });
              } else {
                throw new ServerConnection.ResponseError(result);
              }
            })
            .catch((data) => {
              throw new ServerConnection.NetworkError(data);
            });
        }
      });
    });

    const widget = new Widget({ node: quit });
    widget.addClass("jp-Button-flat");
    topBar.addItem("quit-button", widget);
  },
};

export default extension;
