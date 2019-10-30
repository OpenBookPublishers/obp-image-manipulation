# obp-image-manipulation
This script simplifies elements of html files exported from InDesign.

With our present configuration, InDesign outputs images and captions like so:
```
<div>
    <div id="important-id">
        <img />
    </div>
</div>
<p class="caption"></p>
```
Where **#important-id** describes important rules to display the image.

Whereas this works fine, our workflow can benefit from a more streamlined structure to embed tools (i.e. zoomify) more efficiently. This would be:
```
<figure>
    <img id="important-id" />
    <p class="caption"></p>
</figure>
```
## Installation
Install the system packages. On Debian:
```
$ apt-get install python3.5-venv python3-pip
```
You might want to _install third-party python libraries_ and _run the script_ in a virtual environment. Create the environment first:
```
$ cd your-work-folder
$ pyvenv-3.5 .venv
$ source .venv/bin/activate
```
Then install the dependencies:
```
(.venv) $ pip3 -r requirements.txt 
```

## Run the script
Simply:
```
(.venv) $ python3 main.py input-file.xhtml output-file.xhtml
```

If needed, get tips by:
```
(.venv) $ python3 main.py -h
```
## Troubleshooting
### Character encoding
The current version of the script outputs `utf-8` files. If required a different encoding (i.e. `utf-16`), please change this in the last part of `main.py`, when `beautifulsoup` encodes the _soup_ prior writing the output file.
