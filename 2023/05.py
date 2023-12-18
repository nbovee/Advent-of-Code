import common_advent as advent
import re
input = advent.get_input(__file__)

print(re.split(r"\n\n+", "\n".join(input)))