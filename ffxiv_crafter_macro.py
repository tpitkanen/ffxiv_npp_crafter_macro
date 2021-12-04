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
    "Byregot's Blessing",
    "Precise Touch",
    "Careful Synthesis",
    "Muscle Memory",
    "Prudent Touch",
    "Focused Synthesis",
    "Focused Touch",
    "Preparatory Touch",
    "Groundwork",
    "Delicate Synthesis",
    "Intensive Synthesis",
    "Trained Eye",
    "Advanced Touch",
    "Prudent Synthesis",
    "Trained Finesse"
}
ACTIONS = {a.lower(): (a, 3) for a in ACTIONS}

# Buffs, need 2 s wait time
BUFFS = {
    "Inner Quiet",
    "Tricks Of The Trade",
    "Observe",
    "Waste Not",
    "Veneration",
    "Great Strides",
    "Innovation",
    "Final Appraisal",
    "Waste Not II",
    "Careful Observation",
    "Manipulation",
    "Reflect"
}
BUFFS = {b.lower(): (b, 2) for b in BUFFS}

# Combined actions & buffs
SKILLS = {}
SKILLS.update(ACTIONS)
SKILLS.update(BUFFS)

# {0}: action name, {1}: wait time
AC_TEMPLATE = '/ac "{0}" <wait.{1}>'

# {0}: page number, {1}: sound effect number
PAGE_DONE_TEMPLATE = "/echo Page {0} done <se.{1}>"

# {0}: sound effect number
MACRO_DONE_TEMPLATE = "/echo Macro done <se.{0}>"


def create_macro(lines, wait_last_line=False, autocomplete=True):
    """Convert lines with crafter skills into "/ac" macro lines"""
    new_lines = []
    for unedited_line in lines:
        line = unedited_line.strip().lower()

        if line in SKILLS:
            line = AC_TEMPLATE.format(*SKILLS[line])
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
    """Return all actions/buffs that begin with `line`'s content"""
    line = line.lower()
    matching = []

    for skill in SKILLS:
        if skill.startswith(line):
            matching.append(SKILLS[skill])

    return matching


def paginate(lines, page_size=15, se=1, se_on_last_page=False):
    """Break lines into `page_size` sized pages with sound effect `se`"""
    processed = []
    remaining = lines

    split_index = page_size - 1
    page_number = 1

    while len(remaining) > page_size:
        processed += remaining[:split_index]
        remaining = remaining[split_index:]
        processed.append(PAGE_DONE_TEMPLATE.format(page_number, se))
        processed.append("")
        page_number += 1
    processed += remaining

    if se_on_last_page:
        processed.append(MACRO_DONE_TEMPLATE.format(se))

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
