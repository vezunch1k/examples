examples
========

Code examples


graph_editor.py
Console graph editor. Check '--help' for usage rules.

graph_editor_with_states.py
Base was taken from graph_editor.py, but difference is in undo/redo implementation (keeping stacks with graph states). Suitable for command parameters independency. Weakness is in memory usage, bad for big objects.

graph_editor_command_pattern.py
Base was taken also from graph_editor.py, but this implementation uses Command pattern for logic separation.
