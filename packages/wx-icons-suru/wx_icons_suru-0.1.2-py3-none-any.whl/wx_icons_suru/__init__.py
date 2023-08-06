#!/usr/bin/python3
#
#  __init__.py
#
#  Copyright (C) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Includes icons from the Suru icon theme.
#  https://github.com/ubuntu/yaru/blob/master/icons
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License version 3
#  as published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
from typing import Any, Optional, Tuple, Union

# 3rd party
import importlib_resources  # type: ignore
import wx  # type: ignore
from wx_icons_hicolor import Icon, IconTheme
from wx_icons_humanity import HumanityIconTheme, wxHumanityIconTheme

# this package
from wx_icons_suru import Suru

with importlib_resources.path(Suru, "index.theme") as theme_index_path_:
	theme_index_path = str(theme_index_path_)

__version__: str = "0.1.2"


def version() -> str:
	return f"""wx_icons_suru
Version {__version__}
Suru Icon Theme Version 20.04.4
"""


class SuruIconTheme(HumanityIconTheme):
	_humanity_theme: IconTheme = HumanityIconTheme.create()

	@classmethod
	def create(cls):
		"""
		Create an instance of the Suru Icon Theme
		"""

		with importlib_resources.path(Suru, "index.theme") as theme_index_path_:
			theme_index_path = str(theme_index_path_)

		return cls.from_configparser(theme_index_path)

	def find_icon(
			self,
			icon_name: str,
			size: int,
			scale: Any,
			prefer_this_theme: bool = True,
			) -> Optional[Icon]:
		"""

		:param icon_name:
		:type icon_name:
		:param size:
		:type size:
		:param scale:
		:type scale:
		:param prefer_this_theme: Return an icon from this theme even if it has to be resized,
			rather than a correctly sized icon from the parent theme.
		:type prefer_this_theme:
		:return:
		:rtype:
		"""

		icon = self._do_find_icon(icon_name, size, scale, prefer_this_theme)
		if icon:
			return icon
		else:
			# If we get here we didn't find the icon.
			return self._humanity_theme.find_icon(icon_name, size, scale)


class wxSuruIconTheme(wxHumanityIconTheme):
	_suru_theme: IconTheme = SuruIconTheme.create()

	def CreateBitmap(self, id: Any, client: Any, size: Union[Tuple[int], wx.Size]) -> wx.Bitmap:
		icon = self._suru_theme.find_icon(id, size[0], None)
		if icon:
			print(icon, icon.path)
			return self.icon2bitmap(icon, size[0])
		else:
			# return self._humanity_theme.find_icon("image-missing", size.x, None).as_bitmap()
			print("Icon not found in Suru theme")
			print(id)
			return super().CreateBitmap(id, client, size)


if __name__ == '__main__':
	# theme = SuruIconTheme.from_configparser(theme_index_path)
	theme = SuruIconTheme.create()

	# for directory in theme.directories:
	# 	print(directory.icons)
	# 3rd party
	from wx_icons_hicolor import test, test_random_icons  # TODO

	# test_random_icons(theme)
	test.test_icon_theme(theme, show_success=False)
