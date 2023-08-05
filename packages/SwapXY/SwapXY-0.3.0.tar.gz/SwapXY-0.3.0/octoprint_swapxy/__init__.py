# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class SwapXYPlugin(octoprint.plugin.SettingsPlugin, octoprint.plugin.TemplatePlugin):
	config_version_key = "0.3.0"

	other = dict(X="Y", Y="X")

	def on_plugin_enabled(self):
		pass

	def on_plugin_disabled(self):
		pass

	def get_update_information(self):
		return dict(
			swapxy=dict(
				displayName="SwapXY",
				displayVersion=self._plugin_version,

				# version check: PyPI
				type="pypi_release",
				package="swapxy",
				current=self._plugin_version,

				# update method: pip
				pip="swapxy"
			)
		)

	def get_settings_defaults(self):
		return dict(
			reverse=dict(
				X=False,
				Y=False,
			),
			swap=True
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False),
		]

	def rewrite_jog(self, comm_instance, phase, cmd, cmd_type, gcode, subcode=None, tags=None, *args, **kwargs):
		"""
		Replace X with Y or Y with X in gcode initiated by jog commands.
		"""
		if "trigger:printer.jog" not in tags:
			# Ignore normal gcode commands, only affect control buttons
			return

		for axis in ["X", "Y"]:
			if axis in cmd:
				if self._settings.get_boolean(["swap"]):
					# Swap to other axis
					new_axis = self.other[axis]
					cmd = cmd.replace(axis, new_axis)
				else:
					# Do not swap
					new_axis = axis

				# Reverse direction if configured
				if self._settings.get_boolean(["reverse", new_axis]):
					negative = new_axis + "-"

					if negative in cmd:
						cmd = cmd.replace(negative, new_axis)
					elif new_axis in cmd:
						cmd = cmd.replace(new_axis, negative)
			
				# Don't switch it back by iterating again
				break
		return cmd,

__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = SwapXYPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.rewrite_jog,
	}
