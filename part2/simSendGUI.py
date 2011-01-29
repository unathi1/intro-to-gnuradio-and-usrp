#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Simulated Sender GUI
# Generated: Sat Jan 29 16:30:39 2011
##################################################

from gnuradio import blks2
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import numpy
import wx

class simSendGUI(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Simulated Sender GUI")

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 32000
		self.noise_voltage = noise_voltage = 0.01
		self.mult_const = mult_const = 1

		##################################################
		# Controls
		##################################################
		_noise_voltage_sizer = wx.BoxSizer(wx.VERTICAL)
		self._noise_voltage_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_noise_voltage_sizer,
			value=self.noise_voltage,
			callback=self.set_noise_voltage,
			label="Noise Voltage",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._noise_voltage_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_noise_voltage_sizer,
			value=self.noise_voltage,
			callback=self.set_noise_voltage,
			minimum=0,
			maximum=1,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Add(_noise_voltage_sizer)
		self._mult_const_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.mult_const,
			callback=self.set_mult_const,
			label="Multiplication Const",
			converter=forms.float_converter(),
		)
		self.Add(self._mult_const_text_box)

		##################################################
		# Blocks
		##################################################
		self.blks2_ofdm_mod_0 = grc_blks2.packet_mod_b(blks2.ofdm_mod(
				options=grc_blks2.options(
					modulation="bpsk",
					fft_length=512,
					occupied_tones=200,
					cp_length=128,
					pad_for_usrp=True,
					log=None,
					verbose=None,
				),
			),
			payload_length=512,
		)
		self.gr_channel_model_0 = gr.channel_model(
			noise_voltage=noise_voltage,
			frequency_offset=0.0,
			epsilon=1.0,
			taps=(1.0 + 1.0j, ),
			noise_seed=42,
		)
		self.gr_multiply_const_vxx_0 = gr.multiply_const_vcc((mult_const, ))
		self.gr_throttle_0 = gr.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.random_source_x_0 = gr.vector_source_b(map(int, numpy.random.randint(0, 256, 512)), True)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=50,
			sample_rate=samp_rate,
			fft_size=256,
			fft_rate=30,
			average=True,
			avg_alpha=0.1,
			title="FFT Plot",
			peak_hold=False,
		)
		self.Add(self.wxgui_fftsink2_0.win)

		##################################################
		# Connections
		##################################################
		self.connect((self.gr_throttle_0, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.gr_channel_model_0, 0), (self.gr_throttle_0, 0))
		self.connect((self.gr_multiply_const_vxx_0, 0), (self.gr_channel_model_0, 0))
		self.connect((self.random_source_x_0, 0), (self.blks2_ofdm_mod_0, 0))
		self.connect((self.blks2_ofdm_mod_0, 0), (self.gr_multiply_const_vxx_0, 0))

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)

	def set_noise_voltage(self, noise_voltage):
		self.noise_voltage = noise_voltage
		self._noise_voltage_slider.set_value(self.noise_voltage)
		self._noise_voltage_text_box.set_value(self.noise_voltage)
		self.gr_channel_model_0.set_noise_voltage(self.noise_voltage)

	def set_mult_const(self, mult_const):
		self.mult_const = mult_const
		self._mult_const_text_box.set_value(self.mult_const)
		self.gr_multiply_const_vxx_0.set_k((self.mult_const, ))

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = simSendGUI()
	tb.Run(True)

