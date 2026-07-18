#!/usr/bin/env python3
"""
Generate terminal-banner.svg with human-like typing animations.

All configurable values are at the top of this file.
Run:  python3 generate-banner.py
"""

import random

#  ╔══════════════════════════════════════════════════════════════════════╗
# ║                        CONFIGURATION                                 ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ── Identity ────────────────────────────────────────────────────────────
USERNAME   = "gideon"
HOSTNAME   = "Andromeda-43"
SHELL_TITLE = "bash — 100x30"

# ── Terminal commands and outputs ───────────────────────────────────────
# Each entry: (command_text, output_lines, is_typo)
# output_lines: list of items, each either:
#   ("text", "css_class")                         — single-style line
#   [("text", "css_class", x_offset), ...]        — multi-style line
# is_typo: None or dict with typo config

TYPO_CONFIG = {
    "correct_prefix": "whoam",   # correctly typed part
    "wrong_suffix":   "me",      # the typo characters
    "fix_suffix":     "i",       # what gets typed after backspace
}

COMMANDS = [
    {
        "cmd": "whoami",  # display only — typing controlled by TYPO_CONFIG
        "typo": TYPO_CONFIG,
        "output": [
            ("gideon — full-stack developer, Kampala, Uganda 🇺🇬 [UG]", "out-str"),
        ],
    },
    {
        "cmd": "cat philosophy.txt",
        "typo": None,
        "output": [
            ("I plan before I build. Every project starts", "out-str"),
            ("with a spec, not a blank editor.", "out-str"),
        ],
    },
    {
        "cmd": "ls --currently-shipping",
        "typo": None,
        "output": [
            [("Acadex", "out-key", 0), ("# multi-tenant school SaaS for East Africa", "comment", 140)],
            [("RestaurantOS", "out-key", 0), ("# POS, kitchen & ops for restaurants", "comment", 140)],
        ],
    },
    {
        "cmd": "stack --list",
        "typo": None,
        "output": [
            ("TypeScript · Python · Next.js · React · Prisma · PostgreSQL", "out-str"),
        ],
    },
    {
        "cmd": "echo $MOTTO",
        "typo": None,
        "output": [
            ('"Systems that outlast motivation."', "out-str"),
        ],
    },
]

# ── Layout ──────────────────────────────────────────────────────────────
SVG_WIDTH     = 1000
PROMPT_X      = 24       # left margin for all content
CHAR_W        = 9.0      # monospace character width (Fira Code 15px)
LINE_HEIGHT   = 22       # vertical spacing between lines
TITLEBAR_H    = 36       # title bar height
FIRST_LINE_Y  = 70       # y baseline of first command line
BLOCK_GAP     = 8        # extra vertical pixels between command blocks
BOTTOM_PAD    = 30       # padding below last element

# ── Timing (seconds) ───────────────────────────────────────────────────
BASE_KEYSTROKE        = 0.075   # base delay per keystroke
INITIAL_DELAY         = 0.30    # delay before first prompt appears
PAUSE_AFTER_ENTER     = 0.35    # delay after Enter before output shows
PAUSE_BEFORE_PROMPT   = 0.01    # delay after output before next prompt (10ms = instant)
PAUSE_BEFORE_TYPING   = 0.25    # delay after prompt before human starts typing
TYPO_NOTICE_PAUSE_MIN = 0.35    # min pause when noticing a typo
TYPO_NOTICE_PAUSE_MAX = 0.50    # max pause when noticing a typo
TYPO_RETYPE_PAUSE_MIN = 0.10    # min pause before retyping after backspace
TYPO_RETYPE_PAUSE_MAX = 0.18    # max pause before retyping after backspace
BACKSPACE_DELAY_MIN   = 0.06    # min delay per backspace
BACKSPACE_DELAY_MAX   = 0.10    # max delay per backspace
FINAL_CURSOR_DELAY    = 0.30    # delay before final blinking cursor appears

