/*
 * This module provides sound access for QUISK using the soundio library.
*/
#include <Python.h>
#include <complex.h>
#include <math.h>
#include "quisk.h"
#include <soundio/soundio.h>
#include <stdint.h>

struct dev_data_t {
	struct SoundIo * soundio;
	struct SoundIoDevice * device;
	struct SoundIoOutStream * outstream;
	struct SoundIoInStream * instream;
	struct SoundIoRingBuffer * capture_buffer;
	struct SoundIoRingBuffer * play_buffer;
	int buffer_read_restart;
	int buffer_write_restart;
} ;

static enum SoundIoBackend text2backend(const char * text)
{
	if (strcmp("alsa", text) == 0)
		return SoundIoBackendAlsa;
	if (strcmp("pulseaudio", text) == 0)
		return SoundIoBackendPulseAudio;
	if (strcmp("jack", text) == 0)
		return SoundIoBackendJack;
	if (strcmp("coreaudio", text) == 0)
		return SoundIoBackendCoreAudio;
	if (strcmp("wasapi", text) == 0)
		return SoundIoBackendWasapi;
	return SoundIoBackendDummy;
}

static enum SoundIoFormat choose_format(struct sound_dev * dev, struct SoundIoDevice * device)
{
	if (soundio_device_supports_format(device, SoundIoFormatS16LE)) {
		dev->sound_format = Int16;
		dev->sample_bytes = 2;
		return SoundIoFormatS16LE;
	}
	if (soundio_device_supports_format(device, SoundIoFormatFloat32LE)) {
		dev->sound_format = Float32;
		dev->sample_bytes = 4;
		return SoundIoFormatFloat32LE;
	}
	if (soundio_device_supports_format(device, SoundIoFormatS32LE)) {
		dev->sound_format = Int32;
		dev->sample_bytes = 4;
		return SoundIoFormatS32LE;
	}
	snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "No suitable device format available.");
	if (quisk_sound_state.verbose_sound) printf("  %s\n", dev->dev_errmsg);
	return SoundIoFormatInvalid;
}

static void overflow_callback(struct SoundIoInStream *stream) {
	struct sound_dev * dev = stream->userdata;
	if (quisk_sound_state.verbose_sound) printf("%s: overflow stream error\n", dev->stream_description);
	dev->dev_error++;
}
	
static void underflow_callback(struct SoundIoOutStream *stream) {
	struct sound_dev * dev = stream->userdata;
	quisk_sound_state.underrun_error++;
	if (quisk_sound_state.verbose_sound) printf("%s: device underflow\n", dev->stream_description);
	dev->dev_underrun++;
}

static void error_callback_in(struct SoundIoInStream *stream, int err) {
	struct sound_dev * dev = stream->userdata;
	if (quisk_sound_state.verbose_sound) printf("%s: input stream error: %s\n", dev->stream_description, soundio_strerror(err));
	dev->dev_error++;
}

static void error_callback_out(struct SoundIoOutStream *stream, int err) {
	struct sound_dev * dev = stream->userdata;
	if (quisk_sound_state.verbose_sound) printf("%s: output stream error: %s\n", dev->stream_description, soundio_strerror(err));
	dev->dev_error++;
}

