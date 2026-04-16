import { useRef } from "react"

export default function useWebSocket() {

  const wsRef = useRef(null)
  const recorderRef = useRef(null)
  const chunksRef = useRef([])

  const startListening = async () => {

    // always create new websocket
    const ws = new WebSocket("ws://localhost:8000/ws/voice")

    ws.binaryType = "arraybuffer"

    ws.onopen = () => {
      console.log("WebSocket connected")
    }

    ws.onmessage = async (event) => {

      const blob = new Blob([event.data], { type: "audio/wav" })
      const url = URL.createObjectURL(blob)

      const audio = new Audio(url)
      await audio.play()
    }

    ws.onclose = () => {
      console.log("WebSocket closed")
    }

    wsRef.current = ws

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

    const recorder = new MediaRecorder(stream, { mimeType: "audio/webm" })

    recorderRef.current = recorder
    chunksRef.current = []

    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunksRef.current.push(event.data)
      }
    }

    recorder.start()
  }


  const stopListening = async () => {

    const recorder = recorderRef.current
    const ws = wsRef.current

    if (!recorder || !ws) return

    recorder.stop()

    recorder.onstop = async () => {

      const blob = new Blob(chunksRef.current, { type: "audio/webm" })
      const buffer = await blob.arrayBuffer()

      ws.send(buffer)
      ws.send("stop")

      chunksRef.current = []
    }
  }

  return { startListening, stopListening }
}