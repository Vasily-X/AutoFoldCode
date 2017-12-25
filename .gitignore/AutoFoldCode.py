import sublime
import sublime_plugin

import os

# File name that our plugin data is saved under.
__storage_file__ = 'AutoFoldCode.sublime-settings'

class AutoFoldCode(sublime_plugin.EventListener):
  # Restore all the saved folds.
  def restore_folds(self, view):
    s = sublime.load_settings(__storage_file__)
    saved_regions = s.get(view.file_name(), [])

    if saved_regions:
      for a, b in saved_regions:
        view.fold(sublime.Region(a, b))

  # Restore folded regions when each file is opened.
  def on_load_async(self, view):
    self.restore_folds(view)

  # Save the folded regions to disk.
  def save_regions(self, view):
    s = sublime.load_settings(__storage_file__)
    regions_to_save = [(r.a, r.b) for r in view.folded_regions()]

    # Save the folded regions.
    if regions_to_save:
      s.set(view.file_name(), regions_to_save)
      sublime.save_settings(__storage_file__)

  # Save regions when file is saved.
  def on_post_save_async(self, view):
    self.save_regions(view);

  # Save regions when file is closed.
  def on_close(self, view):
    self.save_regions(view);


# A window command that clears all the saved code folds.
class AutoFoldCodeClearCommand(sublime_plugin.WindowCommand):
  def run(self):
    # Load the settings.
    settings = sublime.load_settings(__storage_file__)
    # Read the file (to get the keys).
    f = sublime.load_resource(os.path.join('Packages', 'User', __storage_file__))
    try:
      # For each key (file_name), erase the value (folded regions).
      for key in sublime.decode_value(f):
        settings.erase(key)
    except:
      print('[AutoFoldCode.clear] Error loading settings file.')
    # Flush changes to disk.
    sublime.save_settings(__storage_file__)