static void write_callback(struct SoundIoOutStream *stream, int frame_count_min, int frame_count_max)
{  // Read samples from the Quisk play_buffer and write them to the sound card.
	struct SoundIoChannelArea *areas;
	struct sound_dev * dev = stream->userdata;
	struct dev_data_t * device_data;
	struct SoundIoRingBuffer * ring;
	int i, err, two, ch_I, ch_Q;
	char * ptSamples;
	int frames, total_frames, bytes_per_frame, bytes_per_sample;

	//QuiskPrintTime("write_callback", 0);
	if ( ! dev) {
		printf("No dev\n");
		return;
	}
	device_data = dev->device_data;
	if ( ! device_data) {
		printf("No device_data min %d max %d\n", frame_count_min, frame_count_max);
		return;
	}
	ring = device_data->play_buffer;
	if ( ! ring) {
		printf("No play_buffer\n");
		return;
	}

	if (quisk_sound_state.verbose_sound > 1) {
		if (quisk_sound_state.verbose_sound == 4) {
			QuiskMeasureRate("   write_callback", frame_count_max, 0);
		}
		if (quisk_sound_state.verbose_sound >= 9) {
			printf("%s:	 write_callback		frame_count_max %4d\n", dev->stream_description, frame_count_max);
		}
	}

	two = dev->num_channels >= 2;
	ch_I = dev->channel_I;
	ch_Q = dev->channel_Q;
	bytes_per_frame = stream->bytes_per_frame;
	bytes_per_sample = stream->bytes_per_sample;
	if (quisk_play_state == STARTING) {
		device_data->buffer_read_restart = 0;
	}
	else if (device_data->buffer_read_restart) {
		if (soundio_ring_buffer_fill_count(ring) >= soundio_ring_buffer_capacity(ring) / 2) {
			device_data->buffer_read_restart = 0;
			if (quisk_sound_state.verbose_sound)
				printf("%s:	 write_callback: buffer underflow recovery\n", dev->stream_description);
		}
	}
	else if (frame_count_max * bytes_per_frame >= soundio_ring_buffer_fill_count(ring)) {		// underflow in buffer
		device_data->buffer_read_restart = 1;
		dev->dev_underrun++;
		if (quisk_sound_state.verbose_sound)
			printf("%s:	 write_callback: buffer underflow\n", dev->stream_description);
	}
	total_frames = frame_count_max;
	while(total_frames) {
		frames = total_frames;
		if ((err = soundio_outstream_begin_write(stream, &areas, &frames)) != 0) {	// write the first "frames" frames
			if (quisk_sound_state.verbose_sound)
				printf("%s:	 write_callback: unrecoverable stream error: %s\n",
					dev->stream_description, soundio_strerror(err));
			dev->dev_error++;
			return;
		}
		total_frames -= frames;
		if (device_data->buffer_read_restart || quisk_play_state == STARTING) {		// play silence
			for (i = 0; i < frames; i++) {
				memset(areas[ch_I].ptr, 0, bytes_per_sample);
				areas[ch_I].ptr += areas[ch_I].step;
				if (two) {
					memset(areas[ch_Q].ptr, 0, bytes_per_sample);
					areas[ch_Q].ptr += areas[ch_Q].step;
				}
			}
			// do not remove samples from ring buffer
		}
		else if ((rxMode == CWU || rxMode == CWL) && quiskSpotLevel < 0 && dev->dev_index == t_MicPlayback) {	// SoftRock Tx CW from soundio
			for (i = 0; i < frames; i++) {
				ptSamples = quisk_make_txIQ(dev, 0);
				memcpy(areas[ch_I].ptr, ptSamples, bytes_per_sample);
				areas[ch_I].ptr += areas[ch_I].step;
				if (two) {
					ptSamples += bytes_per_sample;
					memcpy(areas[ch_Q].ptr, ptSamples, bytes_per_sample);
					areas[ch_Q].ptr += areas[ch_Q].step;
				}
			}
			soundio_ring_buffer_advance_read_ptr(ring, frames * bytes_per_frame);	// remove samples from ring buffer
		}
		else if (quisk_play_state > RECEIVE && quisk_active_sidetone == 1 && dev->dev_index == t_Playback) {	// Sidetone from soundio
			for (i = 0; i < frames; i++) {
				ptSamples = quisk_make_sidetone(dev, 0);
				memcpy(areas[ch_I].ptr, ptSamples, bytes_per_sample);
				areas[ch_I].ptr += areas[ch_I].step;
				if (two) {
					memcpy(areas[ch_Q].ptr, ptSamples, bytes_per_sample);
					areas[ch_Q].ptr += areas[ch_Q].step;
				}
			}
			soundio_ring_buffer_advance_read_ptr(ring, frames * bytes_per_frame);	// remove samples from ring buffer
		}
		else {		// copy sound samples from the ring buffer to the sound device.
			ptSamples = soundio_ring_buffer_read_ptr(ring);
			if (dev->num_channels == 2 && areas[1].ptr == areas[0].ptr + bytes_per_sample && areas[0].step == bytes_per_sample * 2 &&
					areas[1].step == bytes_per_sample * 2 && ch_I == 0 && ch_Q == 1) {	// check for interleaved and fast copy
				memcpy(areas[0].ptr, ptSamples, frames * bytes_per_frame);
			}
			else {
				for (i = 0; i < frames; i++) {
					memcpy(areas[ch_I].ptr, ptSamples, bytes_per_sample);
					areas[ch_I].ptr += areas[ch_I].step;
					ptSamples += bytes_per_sample;
					if (two) {
						memcpy(areas[ch_Q].ptr, ptSamples, bytes_per_sample);
						areas[ch_Q].ptr += areas[ch_Q].step;
						ptSamples += bytes_per_sample;
					}
				}
			}
			soundio_ring_buffer_advance_read_ptr(ring, frames * bytes_per_frame);	// remove samples from ring buffer
		}
		if ((err = soundio_outstream_end_write(stream)) != 0) {
			if (err == SoundIoErrorUnderflow) {
				if (quisk_sound_state.verbose_sound)
					printf("%s:	 write_callback: write underflow min %d max %d\n",
						dev->stream_description, frame_count_min, frame_count_max);
				quisk_sound_state.underrun_error++;
				dev->dev_underrun++;
			}
			else {
				if (quisk_sound_state.verbose_sound)
					 printf("%s	 write_callback: unrecoverable stream error: %s\n",
						dev->stream_description, soundio_strerror(err));
				dev->dev_error++;
				return;
			}
		}
	}
}