# ── Typing variance (multipliers) ──────────────────────────────────────
SLOW_CHAR_MULT_MIN    = 1.3     # min multiplier for symbols/shifted chars
SLOW_CHAR_MULT_MAX    = 1.8     # max multiplier
SPACE_MULT_MIN        = 1.1     # min multiplier for spacebar
SPACE_MULT_MAX        = 1.5     # max multiplier
JITTER_STDDEV         = 0.018   # gaussian jitter standard deviation
MICRO_PAUSE_CHANCE    = 0.08    # probability of a tiny thinking pause
MICRO_PAUSE_MIN       = 0.05    # min micro-pause duration
MICRO_PAUSE_MAX       = 0.12    # max micro-pause duration
MIN_KEYSTROKE         = 0.03    # minimum delay floor

# ── Colors ──────────────────────────────────────────────────────────────
COLOR_BG       = "#241f31"
COLOR_TITLEBAR = "#2d2a3d"
COLOR_BORDER   = "#3d3846"
COLOR_DOT      = "#3c6eb4"
COLOR_PATH     = "#9a9996"
COLOR_USER     = "#8ff0a4"
COLOR_AT       = "#f6f5f4"
COLOR_HOST     = "#8ff0a4"
COLOR_SEP      = "#f6f5f4"
COLOR_DIR      = "#62a0ea"
COLOR_SYM      = "#f6f5f4"
COLOR_CMD      = "#f6f5f4"
COLOR_COMMENT  = "#77767b"
COLOR_OUT_KEY  = "#8ff0a4"
COLOR_OUT_STR  = "#99c1f1"
COLOR_CURSOR   = "#f6f5f4"
COLOR_WINCTRL  = "#9a9996"

# ── Random seed (for reproducible animations) ──────────────────────────
RANDOM_SEED = 42


# ╔═══════════════════════════════════════════════════════════════════════╗
# ║                     ENGINE (modify with care)                        ║
# ╚═══════════════════════════════════════════════════════════════════════╝

SLOW_CHARS = set('!@#$%^&*()_+-={}[]|\\:;"\'<>,.?/~`')
SHIFT_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+{}|:"<>?~')

def keystroke_delay(char, prev_char=None):
    base = BASE_KEYSTROKE
    if char in SLOW_CHARS or char in SHIFT_CHARS:
        base *= random.uniform(SLOW_CHAR_MULT_MIN, SLOW_CHAR_MULT_MAX)
    if char == ' ':
        base *= random.uniform(SPACE_MULT_MIN, SPACE_MULT_MAX)
    jitter = random.gauss(0, JITTER_STDDEV)
    delay = base + jitter
    if random.random() < MICRO_PAUSE_CHANCE:
        delay += random.uniform(MICRO_PAUSE_MIN, MICRO_PAUSE_MAX)
    return max(MIN_KEYSTROKE, delay)

def backspace_delay_val():
    return random.uniform(BACKSPACE_DELAY_MIN, BACKSPACE_DELAY_MAX)

