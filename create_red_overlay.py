def create_red_overlay(widget, alpha=0.35, duration=2000):
    """
    Create a fuzzy red overlay on top of a widget.

    :param widget: The widget to overlay.
    :param alpha: The initial transparency level of the overlay (0.0 to 1.0).
    :param duration: The duration of the fade-out effect in milliseconds.
    """
    # Get the dimensions and position of the widget
    original_x = widget.winfo_rootx()
    original_y = widget.winfo_rooty()
    original_width = widget.winfo_width()
    original_height = widget.winfo_height()

    # Create a translucent overlay with a red background
    overlay = tk.Toplevel(widget)
    overlay.overrideredirect(True)
    overlay.geometry(f"{original_width}x{original_height}+{original_x}+{original_y}")
    overlay.configure(bg="red")  # Set the background color to red
    overlay.attributes("-alpha", alpha)  # Set initial transparency level

    def fade_out(alpha):
        current_alpha = overlay.attributes("-alpha")
        new_alpha = current_alpha - (1.0 / duration)  # Decrease alpha gradually based on the duration
        if new_alpha > 0:
            overlay.attributes("-alpha", new_alpha)
            overlay.after(1, fade_out, new_alpha)  # Call fade_out function recursively
        else:
            overlay.destroy()

    overlay.after(0, fade_out, 1.0)  # Start the fade-out immediately