from jupyterfg.save import post_save_hook

c.FileContentsManager.post_save_hook = post_save_hook

c.ServerApp.jpserver_extensions = {"crash_ext": True}
