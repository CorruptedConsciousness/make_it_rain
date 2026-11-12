
import random
import shutil
import sys
import time

# ==========================================
# MAKE IT RAIN - Matrix Digital Rain
# ==========================================

# Animation settings
FRAME_DELAY = 0.035
COLUMN_SPACING = 1
MIN_TRAIL = 12
MAX_TRAIL = 35
MIN_SPEED = 1
MAX_SPEED = 5
RAIN_DENSITY = 0.85

# Terminal dimensions
width, height = shutil.get_terminal_size()
columns = list(range(1, width + 1, COLUMN_SPACING))

# Matrix color palette (ANSI 256-color)
COLORS = [
    22,   # Very dark green
    28,   # Dark green
    34,   # Medium green
    40,   # Green
    46,   # Bright neon green
    82,   # Electric green
    120,  # Pale green
    231,  # White
]


def create_stream():
    return {
        "row": random.randint(-height, 0),
        "speed": random.randint(MIN_SPEED, MAX_SPEED),
        "length": random.randint(MIN_TRAIL, MAX_TRAIL),
        "active": random.random() < RAIN_DENSITY,
    }


streams = [create_stream() for _ in columns]


def draw(row, col, digit, color):
    if 1 <= row <= height:
        sys.stdout.write(
            f"\033[{row};{col}H"
            f"\033[38;5;{color}m{digit}"
        )


def reset_stream(stream):
    stream["row"] = random.randint(-height, 0)
    stream["speed"] = random.randint(MIN_SPEED, MAX_SPEED)
    stream["length"] = random.randint(MIN_TRAIL, MAX_TRAIL)
    stream["active"] = random.random() < RAIN_DENSITY


try:
    # Alternate screen, hide cursor, black background
    sys.stdout.write(
        "\033[?1049h"
        "\033[?25l"
        "\033[40m"
        "\033[2J"
    )
    sys.stdout.flush()

    frame = 0

    while True:
        for col, stream in zip(columns, streams):

            if frame % stream["speed"] != 0:
                continue

            row = stream["row"]
            length = stream["length"]

            # Erase the end of the trail
            draw(row - length, col, " ", 22)

            if stream["active"]:

                # Draw the entire fading trail
                for offset in range(length - 1, 0, -1):
                    trail_row = row - offset

                    # Dark at tail, bright near head
                    brightness = 1 - (offset / length)

                    if brightness < 0.20:
                        color = COLORS[0]
                    elif brightness < 0.40:
                        color = COLORS[1]
                    elif brightness < 0.60:
                        color = COLORS[2]
                    elif brightness < 0.80:
                        color = COLORS[3]
                    else:
                        color = COLORS[4]

                    # Randomly changing binary digits
                    if random.random() < 0.35:
                        digit = random.randint(0, 1)
                        draw(trail_row, col, digit, color)

                # Bright green near the head
                draw(row - 1, col, random.randint(0, 1), 82)

                # Brilliant white leading digit
                draw(row, col, random.randint(0, 1), 231)

            stream["row"] += 1

            # Restart stream after leaving screen
            if stream["row"] - length > height:
                reset_stream(stream)

        sys.stdout.flush()
        frame += 1
        time.sleep(FRAME_DELAY)

except KeyboardInterrupt:
    pass

finally:
    # Restore terminal
    sys.stdout.write(
        "\033[0m"
        "\033[?25h"
        "\033[?1049l"
    )
    sys.stdout.flush()
