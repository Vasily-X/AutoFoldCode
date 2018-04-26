import os
import sublime
import sublime_plugin

# File name/path where the plugin data is saved.
__storage_file__ = 'AutoFoldCode.sublime-settings'
__storage_path__ = os.path.join('Packages', 'User', __storage_file__)

# Called at sublime startup: restore folded regions for each view.
def plugin_loaded():
  for window in sublime.windows():
    for view in window.views():
      if view.file_name():
        _restore_folds(view)

# Listen to changes in views to automatically save code folds.
class AutoFoldCodeListener(sublime_plugin.EventListener):
  def on_load_async(self, view):
    _restore_folds(view)

  def on_post_save_async(self, view):
    _save_folds(view)

  def on_close(self, view):
    _save_folds(view)

  def on_text_command(self, view, command_name, args):
    if command_name == 'unfold_all' and view.file_name() != None:
      _clear_cache(view.file_name())

# ------------------- #
#   Window Commands   #
# ------------------- #

# Clears all the saved code folds and unfolds all the currently open windows.
class AutoFoldCodeClearAllCommand(sublime_plugin.WindowCommand):
  def run(self):
    _clear_cache('*')
    self.window.run_command('auto_fold_code_unfold_all')

# Clears the cache for the current view, and unfolds all its regions.
class AutoFoldCodeClearCurrentCommand(sublime_plugin.WindowCommand):
  def run(self):
    view = self.window.active_view()
    if view and view.file_name():
      view.unfold(sublime.Region(0, view.size()))
      _clear_cache(view.file_name())

  def is_enabled(self):
    view = self.window.active_view()
    return view != None and view.file_name() != None

# Unfold all code folds in all open files.
class AutoFoldCodeUnfoldAllCommand(sublime_plugin.WindowCommand):
  def run(self):
    for window in sublime.windows():
      for view in window.views():
        view.unfold(sublime.Region(0, view.size()))

# ----------- #
#   Helpers   #
# ----------- #

# Restore the saved folds for the given view.
def _restore_folds(view):
  settings = sublime.load_settings(__storage_file__)
  for a, b in settings.get(view.file_name(), []):
    view.fold(sublime.Region(a, b))

# Save the folded regions of the view to disk.
def _save_folds(view):
  settings = sublime.load_settings(__storage_file__)
  regions = [(r.a, r.b) for r in view.folded_regions()]
  settings.set(view.file_name(), regions)
  sublime.save_settings(__storage_file__)

# Clears the cache. If name is '*', it will clear the whole cache.
# Otherwise, pass in the file_name of the view to clear the view's cache.
def _clear_cache(name):
  # Read the file (to get it as a dict).
  json = sublime.load_resource(__storage_path__)
  settings = sublime.load_settings(__storage_file__)
  try:
    for file_name in sublime.decode_value(json):
      if name == '*' or file_name == name:
        settings.erase(file_name)
  except Exception as e:
    print('[AutoFoldCode._clear_cache] Error loading settings file:')
    print(e)
  # Flush changes to disk.
  sublime.save_settings(__storage_file__)
