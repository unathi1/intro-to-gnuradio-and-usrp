#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Simple TX/RX Path
# Generated: Wed Jan 19 18:49:39 2011
##################################################

from gnuradio import blks2
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser

class simplePath(gr.top_block):

	def __init__(self):
		gr.top_block.__init__(self, "Simple TX/RX Path")

		##################################################
		# Blocks
		##################################################
		self.blks2_gmsk_demod_0 = blks2.gmsk_demod(
			samples_per_symbol=2,
			gain_mu=0.175,
			mu=0.5,
			omega_relative_limit=0.005,
			freq_error=0.0,
			verbose=False,
			log=False,
		)
		self.blks2_gmsk_mod_0 = blks2.gmsk_mod(
			samples_per_symbol=2,
			bt=0.35,
			verbose=False,
			log=False,
		)
		self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
				access_code="",
				threshold=-1,
				callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
			),
		)
		self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
				samples_per_symbol=1,
				bits_per_symbol=1,
				access_code="",
				pad_for_usrp=True,
			),
			payload_length=0,
		)
		self.blks2_tcp_sink_0 = grc_blks2.tcp_sink(
			itemsize=gr.sizeof_char*1,
			addr="127.0.0.1",
			port=9001,
			server=True,
		)
		self.blks2_tcp_source_0 = grc_blks2.tcp_source(
			itemsize=gr.sizeof_char*1,
			addr="127.0.0.1",
			port=9000,
			server=True,
		)
		self.gr_channel_model_0 = gr.channel_model(
			noise_voltage=0.0,
			frequency_offset=0.0,
			epsilon=1.0,
			taps=(1.0 + 1.0j, ),
			noise_seed=42,
		)

		##################################################
		# Connections
		##################################################
		self.connect((self.blks2_tcp_source_0, 0), (self.blks2_packet_encoder_0, 0))
		self.connect((self.blks2_packet_encoder_0, 0), (self.blks2_gmsk_mod_0, 0))
		self.connect((self.blks2_gmsk_mod_0, 0), (self.gr_channel_model_0, 0))
		self.connect((self.gr_channel_model_0, 0), (self.blks2_gmsk_demod_0, 0))
		self.connect((self.blks2_gmsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
		self.connect((self.blks2_packet_decoder_0, 0), (self.blks2_tcp_sink_0, 0))

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = simplePath()
	tb.start()
	raw_input('Press Enter to quit: ')
	tb.stop()

