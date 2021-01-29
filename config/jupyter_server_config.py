from jupyterfg.save import post_save_hook

c.FileContentsManager.post_save_hook = post_save_hook

c.ServerApp.nbserver_extensions.append("crash_ext")
