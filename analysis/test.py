#!/usr/bin/env python3

# Using selenium + tor.
# Install with tbselenium with pip. Insure that you use the pip in your virtual
# environment.
# $ $(which pip) install tbselenium

from pathlib import Path
home = Path.home()

from os.path import join
tor_path = join(home,".tor")

from os import getcwd
here = getcwd()
tor_path = join(here,"extensions","torbrowser-install-win64-9.0.9_en-US.exe")

from tbselenium.tbdriver import TorBrowserDriver

with TorBrowserDriver(tor_path) as driver:
    driver.get('https://check.torproject.org')

