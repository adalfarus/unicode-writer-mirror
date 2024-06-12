from pynput import keyboard

# current set of pressed keys
current_keys = set()

# string to collect numbers
number_string = ''

controller = keyboard.Controller()

def on_press(key):
    if key == keyboard.Key.alt_gr or key == keyboard.Key.alt_l:
        current_keys.add(key)
    elif current_keys: # check if either alt key is pressed
        try:
            char = key.char.lower()
            if char.isdigit() or char in 'abcdef':
                global number_string
                number_string += char
        except AttributeError:
            pass # non-integer key pressed, we can ignore it

def on_release(key):
    global number_string
    if key == keyboard.Key.alt_gr or key == keyboard.Key.alt_l:
        if number_string:
            try:
                # decode and print Unicode character
                unicode_int = int(number_string, 16)  # interpret as hexadecimal
                if 0 <= unicode_int <= 0x10FFFF:
                    controller.type(chr(unicode_int))
                else:
                    print(f"Error: {number_string} (interpreted as {unicode_int}) is not a valid Unicode code point.")
            except ValueError:
                print(f"Error: {number_string} is not a valid hexadecimal integer.")
            number_string = ''
        current_keys.clear()

# listen to the keyboard
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
