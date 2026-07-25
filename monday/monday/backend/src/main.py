from pathlib import Path



from audio_io import listen_once
from speaker import speak
from agent import build_graph



def should_exit(text):
    text = text.lower()
    return text in ["exit", "quit", "bye", "goodbye"]

def main():
    app = build_graph()
    print("Starting the assistant...")
    print("Ask me about coding, cooking, tarot or anything else")
    print(" Say 'stop' or 'exit' to stop the assistant")
    while True:
        user_text = listen_once()
        if not user_text:
            print("No audio detected, try again")
            continue
        print(f"User said: {user_text}")
        if should_exit(user_text):
            reply = "Goodbye"
            print(f"assistant: {reply}")
            speak(reply)
            break
        result = app.invoke({"user_text": user_text})
        reply = result.get("final_answer", "I'm sorry, I don't know how to help with that.")
        print(f"assistant: {reply}")
        speak(reply)


if __name__ == "__main__":
    main()
