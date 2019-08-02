import os
import sublime
import sublime_plugin
import zlib

'''
Storage file format (1.2.0+):

  {
    "version": 1,
    "folds":
    {
      "<filename>":
      {
        "<content_crc32>":
        [
          [
            <region_start>,
            <region_end>
          ],
          ...
        ],
        ...
      },
      ...
    }
  }

Storage file format (pre-1.2.0):

  {
    "<filename>":
    [
      [
        <region_start>,
        <region_end>
      ],
      ...
    ],
    ...
  }
'''

# File name/path where the plugin data is saved.
__storage_file__ = 'AutoFoldCode.sublime-settings'
__storage_path__ = os.path.join('Packages', 'User', __storage_file__)

CURRENT_STORAGE_VERSION = 1

# Called at sublime startup: restore folded regions for each view.
def plugin_loaded():
  for window in sublime.windows():
    for view in window.views():
      if view.file_name() != None:
        _restore_folds(view)

# Listen to changes in views to automatically save code folds.
class AutoFoldCodeListener(sublime_plugin.EventListener):
  def on_load_async(self, view):
    _restore_folds(view)

  def on_post_save_async(self, view):
    # Keep only the latest version, since it's guaranteed that on open, the
    # saved version of the file is opened.
    _save_folds(view, True)

  # Listening on close events is required to handle hot exit, for whom there is
  # no available listener.
  def on_close(self, view):
    # In this case, we don't clear the previous versions fold data, so that on
    # open, depending on the previous close being a hot exit or a regular window
    # close, the corresponding fold data is retrieved.
    #
    # If a user performs multiple modifications and hot exits, the fold data for
    # each version is stored. This is acceptable, since the first user initiated
    # save will purge the versions and store only the latest.
    _save_folds(view, False)

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
  file_name = view.file_name()

  if file_name != None:
    settings, all_folds_data = _load_storage_settings(save_on_reset=True)

    view_folds_data = all_folds_data.get(file_name, {})
    view_content_checksum = _compute_view_content_checksum(view)

    for a, b in view_folds_data.get(view_content_checksum, []):
      view.fold(sublime.Region(a, b))

# Save the folded regions of the view to disk.
def _save_folds(view, clean_existing_fold_versions):
  file_name = view.file_name()

  if file_name != None:
    settings, all_folds_data = _load_storage_settings(save_on_reset=False)

    regions = [(r.a, r.b) for r in view.folded_regions()]

    if regions:
      if clean_existing_fold_versions or not file_name in all_folds_data:
        all_folds_data[file_name] = {}

      view_folds_data = all_folds_data.get(file_name)
      view_content_checksum = _compute_view_content_checksum(view)
      view_folds_data[view_content_checksum] = regions
    else:
      all_folds_data.pop(file_name, None)

    settings.set("folds", all_folds_data)
    sublime.save_settings(__storage_file__)

# Clears the cache. If name is '*', it will clear the whole cache.
# Otherwise, pass in the file_name of the view to clear the view's cache.
def _clear_cache(name):
  settings, all_folds_data = _load_storage_settings(save_on_reset=False)

  file_names_to_delete = [file_name for file_name in all_folds_data if name == '*' or file_name == name]
  for file_name in file_names_to_delete:
    all_folds_data.pop(file_name)

  settings.set("folds", all_folds_data)
  sublime.save_settings(__storage_file__)

# Loads the settings, resetting the storage file, if the version is old (or broken).
# Returns the settings instance, and, for convenience, the folds data.
def _load_storage_settings(save_on_reset):
  try:
    settings = sublime.load_settings(__storage_file__)
  except Exception as e:
    print('[AutoFoldCode.] Error loading settings file (file will be reset): ', e)
    save_on_reset = True

  if _is_old_storage_version(settings):
    settings.set("version", CURRENT_STORAGE_VERSION)
    settings.set("folds", {})

    if save_on_reset:
      sublime.save_settings(__storage_file__)

  return settings, settings.get("folds")

def _is_old_storage_version(settings):
  settings_version = settings.get("version", 0)

  # Consider the edge case of a file named "version".
  return not isinstance(settings_version, int) or settings_version < CURRENT_STORAGE_VERSION

# Returns the checksum in Python hex string format.
#
# The view content returned is always the latest version, even when closing
# without saving.
def _compute_view_content_checksum(view):
  view_content = view.substr(sublime.Region(0, view.size()))
  int_crc32 = zlib.crc32(view_content.encode('utf-8'))
  return hex(int_crc32 % (1<<32))