static void read_callback(struct SoundIoInStream *stream, int frame_count_min, int frame_count_max)
{  // Read samples from the sound card and write them to the capture_buffer. Quisk will read them from there.
	struct SoundIoChannelArea * areas;
	struct sound_dev * dev = stream->userdata;
	struct dev_data_t * device_data;
	struct SoundIoRingBuffer * ring;
	int i, err, ring_max, fill_count, ch_I, ch_Q, bytes_per_sample;
	int frames, total_frames, bytes_per_frame;
	char * ptWrite;

	//QuiskPrintTime("read_callback", 0);
	if ( ! dev)
		return;
	device_data = dev->device_data;
	if ( ! device_data)
		return;
	ring = device_data->capture_buffer;
	if ( ! ring)
		return;
	if (quisk_play_state == STARTING)
		soundio_ring_buffer_clear(ring);
	bytes_per_frame = stream->bytes_per_frame;
	if (quisk_sound_state.verbose_sound >= 7) {
		fill_count = soundio_ring_buffer_fill_count(ring);
		printf("%s read_callback state %d, fill_frames %4d, frame_count_max %4d\n",
			dev->stream_description, quisk_play_state, fill_count / bytes_per_frame, frame_count_max);
	}
	ch_I = dev->channel_I;
	ch_Q = dev->channel_Q;
	bytes_per_sample = stream->bytes_per_sample;
	ring_max = soundio_ring_buffer_free_count(ring) / bytes_per_frame;
	if (frame_count_max >= ring_max) {
		if (quisk_sound_state.verbose_sound)
			printf("%s: the read_callback ring buffer has %d, need %d\n",
				dev->stream_description, ring_max, frame_count_max);
		ring = NULL;
		dev->dev_error++;
	}
	total_frames = frame_count_max;
	while(total_frames) {
		frames = total_frames;
		if ((err = soundio_instream_begin_read(stream, &areas, &frames))) {	// read the first "frames" frames
			if (quisk_sound_state.verbose_sound)
				printf("%s read_callback: unrecoverable stream error: %s\n", dev->stream_description, soundio_strerror(err));
			dev->dev_error++;
			return;
		}
		if ( ! areas) {		// hole in buffer
			;
		}
		else if (frames <= 0) {		// buffer is empty
			return;
		}
		else {
			total_frames -= frames;
		}
		if (areas && ring) {
			ptWrite = soundio_ring_buffer_write_ptr(ring);
			if (dev->num_channels == 2 && areas[1].ptr == areas[0].ptr + bytes_per_sample && areas[0].step == bytes_per_sample * 2 &&
					areas[1].step == bytes_per_sample * 2 && ch_I == 0 && ch_Q == 1) {	// check for interleaved and fast copy
				memcpy(ptWrite, areas[0].ptr, frames * bytes_per_frame);
			}
			else {
				for (i = 0; i < frames; i++) {
					memcpy(ptWrite, areas[ch_I].ptr, bytes_per_sample);
					areas[ch_I].ptr += areas[ch_I].step;
					ptWrite += bytes_per_sample;
					memcpy(ptWrite, areas[ch_Q].ptr, bytes_per_sample);
					areas[ch_Q].ptr += areas[ch_Q].step;
					ptWrite += bytes_per_sample;
				}
			}
			soundio_ring_buffer_advance_write_ptr(ring, frames * bytes_per_frame);
		}
		if ((err = soundio_instream_end_read(stream))) {
			if (quisk_sound_state.verbose_sound)
				printf("%s read_callback: unrecoverable stream error: %s\n", dev->stream_description, soundio_strerror(err));
			dev->dev_error++;
			return;
		}
	}
}

