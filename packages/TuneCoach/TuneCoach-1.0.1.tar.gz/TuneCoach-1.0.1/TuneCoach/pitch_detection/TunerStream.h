#pragma once
#include <atomic>
#include "CircularBuffer.h"
#include "PitchDetector.h"

#ifdef USE_PULSE
#include <pulse/simple.h>
#endif
#ifdef USE_ALSA
#define ALSA_PCM_NEW_HW_PARAMS_API
#include <alsa/asoundlib.h>
#endif

class TunerStream
{
public:
    TunerStream(int sample_rate);
    void mainloop();
    void pause();
    void resume();
    void kill();
    bool isSafeToDelete();
    bool isAlive();
    bool isPaused();
    bool fetch_freq(double& hz);
    double peek();

    ~TunerStream();

private:
    std::atomic_bool alive;
    std::atomic_bool paused;
    std::atomic_bool was_started;
    std::atomic_bool safe_to_delete;
    CircularBuffer<double, 4096> buffer;
    std::atomic<double> most_recent;
    PitchDetector* p;

    unsigned int sample_rate;
    int audio_buffer_size = 2048;
    float* audio_buffer;

#ifdef USE_ALSA
    snd_pcm_t *handle;
#endif
#ifdef USE_PULSE
    pa_simple *server;
#endif
};
