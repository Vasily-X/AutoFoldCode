# AutoFoldCode <img src="./resources/fold-marker.png" height="16" />

A Sublime Text package that saves/restores folded code regions in files automatically.

This plugin makes folded code regions persist - whether you're just opening/closing a file, starting/quitting Sublime Text or rebooting your computer, AutoFoldCode will restore your folded code with no hassle.

Thank you for checking this out, if you want to support what I do you might [buy me a coffee](https://ko-fi.com/ridetoday)!

## Installation

#### Automatic (preferred)

1. Open the Command Palette, and find `Package Control: Install Package`.
2. Search for `AutoFoldCode` and install.

#### Manual

```bash
# To install, clone this repository into you Sublime Packages directory:
cd /path/to/packages/directory
git clone https://github.com/RIDE-2DAY/AutoFoldCode.git

# To update to the latest:
git pull origin master
```

## Usage

Once installed, AutoFoldCode will automatically begin persisting code folds.

This package includes some useful commands:

* `AutoFoldCode: Clear All`
	- This command will clear AutoFoldCode's cache, and unfold any folded regions in open views.
* `AutoFoldCode: Clear Current File`
	- This command will remove the current file's folded regions from the cache, and unfold all folded regions in the file.
* `AutoFoldCode: Unfold All Open Files`
	- This unfolds all open files in all open windows.
	- If you want to just unfold just the current file, Sublime Text already includes the `"unfold_all"` command for this.

## FAQ

* "When I start Sublime Text, my code folds aren't restored immediately"
	- This is because AutoFoldCode hasn't loaded yet. Once Sublime Text initialises AutoFoldCode, then your folds will be restored.
* "Sometimes AutoFoldCode folds my code in the wrong places"
	- This will occur if you have closed Sublime Text, edit the file with another editor, then re-open Sublime Text.

## Credits

Many thanks to the [contributors](https://github.com/RIDE-2DAY/AutoFoldCode/graphs/contributors)!  
And of course, thanks to the great developers at [Sublime Text](http://sublimetext.com/).

## License

[MIT](./LICENSE)
