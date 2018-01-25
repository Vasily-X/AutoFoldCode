## AutoFoldCode
A Sublime Text package that saves/restores folded code regions in files automatically.

This plugin makes folded code regions persist - whether you're just opening/closing a file, starting/quitting Sublime Text or rebooting your computer, AutoFoldCode will restore your folded code with no hassle.

Thank you for checking this out, if you want to support what I do you might [buy me a coffe](https://ko-fi.com/ridetoday)!

## Installation
1. Open the Command Palette, and find `Package Control: Install Package`.
2. Search for `AutoFoldCode` and install.

## Usage
Once installed, AutoFoldCode will automatically begin persisting code folds. To clear AutoFoldCode's cache, use the `AutoFoldCode: Clear` command from the Command Palette.

## Known Issues
- When you start Sublime Text for the first time, it opens the last files you have been working with, unfortunately the plugin won't restore the folded regions because there isn't any event for that yet. However, closing and reopening the files (or project) fixes this issue.

## Authors
Originally developed by @callodacity, now it's being mantained by me.

## License
[MIT](./LICENSE)
