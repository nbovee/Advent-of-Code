import common_advent as advent
signal = advent.get_input(__file__).pop()

packet_end_offset = 4
message_end_offset = 14
find_packet = True

for i in range(len(signal) - packet_end_offset):
    if len(set(signal[i:i+packet_end_offset])) == packet_end_offset:    
        print(i + packet_end_offset)
        if find_packet:
            find_packet = not find_packet
            packet_end_offset = message_end_offset
        else: 
            break