int quisk_read_soundio(struct sound_dev * dev, complex double * cSamples)
{	// Called from Quisk by the sound thread. Read samples from the sound card capture capture_buffer.
	// The capture_buffer always stores samples as: IQIQIQIQ...
	// cSamples can be NULL to discard samples.
	struct dev_data_t * device_data;
	struct SoundIoRingBuffer * ring;
	int i;
	float timer;
	int frames, bytes_per_frame;
	float samp_r, samp_i;
	int16_t * ptInt16;
	int32_t * ptInt32;
	float   * ptFloat32;

	device_data = dev->device_data;
	if ( ! device_data)
		return 0;
	ring = device_data->capture_buffer;
	if ( ! ring)
		return 0;
	bytes_per_frame = dev->sample_bytes * dev->num_channels;
	frames = soundio_ring_buffer_fill_count(ring) / bytes_per_frame;	// available frames
	if (dev->read_frames > 0) {	// blocking read
		timer = (float)(dev->read_frames - frames) / dev->sample_rate;
		if (timer > 0.001 && timer < 0.100)
			QuiskSleepMicrosec((int)(timer * 1E6));
		frames = soundio_ring_buffer_fill_count(ring) / bytes_per_frame;
	}
	if (cSamples) switch (dev->sound_format) {
	case Int16:
		ptInt16 = (int16_t *)soundio_ring_buffer_read_ptr(ring);
		for (i = 0; i < frames; i++) {
			samp_r = *ptInt16++;
			samp_i = *ptInt16++;
			cSamples[i] = (samp_r + I * samp_i) * CLIP16;
		}
		break;
	case Int24:
		break;
	case Int32:
		ptInt32 = (int32_t *)soundio_ring_buffer_read_ptr(ring);
		for (i = 0; i < frames; i++) {
			samp_r = *ptInt32++;
			samp_i = *ptInt32++;
			cSamples[i] = (samp_r + I * samp_i);
		}
		break;
	case Float32:
		ptFloat32 = (float *)soundio_ring_buffer_read_ptr(ring);
		for (i = 0; i < frames; i++) {
			samp_r = *ptFloat32++;
			samp_i = *ptFloat32++;
			cSamples[i] = (samp_r + I * samp_i) * CLIP32;
		}
		break;
	}
	soundio_ring_buffer_advance_read_ptr(ring, frames * bytes_per_frame);
	return frames;
}

void quisk_write_soundio(struct sound_dev * dev, int nSamples, complex double * cSamples)
{	// Called from Quisk by the sound thread. Write samples to the sound card play_buffer.
	// The ring buffer always stores samples as: IQIQIQIQ...
	struct dev_data_t * device_data;
	struct SoundIoRingBuffer * ring;
	int i, bytes_per_frame, capacity, fill_count;
	float fill;
	int16_t * ptInt16;
	int32_t * ptInt32;
	float   * ptFloat;
	static int timer = 999999;

	if ( ! dev)
		return;
	device_data = dev->device_data;
	if ( ! device_data)
		return;
	ring = device_data->play_buffer;
	if ( ! ring)
		return;

	soundio_flush_events(device_data->soundio);
	//QuiskPrintTime("write play buffer", 0);
	bytes_per_frame = dev->sample_bytes * dev->num_channels;
	capacity = soundio_ring_buffer_capacity(ring);
	fill_count = soundio_ring_buffer_fill_count(ring);
	if (quisk_sound_state.verbose_sound > 1) {
		if (quisk_sound_state.verbose_sound >= 2) {
			timer += nSamples;
			if (timer > dev->sample_rate) {
				timer = 0;
				fill = (float)(fill_count) / capacity;
				printf("%s: play_buffer state %d, fill level %.2f%%\n",
					dev->stream_description, quisk_play_state, fill * 100.0);
			}
		}
		if (quisk_sound_state.verbose_sound == 4) {
			QuiskMeasureRate("play_buffer", nSamples, 1);
		}
		if (quisk_sound_state.verbose_sound >= 9) {
			printf("%s: play_buffer state %d, fill_frames %4d, nSamples %4d\n",
				dev->stream_description, quisk_play_state, fill_count / bytes_per_frame, nSamples);
		}
	}
	if (quisk_play_state == STARTING) {
		device_data->buffer_write_restart = 0;
		soundio_ring_buffer_clear(ring);
		return;
	}
	if (device_data->buffer_write_restart) {
		if (fill_count < capacity / 2) {
			device_data->buffer_write_restart = 0;
			if (quisk_sound_state.verbose_sound)
				printf("%s: play_buffer overflow recovery\n", dev->stream_description);
		}
		else
			return;
	}
	if (fill_count + nSamples * bytes_per_frame >= capacity) {
		device_data->buffer_write_restart = 1;
		if (quisk_sound_state.verbose_sound)
			printf("%s: play_buffer overflow\n", dev->stream_description);
		dev->dev_error++;
		       return;
	}
	if (nSamples > 2) {
		if (fill_count + nSamples * bytes_per_frame > capacity * 7 / 10) {
			nSamples--;	// buffer too full, remove a sample
		}
		else if (fill_count + nSamples * bytes_per_frame < capacity * 3 / 10) {
			cSamples[nSamples] = cSamples[nSamples - 1];
			cSamples[nSamples - 1] = (cSamples[nSamples - 2] + cSamples[nSamples]) / 2.0;
			nSamples++;	// buffer too empty, add a sample
		}
	}
	switch (dev->sound_format) {
	case Int16:
		ptInt16 = (int16_t *)soundio_ring_buffer_write_ptr(ring);
		for (i = 0; i < nSamples; i++) {		// for each frame
			*ptInt16++ = quisk_audioVolume * creal(cSamples[i]) / 65536;
			*ptInt16++ = quisk_audioVolume * cimag(cSamples[i]) / 65536;
		}
		break;
	case Int24:
		break;
	case Int32:
		ptInt32 = (int32_t *)soundio_ring_buffer_write_ptr(ring);
		for (i = 0; i < nSamples; i++) {
			*ptInt32++ = quisk_audioVolume * creal(cSamples[i]);
			*ptInt32++ = quisk_audioVolume * cimag(cSamples[i]);
		}
		break;
	case Float32:
		ptFloat = (float *)soundio_ring_buffer_write_ptr(ring);
		for (i = 0; i < nSamples; i++) {
			*ptFloat++ = quisk_audioVolume * creal(cSamples[i]) / CLIP32;
			*ptFloat++ = quisk_audioVolume * cimag(cSamples[i]) / CLIP32;
		}
		break;
	}
	soundio_ring_buffer_advance_write_ptr(ring, nSamples * bytes_per_frame);
}

