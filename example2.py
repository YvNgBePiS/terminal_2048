from sshkeyboard import listen_keyboard, stop_listening

def press(key):
    print(f"'{key}' pressed")
    if key == "z":
        stop_listening()

listen_keyboard(on_press=press)