import { useRef, useCallback } from 'react';

const WS_URL = import.meta.env.VITE_WS_URL || 'wss://api.yourdomain.com/ws/voice';

export function useWebSocket({ onTranscript, onAudioChunk, onAssistantDone }) {
  const wsRef = useRef(null);
  const sessionId = useRef(crypto.randomUUID());

  const connect = useCallback(() => {
    const ws = new WebSocket(
      `${WS_URL}?session=${sessionId.current}`
    );
    ws.binaryType = 'arraybuffer';

    ws.onmessage = (event) => {
      if (typeof event.data === 'string') {
        const msg = JSON.parse(event.data);
        if (msg.type === 'transcript')    onTranscript?.(msg.text);
        if (msg.type === 'assistant_done') onAssistantDone?.();
      } else {
        // Binary = MP3 audio chunk from Polly
        onAudioChunk?.(event.data);
      }
    };

    wsRef.current = ws;
    return ws;
  }, [onTranscript, onAudioChunk, onAssistantDone]);

  // Send raw Float32 PCM audio to backend
  const sendAudio = useCallback((float32Array) => {
    const ws = wsRef.current;
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(float32Array.buffer);
    }
  }, []);

  // Tell backend to stop generating (user interrupted)
  const sendStop = useCallback(() => {
    wsRef.current?.send(JSON.stringify({ type: 'stop' }));
  }, []);

  const sendEndUtterance = useCallback(() => {
    wsRef.current?.send(JSON.stringify({ type: 'end_utterance' }));
  }, []);

  const disconnect = useCallback(() => {
    wsRef.current?.close();
  }, []);

  return { connect, sendAudio, sendStop, sendEndUtterance, disconnect };
}