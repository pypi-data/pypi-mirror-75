=====================
wx_icons_suru
=====================

.. start short_desc

**Suru icon theme for wxPython 🐍**

.. end short_desc

This package provides a wxPython wxArtProvider class with icons from the Suru Icon Theme.

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/custom_wx_icons_suru/latest?logo=read-the-docs
	:target: https://custom_wx_icons_suru.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |docs_check| image:: https://github.com/domdfcoding/custom_wx_icons_suru/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/custom_wx_icons_suru/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/custom_wx_icons_suru/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/custom_wx_icons_suru
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/custom_wx_icons_suru/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/custom_wx_icons_suru/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/custom_wx_icons_suru/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/custom_wx_icons_suru/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/custom_wx_icons_suru/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/custom_wx_icons_suru/requirements/?branch=master
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/custom_wx_icons_suru?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/custom_wx_icons_suru
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/wx_icons_suru
	:target: https://pypi.org/project/wx_icons_suru/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/wx_icons_suru?logo=python&logoColor=white
	:target: https://pypi.org/project/wx_icons_suru/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/wx_icons_suru
	:target: https://pypi.org/project/wx_icons_suru/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/wx_icons_suru
	:target: https://pypi.org/project/wx_icons_suru/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/custom_wx_icons_suru
	:target: https://github.com/domdfcoding/custom_wx_icons_suru/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/custom_wx_icons_suru
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/custom_wx_icons_suru/v0.1.2
	:target: https://github.com/domdfcoding/custom_wx_icons_suru/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/custom_wx_icons_suru
	:target: https://github.com/domdfcoding/custom_wx_icons_suru/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. end shields

Installation
===============

.. start installation

``wx_icons_suru`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install wx_icons_suru

.. end installation

Usage
=======

To use ``wx_icons_suru`` in your application:

.. code-block:: python

	from wx_icons_suru import wxSuruIconTheme

	class MyApp(wx.App):
		def OnInit(self):
			wx.ArtProvider.Push(wxSuruIconTheme())
			self.frame = TestFrame(None, wx.ID_ANY)
			self.SetTopWindow(self.frame)
			self.frame.Show()
			return True

And then the icons can be accessed through wx.ArtProvider:

.. code-block:: python

	wx.ArtProvider.GetBitmap('document-new', wx.ART_OTHER, wx.Size(48, 48))

Any `FreeDesktop Icon Theme Specification <https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html>`_ name can be used.

Currently the `Client ID` is not used, so just pass `wx.ART_OTHER`.