static struct SoundIoDevice * open_device(struct SoundIo * soundio, struct sound_dev * dev)
{
	enum SoundIoBackend backend;
	int i, err, device_count;
	struct SoundIoDevice * devtmp, * device;
	const struct SoundIoChannelLayout * layout;
#ifdef MS_WINDOWS
	backend = SoundIoBackendWasapi;
#else
	backend = SoundIoBackendAlsa;
#endif
	if (quisk_sound_state.verbose_sound) {
		if (dev->stream_dir_record)	// capture
			printf("Opening SoundIO capture device %s\n  Name %s\n  Device name %s\n", dev->stream_description, dev->name, dev->device_name);
		else
			printf("Opening SoundIO playback device %s\n  Name %s\n  Device name %s\n", dev->stream_description, dev->name, dev->device_name);
	}
	err = soundio_connect_backend(soundio, backend);
	if (err) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Unable to connect to backend: %s", soundio_strerror(err));
		if (quisk_sound_state.verbose_sound) printf("  %s\n", dev->dev_errmsg);
		return NULL;
	}
	soundio_flush_events(soundio);
	device = NULL;
	if (dev->stream_dir_record) {	// capture
		device_count = soundio_input_device_count(soundio);
		for (i = 0; i < device_count && device == NULL; i++) {
			devtmp = soundio_get_input_device(soundio, i);
			if (devtmp->probe_error)
				;
#ifdef MS_WINDOWS
			else if (devtmp->is_raw && strcmp(devtmp->id, dev->device_name) == 0)
#else
			else if (strcmp(devtmp->id, dev->device_name) == 0)
#endif
				device = devtmp;
			else
				soundio_device_unref(devtmp);
		}
	}
	else {		// playback
		device_count = soundio_output_device_count(soundio);
		for (i = 0; i < device_count && device == NULL; i++) {
			devtmp = soundio_get_output_device(soundio, i);
			if (devtmp->probe_error)
				;
#ifdef MS_WINDOWS
			else if (devtmp->is_raw && strcmp(devtmp->id, dev->device_name) == 0)
#else
			else if (strcmp(devtmp->id, dev->device_name) == 0)
#endif
				device = devtmp;
			else
				soundio_device_unref(devtmp);
		}
	}
	if ( ! device) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Sound device not found: %.80s", dev->device_name);
		if (quisk_sound_state.verbose_sound) printf("  %.40s for name %.40s device %.80s\n", dev->dev_errmsg, dev->name, dev->device_name);
		return NULL;
	}
	if (quisk_sound_state.verbose_sound) {
		printf("  Supported formats:");
		for (i = 0; i < device->format_count; i++)
			printf("   %s   ", soundio_format_string(device->formats[i]));
		printf("\n");
		printf("  Supported sample rates:");
		if (soundio_device_supports_sample_rate(device, 48000))
			printf(" 48000");
		if (soundio_device_supports_sample_rate(device, 96000))
			printf(" 96000");
		if (soundio_device_supports_sample_rate(device, 192000))
			printf(" 192000");
		printf("\n");
		printf("  Supports %d layouts:", device->layout_count);
		for (i = 0; i < device->layout_count; i++) {
			layout = &device->layouts[i];
			if (layout->name)
				printf(" %s[%d chan]", layout->name, layout->channel_count);
			else
				printf(" NoName[%d chan]", layout->channel_count);
		}
		printf("\n");
		printf ("  Latency %.3lf %.3lf\n", device->software_latency_min, device->software_latency_max);
	}
	return device;
}

