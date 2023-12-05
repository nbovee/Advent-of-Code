import common_advent as advent
signal = advent.get_input(__file__).pop()

packet_end_offset = 4
message_end_offset = 14

def signal_scanner(_signal, offset):
    for i in range(len(_signal) - offset):
        if len(set(_signal[i:i + offset])) == offset:    
            return i + offset

packet_start = signal_scanner(signal, packet_end_offset)
print(packet_start)
print(signal_scanner(signal[packet_start:], message_end_offset) + packet_start)