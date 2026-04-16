import React,{useState} from "react"
import useWebSocket from "./useWebSocket"

export default function VoiceAssistant(){

  const {startListening,stopListening} = useWebSocket()

  const [status,setStatus] = useState("idle")

  return(

    <div>

      <div>
        Status: {status}
      </div>

      <button
        onClick={()=>{
          startListening()
          setStatus("listening")
        }}
      >
        Start Listening
      </button>

      <button
        onClick={()=>{
          stopListening()
          setStatus("idle")
        }}
      >
        Stop
      </button>

    </div>

  )

}