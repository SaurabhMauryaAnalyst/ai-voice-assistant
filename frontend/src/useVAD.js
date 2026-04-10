// Voice Activity Detection hook using @ricky0123/vad-web (Silero VAD)
// Detects when the user starts and stops speaking
import { useMemo, useRef, useCallback } from 'react';
import { MicVAD } from '@ricky0123/vad-web';

export function useVAD({ onSpeechStart, onSpeechEnd, onFrameProcessed }) {
  const vadRef = useRef(null);

  const start = useCallback(async () => {
    if (vadRef.current) return;

    vadRef.current = await MicVAD.new({
      // Fires when voice detected — open WS stream
      onSpeechStart: () => {
        console.log('[VAD] Speech started');
        onSpeechStart?.();
      },
      // Fires after 800ms silence — end utterance
      onSpeechEnd: (audio) => {
        console.log('[VAD] Speech ended, samples:', audio.length);
        onSpeechEnd?.(audio);   // audio = Float32Array PCM
      },
      // Optional: receive each 30ms frame for streaming STT
      onFrameProcessed: (probs) => {
        onFrameProcessed?.(probs);
      },
      positiveSpeechThreshold: 0.85,
      negativeSpeechThreshold: 0.20,
      minSpeechFrames: 4,
      preSpeechPadFrames: 3,
    });

    await vadRef.current.start();
  }, [onSpeechStart, onSpeechEnd, onFrameProcessed]);

  const stop = useCallback(() => {
    vadRef.current?.destroy();
    vadRef.current = null;
  }, []);

  return { start, stop };
}