static int channel_min_max(struct SoundIoDevice * device, struct sound_dev * dev)
{
	int i, index, index_smallest, index_mono, count, smallest;

	if (device->layout_count <= 0)
		printf("Error: device provides no layouts\n");	// should never happen
	index_smallest = -1;
	index_mono = -1;
	smallest = 999;
	for (i = 0; i < device->layout_count; i++) {
		count = device->layouts[i].channel_count;
		if (count == 1)
			index_mono = i;
		if (count >= dev->num_channels) {	// this layout has enough channels
			if (count < smallest) {	// use the smallest layout
				index_smallest = i;
				smallest = count;
			}
		}
	}
	if (index_smallest >= 0) {
		index = index_smallest;
	}
	else if ((dev->dev_index == t_Playback || dev->dev_index == t_MicCapture) && index_mono >= 0) {	// mono device is OK for radio sound or mic
		index = index_mono;
		dev->channel_I = 0;
		dev->channel_Q = 0;
	}
	else {
		index = 0;	// just use the first layout
		printf("Error: This device does not support %d channels as requested\n", dev->num_channels);
		dev->channel_I = 0;
		dev->channel_Q = 0;
	}
	dev->num_channels = device->layouts[index].channel_count;	// This may increase num_channels
	return index;
}

static void open_soundio_capture(struct sound_dev * dev)
{
	int err;
	double latency;
	enum SoundIoFormat format;
	struct SoundIo * soundio;
	struct SoundIoDevice * device;
	struct SoundIoInStream * stream;
	struct dev_data_t * device_data;

	dev->dev_errmsg[0] = 0;
	soundio = soundio_create();
	if (!soundio) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Can not create soundio");
		if (quisk_sound_state.verbose_sound) printf("%s\n", dev->dev_errmsg);
		return;
	}
	device = open_device(soundio, dev);
	if ( ! device) {
		soundio_destroy(soundio);
		return;
	}
	stream = soundio_instream_create(device);
	if ( ! stream) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Cannot create the stream");
		if (quisk_sound_state.verbose_sound) printf("  %s\n", dev->dev_errmsg);
		soundio_device_unref(device);
		soundio_destroy(soundio);
		return;
	}
	format = choose_format(dev, device);
	if (format == SoundIoFormatInvalid) {
		soundio_instream_destroy(stream);
		soundio_device_unref(device);
		soundio_destroy(soundio);
		return;
	}
	if (dev->dev_index == t_Capture)	// capture samples
		latency = quisk_sound_state.data_poll_usec * 1E-6;
	else
		latency = quisk_sound_state.latency_millisecs * 1E-3;
	if (latency < device->software_latency_min)
		latency = device->software_latency_min;
	else if (latency > device->software_latency_max)
		latency = device->software_latency_max;
	if (quisk_sound_state.verbose_sound) {
		printf("  Using format %s\n", soundio_format_string(format));
		printf("  Using sample rate %d\n", dev->sample_rate);
		printf("  Request latency %.6f sec\n", latency);
	}
	stream->format = format;
	stream->read_callback = read_callback;
	stream->overflow_callback = overflow_callback;
	stream->error_callback = error_callback_in;
	stream->name = dev->stream_description;
	stream->software_latency = latency;
	stream->sample_rate = dev->sample_rate;
	stream->userdata = dev;
	stream->layout = device->layouts[channel_min_max(device, dev)];
	if ((err = soundio_instream_open(stream))) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Unable to open device: %s", soundio_strerror(err));
		if (quisk_sound_state.verbose_sound) {
			if (stream->layout_error)
				printf("  Layout error %d\n", stream->layout_error);
			printf("  %s\n", dev->dev_errmsg);
		}
		soundio_instream_destroy(stream);
		soundio_device_unref(device);
		soundio_destroy(soundio);
		return;
	}
	if (quisk_sound_state.verbose_sound) {
		printf("  Software latency: %f\n", stream->software_latency);
		if (stream->layout.name)
			printf("  Using %d channels layout %s\n", stream->layout.channel_count, stream->layout.name);
		else
			printf("  Using %d channels layout <no name>\n", stream->layout.channel_count);
	}
	if (stream->layout_error) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Unable to set channel layout: %s", soundio_strerror(stream->layout_error));
		if (quisk_sound_state.verbose_sound) printf("  %s\n", dev->dev_errmsg);
	}
	device_data = malloc(sizeof(struct dev_data_t));
	device_data->soundio = soundio;
	device_data->device = device;
	device_data->instream = stream;
	device_data->outstream = NULL;
	device_data->capture_buffer = soundio_ring_buffer_create(soundio, dev->sample_rate * dev->sample_bytes * dev->num_channels / 4);
	device_data->play_buffer = NULL;
	device_data->buffer_read_restart = 0;
	device_data->buffer_write_restart = 0;
	dev->device_data = device_data;
	dev->handle = soundio;
	if ((err = soundio_instream_start(stream))) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Unable to start device: %s", soundio_strerror(err));
		if (quisk_sound_state.verbose_sound) printf("  %s\n", dev->dev_errmsg);
		soundio_instream_destroy(stream);
		soundio_device_unref(device);
		soundio_destroy(soundio);
		return;
	}
	if (quisk_sound_state.verbose_sound)
		printf("  Success opening capture device %s\n", dev->stream_description);
}

