import sublime
import sublime_plugin

import os

# File name that our plugin data is saved under.
__storage_file__ = 'AutoFoldCode.sublime-settings'

# Called at sublime startup: restore folded regions for each view.
def plugin_loaded():
  for window in sublime.windows():
    for view in window.views():
      restore_folds(view)

# Restore all the saved folds.
def restore_folds(view):
  s = sublime.load_settings(__storage_file__)
  saved_regions = s.get(view.file_name(), [])

  if saved_regions:
    for a, b in saved_regions:
      view.fold(sublime.Region(a, b))

# Save the folded regions to disk.
def save_folds(view):
  s = sublime.load_settings(__storage_file__)
  regions_to_save = [(r.a, r.b) for r in view.folded_regions()]

  # Save the folded regions.
  if regions_to_save:
    s.set(view.file_name(), regions_to_save)
    sublime.save_settings(__storage_file__)

# Clears the cache. If name is '*', it will clear the whole cache.
# Otherwise, pass in the file_name of the view to clear the view's cache.
def clear_cache(name):
  # Load the settings.
  settings = sublime.load_settings(__storage_file__)
  # Read the file (to get the keys).
  f = sublime.load_resource(os.path.join('Packages', 'User', __storage_file__))
  try:
    for file_name in sublime.decode_value(f):
      if name == '*' or file_name == name:
        settings.erase(file_name)
  except Exception as e:
    print('[AutoFoldCode.clear] Error loading settings file.')
    print(e)
  # Flush changes to disk.
  sublime.save_settings(__storage_file__)

class AutoFoldCodeListener(sublime_plugin.EventListener):
  # Restore folded regions when each file is opened.
  def on_load_async(self, view):
    restore_folds(view)

  # Save regions when file is saved.
  def on_post_save_async(self, view):
    save_folds(view);

  # Save regions when file is closed.
  def on_close(self, view):
    save_folds(view);

# --------------- #
# Window Commands #
# --------------- #

# Clears all the saved code folds and unfolds all the currently open windows.
class AutoFoldCodeClearAllCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.run_command('auto_fold_code_unfold_all')
    clear_cache('*')

# Clears the cache for the current view, and unfolds all its regions.
class AutoFoldCodeClearCurrentCommand(sublime_plugin.WindowCommand):
  def run(self):
    view = self.window.active_view()
    file_name = view.file_name()
    if view and file_name:
      view.unfold(sublime.Region(0, view.size()))
      clear_cache(file_name)

  def is_enabled(self):
    view = self.window.active_view()
    file_name = view.file_name()
    return view != None and file_name != None

# Unfold all code folds in all open files.
class AutoFoldCodeUnfoldAllCommand(sublime_plugin.WindowCommand):
  def run(self):
    for window in sublime.windows():
      for view in window.views():
        view.unfold(sublime.Region(0, view.size()))