def escape_xml(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


# ── Prompt ──────────────────────────────────────────────────────────────

# Compute prompt segment positions from character widths (zero-gap monospace)
# "gideon" = 6, "@" = 1, "Andromeda-43" = 12, ":" = 1, "~" = 1, "$" = 1 = 22 chars
PROMPT_SEGMENTS = [
    (USERNAME,  "prompt-user", 0),
    ("@",       "prompt-at",   len(USERNAME)),
    (HOSTNAME,  "prompt-host", len(USERNAME) + 1),
    (":",       "prompt-sep",  len(USERNAME) + 1 + len(HOSTNAME)),
    ("~",       "prompt-dir",  len(USERNAME) + 1 + len(HOSTNAME) + 1),
    ("$",       "prompt-sym",  len(USERNAME) + 1 + len(HOSTNAME) + 2),
]
PROMPT_CHAR_COUNT = len(USERNAME) + 1 + len(HOSTNAME) + 3  # +3 for :~$
CMD_START_X = PROMPT_X + (PROMPT_CHAR_COUNT + 1) * CHAR_W  # +1 for space after $


def prompt_svg(y, show_time):
    parts = [f'    <g opacity="0">']
    for (text, cls, char_offset) in PROMPT_SEGMENTS:
        x = PROMPT_X + char_offset * CHAR_W
        parts.append(f'<text class="{cls}" x="{x:.1f}" y="{y}">{escape_xml(text)}</text>')
    parts.append(
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{show_time:.2f}s" dur="0.01s" fill="freeze"/>'
    )
    parts.append('</g>')
    return ''.join(parts) + '\n'


# ── Typing Animator ─────────────────────────────────────────────────────

class TypingAnimator:
    def __init__(self, y, start_time):
        self.y = y
        self.t = start_time
        self.x = CMD_START_X
        self.start_x = CMD_START_X
        self.start_time = start_time
        self.elements = []
        self.cursor_keyframes = [(start_time, CMD_START_X)]
        self.prev_char = None

    def type_char(self, char, will_be_deleted=False):
        delay = keystroke_delay(char, self.prev_char)
        self.t += delay
        display = '&#160;' if char == ' ' else escape_xml(char)
        elem = (
            f'      <text class="cmd" x="{self.x:.1f}" y="{self.y}" opacity="0">'
            f'{display}'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{self.t:.2f}s" dur="0.01s" fill="freeze"/>'
        )
        if will_be_deleted:
            elem += f'{{HIDE@{len(self.elements)}}}'
        elem += '</text>'
        self.elements.append(elem)
        self.cursor_keyframes.append((self.t, self.x + CHAR_W))
        self.prev_char = char
        self.x += CHAR_W
        return self.t

    def type_string(self, text):
        for ch in text:
            self.type_char(ch)

    def pause(self, duration):
        self.t += duration
        self.cursor_keyframes.append((self.t, self.x))

    def backspace(self, hide_indices):
        for idx in hide_indices:
            self.t += backspace_delay_val()
            self.x -= CHAR_W
            hide_anim = (
                f'<animate attributeName="opacity" from="1" to="0" '
                f'begin="{self.t:.2f}s" dur="0.01s" fill="freeze"/>'
            )
            self.elements[idx] = self.elements[idx].replace(f'{{HIDE@{idx}}}', hide_anim)
            self.cursor_keyframes.append((self.t, self.x))

    def get_svg(self):
        return '    <g>\n' + '\n'.join(self.elements) + '\n    </g>\n'

    def get_cursor_svg(self):
        if len(self.cursor_keyframes) < 2:
            return ''
        t0 = self.cursor_keyframes[0][0]
        t_end = self.cursor_keyframes[-1][0]
        total_dur = max(t_end - t0, 0.01)
        values = ';'.join(f'{x:.1f}' for (_, x) in self.cursor_keyframes)
        key_times = ';'.join(f'{(t - t0) / total_dur:.4f}' for (t, _) in self.cursor_keyframes)
        cursor_y = self.y - 14
        hide_time = self.t + 0.05
        return (
            f'    <rect class="cursor-blk" x="{self.start_x:.1f}" y="{cursor_y}" '
            f'width="10" height="18" opacity="0">\n'
            f'      <animate attributeName="opacity" from="0" to="1" '
            f'begin="{t0:.2f}s" dur="0.01s" fill="freeze"/>\n'
            f'      <animate attributeName="x" '
            f'values="{values}" keyTimes="{key_times}" '
            f'begin="{t0:.2f}s" dur="{total_dur:.2f}s" fill="freeze"/>\n'
            f'      <animate attributeName="opacity" from="1" to="0" '
            f'begin="{hide_time:.2f}s" dur="0.01s" fill="freeze"/>\n'
            f'    </rect>\n'
        )


# ── Output Lines ────────────────────────────────────────────────────────

def output_lines_svg(lines, y_start, show_time):
    svg = f'    <g opacity="0">\n'
    y = y_start
    for line in lines:
        if isinstance(line, list):
            for (text, css_class, x_offset) in line:
                svg += f'      <text class="{css_class}" x="{PROMPT_X + x_offset}" y="{y}">{escape_xml(text)}</text>\n'
        else:
            text, css_class = line
            svg += f'      <text class="{css_class}" x="{PROMPT_X}" y="{y}">{escape_xml(text)}</text>\n'
        y += LINE_HEIGHT
    svg += (
        f'      <animate attributeName="opacity" from="0" to="1" '
        f'begin="{show_time:.2f}s" dur="0.01s" fill="freeze"/>\n'
        f'    </g>\n'
    )
    return svg, y


# ── Window Controls ─────────────────────────────────────────────────────

def window_controls_svg():
    c = COLOR_WINCTRL
    return f'''    <!-- Window controls — GNOME Adwaita style -->
    <!-- Minimize -->
    <g transform="translate(904, 6)">
      <circle cx="12" cy="12" r="11" fill="transparent"/>
      <line x1="7" y1="12" x2="17" y2="12" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>
    </g>
    <!-- Maximize -->
    <g transform="translate(930, 6)">
      <circle cx="12" cy="12" r="11" fill="transparent"/>
      <rect x="6.5" y="6.5" width="11" height="11" rx="2" fill="none" stroke="{c}" stroke-width="1.6"/>
    </g>
    <!-- Close -->
    <g transform="translate(956, 6)">
      <circle cx="12" cy="12" r="11" fill="transparent"/>
      <line x1="7" y1="7" x2="17" y2="17" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>
      <line x1="17" y1="7" x2="7" y2="17" stroke="{c}" stroke-width="1.6" stroke-linecap="round"/>
    </g>
'''


# ── Main SVG Generation ────────────────────────────────────────────────

def generate_svg():
    random.seed(RANDOM_SEED)

    parts = []
    t = 0.0
    y = FIRST_LINE_Y

    for i, cmd_entry in enumerate(COMMANDS):
        # Show prompt
        if i == 0:
            t += INITIAL_DELAY
        else:
            t += PAUSE_BEFORE_PROMPT
        parts.append(prompt_svg(y, t))

        # Human pause before typing
        t += PAUSE_BEFORE_TYPING

        # Type the command
        anim = TypingAnimator(y, t)

        if cmd_entry["typo"]:
            tc = cmd_entry["typo"]
            # Type the correct prefix
            anim.type_string(tc["correct_prefix"])
            # Type the wrong suffix (mark for deletion)
            wrong_indices = []
            for ch in tc["wrong_suffix"]:
                idx = len(anim.elements)
                anim.type_char(ch, will_be_deleted=True)
                wrong_indices.append(idx)
            # Pause — notice the mistake
            anim.pause(random.uniform(TYPO_NOTICE_PAUSE_MIN, TYPO_NOTICE_PAUSE_MAX))
            # Backspace (reverse order: last typed gets deleted first)
            anim.backspace(list(reversed(wrong_indices)))
            # Small pause before correction
            anim.pause(random.uniform(TYPO_RETYPE_PAUSE_MIN, TYPO_RETYPE_PAUSE_MAX))
            # Type the fix
            anim.type_string(tc["fix_suffix"])
        else:
            anim.type_string(cmd_entry["cmd"])

        t = anim.t
        parts.append(anim.get_svg())
        parts.append(anim.get_cursor_svg())

        # Press Enter → output appears
        t += PAUSE_AFTER_ENTER
        y += LINE_HEIGHT

        out_svg, y = output_lines_svg(cmd_entry["output"], y, t)
        parts.append(out_svg)
        y += BLOCK_GAP

    # Final blinking cursor on empty prompt
    t += PAUSE_BEFORE_PROMPT
    parts.append(prompt_svg(y, t))

    t += FINAL_CURSOR_DELAY
    cursor_y = y - 14
    parts.append(
        f'    <g opacity="0">\n'
        f'      <rect class="cursor-blk" x="{CMD_START_X:.1f}" y="{cursor_y}" '
        f'width="10" height="18">\n'
        f'        <animate attributeName="opacity" values="1;0;1" dur="1s" '
        f'begin="{t:.2f}s" repeatCount="indefinite"/>\n'
        f'      </rect>\n'
        f'      <animate attributeName="opacity" from="0" to="1" '
        f'begin="{t:.2f}s" dur="0.01s" fill="freeze"/>\n'
        f'    </g>\n'
    )

    svg_height = y + BOTTOM_PAD

    # Title bar text
    titlebar_label = f"{USERNAME}@{HOSTNAME}"

    # Assemble CSS
    css = f'''      .term-bg {{ fill: {COLOR_BG}; }}
      .titlebar {{ fill: {COLOR_TITLEBAR}; }}
      .fedora-dot {{ fill: {COLOR_DOT}; }}
      .path {{ fill: {COLOR_PATH}; font: 500 12.5px 'Fira Code', 'Cascadia Code', 'JetBrains Mono', monospace; }}
      .prompt-user {{ fill: {COLOR_USER}; font: 600 15px 'Fira Code', 'Cascadia Code', monospace; }}
      .prompt-at {{ fill: {COLOR_AT}; font: 600 15px 'Fira Code', 'Cascadia Code', monospace; }}
      .prompt-host {{ fill: {COLOR_HOST}; font: 600 15px 'Fira Code', 'Cascadia Code', monospace; }}
      .prompt-sep {{ fill: {COLOR_SEP}; font: 600 15px 'Fira Code', 'Cascadia Code', monospace; }}
      .prompt-dir {{ fill: {COLOR_DIR}; font: 600 15px 'Fira Code', 'Cascadia Code', monospace; }}
      .prompt-sym {{ fill: {COLOR_SYM}; font: 600 15px 'Fira Code', 'Cascadia Code', monospace; }}
      .cmd {{ fill: {COLOR_CMD}; font: 15px 'Fira Code', 'Cascadia Code', monospace; }}
      .comment {{ fill: {COLOR_COMMENT}; font: 13px 'Fira Code', 'Cascadia Code', monospace; }}
      .out-key {{ fill: {COLOR_OUT_KEY}; font: 14px 'Fira Code', 'Cascadia Code', monospace; }}
      .out-str {{ fill: {COLOR_OUT_STR}; font: 13.5px 'Fira Code', 'Cascadia Code', monospace; }}
      .cursor-blk {{ fill: {COLOR_CURSOR}; }}'''

    svg = f'''<svg width="{SVG_WIDTH}" height="{svg_height}" viewBox="0 0 {SVG_WIDTH} {svg_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
{css}
    </style>
    <clipPath id="term-clip">
      <rect x="0" y="0" width="{SVG_WIDTH}" height="{svg_height}" rx="10" ry="10"/>
    </clipPath>
  </defs>

  <g clip-path="url(#term-clip)">
    <rect class="term-bg" x="0" y="0" width="{SVG_WIDTH}" height="{svg_height}"/>

    <!-- Title bar -->
    <rect class="titlebar" x="0" y="0" width="{SVG_WIDTH}" height="{TITLEBAR_H}"/>
    <circle class="fedora-dot" cx="24" cy="18" r="6"/>
    <text class="path" x="42" y="22.5">{escape_xml(titlebar_label)}</text>
    <text class="path" x="500" y="22.5" text-anchor="middle">{escape_xml(SHELL_TITLE)}</text>

{window_controls_svg()}
{''.join(parts)}  </g>

  <rect x="0.5" y="0.5" width="{SVG_WIDTH - 1}" height="{svg_height - 1}" rx="10" ry="10" fill="none" stroke="{COLOR_BORDER}" stroke-width="1"/>
</svg>
'''

    print(f"SVG: {SVG_WIDTH} x {svg_height}")
    print(f"Duration: {t:.1f}s")
    print(f"Prompt: {titlebar_label}:~$")
    print(f"CMD_START_X: {CMD_START_X:.1f} (char {PROMPT_CHAR_COUNT + 1})")
    print(f"CHAR_W: {CHAR_W}")

    return svg


if __name__ == '__main__':
    svg = generate_svg()
    path = '/home/gideon/Documents/CODE/Projects/Gito125/terminal-banner.svg'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"\nWritten: {path}")