static void open_soundio_playback(struct sound_dev * dev)
{
	int err;
	double latency;
	enum SoundIoFormat format;
	struct SoundIo * soundio;
	struct SoundIoDevice * device;
	struct SoundIoOutStream * stream;
	struct dev_data_t * device_data;

	dev->dev_errmsg[0] = 0;
	soundio = soundio_create();
	if (!soundio) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Can not create soundio");
		if (quisk_sound_state.verbose_sound) printf("%s\n", dev->dev_errmsg);
		return;
	}
	device = open_device(soundio, dev);
	if ( ! device) {
		soundio_destroy(soundio);
		return;
	}
	stream = soundio_outstream_create(device);
	if ( ! stream) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Cannot create the stream");
		if (quisk_sound_state.verbose_sound) printf("  %s\n", dev->dev_errmsg);
		soundio_device_unref(device);
		soundio_destroy(soundio);
		return;
	}
	format = choose_format(dev, device);
	if (format == SoundIoFormatInvalid) {
		soundio_outstream_destroy(stream);
		soundio_device_unref(device);
		soundio_destroy(soundio);
		return;
	}
	if (dev->dev_index == t_Playback || dev->dev_index == t_MicPlayback)	// radio sound playback or Mic playback with CW samples
		latency = quisk_sound_state.data_poll_usec * 1E-6;
	else
		latency = quisk_sound_state.latency_millisecs * 1E-3;
	if (latency < device->software_latency_min)
		latency = device->software_latency_min;
	else if (latency > device->software_latency_max)
		latency = device->software_latency_max;
	if (quisk_sound_state.verbose_sound) {
		printf("  Using format %s\n", soundio_format_string(format));
		printf("  Using sample rate %d\n", dev->sample_rate);
		printf("  Latency min %.6f max %.6f sec\n", device->software_latency_min, device->software_latency_max);
		printf("  Request latency %.6f sec\n", latency);
	}
	stream->format = format;
	stream->write_callback = write_callback;
	stream->underflow_callback = underflow_callback;
	stream->error_callback = error_callback_out;
	stream->name = dev->stream_description;
	stream->software_latency = latency;
	stream->sample_rate = dev->sample_rate;
	stream->userdata = dev;
	stream->layout = device->layouts[channel_min_max(device, dev)];
	if ((err = soundio_outstream_open(stream))) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Unable to open device: %s", soundio_strerror(err));
		if (quisk_sound_state.verbose_sound) {
			if (stream->layout_error)
				printf("  Layout error %d\n", stream->layout_error);
			printf("  %s\n", dev->dev_errmsg);
		}
		soundio_outstream_destroy(stream);
		soundio_device_unref(device);
		soundio_destroy(soundio);
		return;
	}
	if (quisk_sound_state.verbose_sound) {
		printf("  Latency min %.6f max %.6f sec\n", device->software_latency_min, device->software_latency_max);
		printf("  Software latency: %f\n", stream->software_latency);
		if (stream->layout.name)
			printf("  Using %d channels layout %s\n", stream->layout.channel_count, stream->layout.name);
		else
			printf("  Using %d channels layout <no name>\n", stream->layout.channel_count);
	}
	if (stream->layout_error) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Unable to set channel layout: %s", soundio_strerror(stream->layout_error));
		if (quisk_sound_state.verbose_sound) printf("  %s\n", dev->dev_errmsg);
	}
	device_data = malloc(sizeof(struct dev_data_t));
	device_data->soundio = soundio;
	device_data->device = device;
	device_data->instream = NULL;
	device_data->outstream = stream;
	device_data->capture_buffer = NULL;
	device_data->play_buffer = soundio_ring_buffer_create(soundio, dev->latency_frames * dev->sample_bytes * dev->num_channels * 2);
	device_data->buffer_read_restart = 0;
	device_data->buffer_write_restart = 0;
	dev->device_data = device_data;
	dev->handle = soundio;
	if ((err = soundio_outstream_start(stream))) {
		snprintf(dev->dev_errmsg, QUISK_SC_SIZE, "Unable to start device: %s", soundio_strerror(err));
		if (quisk_sound_state.verbose_sound) printf("  %s\n", dev->dev_errmsg);
		soundio_outstream_destroy(stream);
		soundio_device_unref(device);
		soundio_destroy(soundio);
		return;
	}
	if (quisk_sound_state.verbose_sound)
		printf("  Success opening playback device %s\n", dev->stream_description);
}

