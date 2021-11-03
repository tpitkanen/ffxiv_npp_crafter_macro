"""Convert lines of crafter skills into a macro.

Made for Python Script extension for Notepad++, but only the `get_lines`
and `set_lines` functions are Notepad++-specific.

Python 2.7+ required.

Example:
    Muscle Memory
    Inner Quiet
    Waste Not
    Groundwork

    ->

    /ac "Muscle Memory" <wait.3>
    /ac "Inner Quiet" <wait.2>
    /ac "Waste Not" <wait.2>
    /ac "Groundwork"

"""

# Actions, need 3 s wait time
ACTIONS = {
    "Basic Synthesis",
    "Basic Touch",
    "Master's Mend",
    "Hasty Touch",
    "Rapid Synthesis",
    "Standard Touch",
    "Brand Of The Elements",
    "Byregot's Blessing",
    "Precise Touch",
    "Careful Synthesis",
    "Muscle Memory",
    "Patient Touch",
    "Prudent Touch",
    "Focused Synthesis",
    "Focused Touch",
    "Preparatory Touch",
    "Groundwork",
    "Delicate Synthesis",
    "Intensive Synthesis",
    "Trained Eye"
}
ACTIONS = {a.lower(): a for a in ACTIONS}

# Buffs, need 2 s wait time
BUFFS = {
    "Inner Quiet",
    "Tricks Of The Trade",
    "Observe",
    "Waste Not",
    "Veneration",
    "Great Strides",
    "Innovation",
    "Name Of The Elements",
    "Final Appraisal",
    "Waste Not II",
    "Careful Observation",
    "Manipulation",
    "Reflect"
}
BUFFS = {b.lower(): b for b in BUFFS}

# {0}: action name, {1}: wait time
AC_TEMPLATE = '/ac "{0}" <wait.{1}>'


def create_macro(lines, wait_last_line=False, autocomplete=True):
    """Convert lines with crafter skills into "/ac" macro lines"""
    new_lines = []
    for unedited_line in lines:
        line = unedited_line.strip().lower()

        if line in ACTIONS:
            line = AC_TEMPLATE.format(ACTIONS[line], 3)
            new_lines.append(line)
            continue
        elif line in BUFFS:
            line = AC_TEMPLATE.format(BUFFS[line], 2)
            new_lines.append(line)
            continue
        else:
            if autocomplete:
                matching = autocomplete_line(line)
                if len(matching) == 1:
                    line = AC_TEMPLATE.format(*matching[0])
                    new_lines.append(line)
                    continue
            new_lines.append(unedited_line)

    if not wait_last_line:
        # Remove " <wait.X>" from last line
        last_line = new_lines[-1]
        wait_index = last_line.find(" <wait.")
        if wait_index >= 0:
            new_lines[-1] = last_line[:wait_index]

    return new_lines


def autocomplete_line(line):
    """Return all actions/buffs that begin with `line`'s content."""
    line = line.lower()
    matching = []

    for action in ACTIONS:
        if action.startswith(line):
            matching.append((ACTIONS[action], 3))

    for buff in BUFFS:
        if buff.startswith(line):
            matching.append((BUFFS[buff], 2))

    return matching


def paginate(lines, page_size=15, se=1):
    """Break lines into `page_size` sized pages with sound effect `se`"""
    processed = []
    remaining = lines
    i = 1

    while len(remaining) > 15:
        processed += remaining[:14]
        remaining = remaining[14:]
        processed.append("/echo Page {0} done <se.{1}>".format(i, se))
        processed.append("")
        i += 1
    processed += remaining

    return processed


def get_lines():
    """Get all lines from Notepad++ editor tab"""
    return editor.getText().splitlines()


def set_lines(lines):
    """Set (replace) all lines in a Notepad++ editor tab"""
    editor.setText("\r\n".join(lines))


def main():
    lines = get_lines()
    new_lines = create_macro(lines)
    new_lines = paginate(new_lines)
    set_lines(new_lines)


if __name__ == "__main__":
    main()
