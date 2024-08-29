CoordMode, Mouse, Screen  ; Ensure coordinates are relative to the screen

Value := 9001  ; Starting value
Loop, 253  ; Number of times to repeat
{
    Click, 2006, 824  ; Move mouse to the input field based on screen coordinates
    Send, %Value%
    Click, 1970, 830  ; Click the Apply button based on screen coordinates
    Value++  ; Increment the value
    Sleep, 20  ; Optional: Add a delay if needed
}
