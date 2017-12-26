# AutoFoldCode
_A Sublime Text package that saves/restores Folded Code Regions in files automagically. Originally developed by @callodacity._

This plugin makes folded code regions persist - whether you're just opening / closing a file, starting / quitting Sublime Text or rebooting your computer, `AutoFoldCode` will restore your folded code with no hassle.

# Installation

1. Open the Command Palette, and find `Package Control: Install Package`.
2. Search for `AutoFoldCode` and install.

# Usage

Once installed `AutoFoldCode` will automatically begin persisting code folds. 

To clear `AutoFoldCode`'s cache, use the `AutoFoldCode: Clear` command from within the Command Palette.

# Known Issues

* When Sublime Text is closed and re-opened, it re-opens the previously opened views. This unfortunately doesn't remember previous folded regions, and there doesn't seem to be an event for it either, so it doesn't seem possible to fix this at the moment. `AutoFoldCode` however, still remembers the folded regions, so closing and re-opening the file will restore the folded regions.

# License

[MIT](./LICENSE)
