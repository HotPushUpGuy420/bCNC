#!/usr/bin/python
# -*- coding: latin1 -*-
# $Id$
#
# Author:	Vasilis.Vlachoudis@cern.ch
# Date:	20-Aug-2015

__author__ = "Vasilis Vlachoudis"
__email__  = "Vasilis.Vlachoudis@cern.ch"

__name__ = "Tile"

from ToolsPage import Plugin

#import math
#from bmath import Vector
#from CNC import CW,CCW,CNC,Block

#==============================================================================
# Tile replicas of the selected blocks
#==============================================================================
class Tool(Plugin):
	"""Generate replicas of selected code"""
	def __init__(self, master):
		Plugin.__init__(self, master)
		self.name = "Tile"
		self.icon = "tile"
		self.variables = [
			("name",      "db",    "", "Name"),
			("nx",       "int",     3, "Nx"),
			("ny",       "int",     3, "Ny"),
			("dx",        "mm",  50.0, "Dx"),
			("dy",        "mm",  50.0, "Dy")
		]
		self.buttons.append("exe")

	# ----------------------------------------------------------------------
	def execute(self, app):
		# Get selected blocks from editor
		blocks = app.editor.getSelectedBlocks()
		if not blocks:
			app.editor.selectAll()
			blocks = app.editor.getSelectedBlocks()

		try:
			dx = float(self["dx"])
		except:
			dx = 0.0

		try:
			dy = float(self["dy"])
		except:
			dy = 0.0

		pos = blocks[-1]	# insert position

		#undoinfo = []
		y = 0.0
		for j in range(self["ny"]):
			x = 0.0
			for i in range(self["nx"]):
				if i==0 and j==0:
					# skip the first 
					x += dx
					continue
				# clone selected blocks
				undoinfo = []	# FIXME it should be only one UNDO
				newblocks = []
				for bid in blocks:
					undoinfo.append(app.gcode.cloneBlockUndo(bid, pos))
					newblocks.append((pos,None))
					pos += 1
				app.addUndo(undoinfo)

				# FIXME but the moveLines already does the addUndo
				# I should correct it
				app.gcode.moveLines(newblocks, x, y)
				x += dx
			y += dy

		app.refresh()
		app.setStatus("Tiled selected blocks")
