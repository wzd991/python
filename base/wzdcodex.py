#!/usr/bin/env python
# -*- codding utf-8 -*- 
# Wzd codex v1.0

import binascii
import os
import sys
class  WzdCodex(object):
	"""docstring for  WzdCodex"""
	DataCache = bytearray()
	CodexStatusIdle = 0
	CodexStatusReceive = 1
	CodexStatusEnd     = 2
	CodexStatusSumError = 3
	CodexStartVal = 0xfa
	CodexAdjustVal = 0xfb
	CodexState = CodexStatusIdle

	def get_sum(self,data):
		pass

	def __init__(self, callback):
		self.callback = callback

	def decode(self,data):
		if CodexState >
		if data == CodexStartVal:# idle
			if CodexState == CodexStatusReceive:
			elif CodexState == CodexStatusIdle:

		elif data
		pass
	def encode(self,data):
		pass

