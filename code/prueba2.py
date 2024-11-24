class ParkpilotSwitch:
    def __init__(self):
        self.state = "Released"
        self.exclusive_press_detected = False

    def read_input(self, signal_data):
        parkpilot_signal = signal_data.get("parkpilot_switch", False)
        other_signals = {key: val for key, val in signal_data.items() if key != "parkpilot_switch"}
        self.exclusive_press_detected = parkpilot_signal and not any(other_signals.values())

    def update_state(self):
        if self.exclusive_press_detected:
            self.state = "Pressed"
        else:
            self.state = "Released"

    def process_signal(self, signal_data):
        self.read_input(signal_data)
        self.update_state()
        return self.state