void quisk_start_sound_soundio (struct sound_dev ** pCapture, struct sound_dev ** pPlayback)
{  // Open the sound devices and start them. Called from the sound thread.
	struct sound_dev * pDev;

	while (*pCapture) {
		pDev = *pCapture++;
		if (pDev->driver == DEV_DRIVER_SOUNDIO) {
			pDev->device_data = NULL;	// this should already be NULL
			open_soundio_capture(pDev);
		}
	}
	while (*pPlayback) {
		pDev = *pPlayback++;
		if (pDev->driver == DEV_DRIVER_SOUNDIO) {
			pDev->device_data = NULL;	// this should already be NULL
			open_soundio_playback(pDev);
		}
	}
}

void quisk_close_sound_soundio(struct sound_dev ** pCapture, struct sound_dev ** pPlayback)
{
	struct sound_dev * pDev;

	while (*pCapture) {
		pDev = *pCapture++;
		if (pDev->driver == DEV_DRIVER_SOUNDIO && pDev->device_data) {
			struct dev_data_t * device_data = pDev->device_data;
			soundio_instream_destroy(device_data->instream);
			soundio_device_unref	(device_data->device);
			soundio_disconnect	(device_data->soundio);
			soundio_ring_buffer_destroy(device_data->capture_buffer);
			soundio_destroy		(device_data->soundio);
			free(pDev->device_data);
			pDev->device_data = NULL;
			pDev->handle = NULL;
			if (quisk_sound_state.verbose_sound)
				printf("Close %s\n", pDev->stream_description);
		}
	}
	while (*pPlayback) {
		pDev = *pPlayback++;
		if (pDev->driver == DEV_DRIVER_SOUNDIO && pDev->device_data) {
			struct dev_data_t * device_data = pDev->device_data;
			soundio_outstream_destroy(device_data->outstream);
			soundio_device_unref	(device_data->device);
			soundio_disconnect	(device_data->soundio);
			soundio_ring_buffer_destroy(device_data->play_buffer);
			soundio_destroy		(device_data->soundio);
			free(pDev->device_data);
			pDev->device_data = NULL;
			pDev->handle = NULL;
			if (quisk_sound_state.verbose_sound)
				printf("Close %s\n", pDev->stream_description);
		}
	}
}

static void add_device(struct SoundIoDevice * device, PyObject * pylist)
{
	PyObject * pytup;

	if (device->probe_error)
		return;
	// data items are (name, id, is_raw)
	pytup = PyTuple_New(3);
	PyList_Append(pylist, pytup);
	PyTuple_SET_ITEM(pytup, 0, PyUnicode_FromString(device->name));
	PyTuple_SET_ITEM(pytup, 1, PyUnicode_FromString(device->id));
	PyTuple_SET_ITEM(pytup, 2, PyInt_FromLong(device->is_raw));
}

PyObject * quisk_sio_sound_devices(PyObject * self, PyObject * args)
{	// Return a list of sound device data [pycapt, pyplay]
	PyObject * pylist, * pycapt, * pyplay;
	int err, count;
	const char * bkend;
	enum SoundIoBackend backend;
	struct SoundIoDevice * device;
	struct SoundIo * soundio;

	if (!PyArg_ParseTuple (args, "s", &bkend))
		return NULL;
	pylist = PyList_New(0);		// list [pycapt, pyplay]
	pycapt = PyList_New(0);		// list of capture devices
	pyplay = PyList_New(0);		// list of play devices
	PyList_Append(pylist, pycapt);
	PyList_Append(pylist, pyplay);

	soundio = soundio_create();
	if ( ! soundio)
		return pylist;
	backend = text2backend(bkend);
	err = soundio_connect_backend(soundio, backend);
	if (err)
		return pylist;
	soundio_flush_events(soundio);
	count = soundio_input_device_count(soundio);
	for (int i = 0; i < count; i++) {
		device = soundio_get_input_device(soundio, i);
		add_device(device, pycapt);
		soundio_device_unref(device);
	}
	count = soundio_output_device_count(soundio);
	for (int i = 0; i < count; i++) {
		device = soundio_get_output_device(soundio, i);
		add_device(device, pyplay);
		soundio_device_unref(device);
	}
	soundio_destroy(soundio);
	return pylist;
}

