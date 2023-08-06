import os
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import wavfile


def envelope(y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    y_mean = y.rolling(window=int(rate / 20),
                       min_periods=1,
                       center=True).max()
    for mean in y_mean:
        if mean > float(threshold):
            mask.append(True)
        else:
            mask.append(False)
    return mask, y_mean


def save_sample(sample, rate, target_dir, fn, ix):
    fn = fn.split('.wav')[0]
    dst_path = os.path.join(target_dir.split('.')[0], fn + '_{}.wav'.format(str(ix)))
    if os.path.exists(dst_path):
        return
    wavfile.write(dst_path, rate, sample)


def split_wavs(wav, rate, delta_time, threshold):
    wav = downsample_mono(wav, rate)
    mask, y_mean = envelope(wav, rate, threshold=threshold)
    wav = wav[mask]
    delta_sample = int(delta_time * rate)
    samples = []
    # cleaned audio is less than a single sample
    # pad with zeros to delta_sample size
    if wav.shape[0] < delta_sample:
        sample = np.zeros(shape=(delta_sample,), dtype=np.int16)
        sample[:wav.shape[0]] = wav
        samples.append(sample)
    # step through audio and save every delta_sample
    # discard the ending audio if it is too short
    else:
        trunc = wav.shape[0] % delta_sample
        for cnt, i in enumerate(np.arange(0, wav.shape[0] - trunc, delta_sample)):
            start = int(i)
            stop = int(i + delta_sample)
            sample = wav[start:stop]
            samples.append(sample)
    return samples


def test_threshold(args):
    src_root = args.src_root
    wav_paths = glob('{}/**'.format(src_root), recursive=True)
    wav_path = [x for x in wav_paths if args.fn in x]
    if len(wav_path) != 1:
        print('audio file not found for sub-string: {}'.format(args.fn))
        return
    rate, wav = downsample_mono(wav_path[0], args.sr)
    mask, env = envelope(wav, rate, threshold=args.threshold)
    plt.style.use('ggplot')
    plt.title('Signal Envelope, Threshold = {}'.format(str(args.threshold)))
    plt.plot(wav[np.logical_not(mask)], color='r', label='remove')
    plt.plot(wav[mask], color='c', label='keep')
    plt.plot(env, color='m', label='envelope')
    plt.grid(False)
    plt.legend(loc='best')
    plt.show()
