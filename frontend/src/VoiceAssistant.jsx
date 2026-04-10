import { useState, useCallback, useRef, useEffect } from 'react';
import { useVAD } from './useVAD';
import { useWebSocket } from './useWebSocket';

export default function VoiceAssistant() {
  const [status, setStatus] = useState('idle');
  // idle | listening | processing | speaking
  const [transcript, setTranscript] = useState('');
  const [reply, setReply]   = useState('');
  const audioQueue = useRef([]);
  const isPlaying  = useRef(false);
  const audioCtx   = useRef(null);

  // Play queued MP3 chunks sequentially
  const playNextChunk = useCallback(async () => {
    if (isPlaying.current || audioQueue.current.length === 0) return;
    isPlaying.current = true;
    const chunk = audioQueue.current.shift();
    const ctx = audioCtx.current || (audioCtx.current = new AudioContext());
    const buffer = await ctx.decodeAudioData(chunk);
    const source = ctx.createBufferSource();
    source.buffer = buffer;
    source.connect(ctx.destination);
    source.start();
    source.onended = () => {
      isPlaying.current = false;
      playNextChunk();  // play next queued chunk
    };
  }, []);

  const { connect, sendAudio, sendStop, sendEndUtterance } = useWebSocket({
    onTranscript: (t) => setTranscript(t),
    onAudioChunk: (chunk) => {
      setStatus('speaking');
      audioQueue.current.push(chunk);
      playNextChunk();
    },
    onAssistantDone: () => setStatus('listening'),
  });

  // VAD callbacks
  const onSpeechStart = useCallback(() => {
    if (status === 'speaking') {
      // User interrupted — stop assistant immediately
      audioCtx.current?.suspend();
      audioQueue.current = [];
      sendStop();
    }
    setStatus('listening');
    setReply('');
    connect();  // open WS
  }, [status, sendStop, connect]);

  const onSpeechEnd = useCallback((audio) => {
    setStatus('processing');
    sendAudio(audio);
    sendEndUtterance();  // signal backend to process
  }, [sendAudio, sendEndUtterance]);

  const { start: startVAD, stop: stopVAD } = useVAD({ onSpeechStart, onSpeechEnd });

  return (
    <div className="assistant-container">
      <div className={`orb orb--${status}`} />
      <p className="status-label">{status}</p>
      <p className="transcript">{transcript}</p>
      <p className="reply">{reply}</p>
      <button onClick={startVAD}>Start Listening</button>
      <button onClick={stopVAD}>Stop</button>
    </div>
  );
}