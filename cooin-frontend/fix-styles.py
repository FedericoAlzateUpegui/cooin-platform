#!/usr/bin/env python3
import re

files = {
    "src/screens/profile/EditProfileScreen.tsx": [161, 173],
    "src/screens/profile/ProfileSetupScreen.tsx": [],
    "src/screens/settings/PrivacySettingsScreen.tsx": [123, 135],
    "src/screens/auth/RegisterScreen.tsx": [],
}

for filepath, lines_to_check in files.items():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find and fix each file
        # First, find where colors is defined
        colors_line = None
        for i, line in enumerate(lines):
            if 'const colors = useColors()' in line:
                colors_line = i
                break

        if colors_line is None:
            print(f"[SKIP] {filepath}: No colors hook found")
            continue

        # Check if styles is already defined right after colors
        if colors_line + 1 < len(lines) and 'const styles = createStyles(colors)' in lines[colors_line + 1]:
            print(f"[OK] {filepath}: styles already at top")
            # Remove duplicate calls
            modified = False
            new_lines = []
            for i, line in enumerate(lines):
                # Skip lines that have "const styles = createStyles" but NOT the one right after colors
                if 'const styles = createStyles(colors)' in line and i != colors_line + 1:
                    # Skip this line and next empty lines
                    modified = True
                    continue
                new_lines.append(line)

            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"[FIXED] {filepath}: Removed duplicate styles calls")
        else:
            # Need to add styles after colors and remove duplicates
            new_lines = []
            added_styles = False
            for i, line in enumerate(lines):
                new_lines.append(line)
                # Add styles right after colors
                if i == colors_line and not added_styles:
                    new_lines.append("  const styles = createStyles(colors);\n")
                    added_styles = True
                # Skip other "const styles = createStyles" lines
                if 'const styles = createStyles(colors)' in line and i != colors_line + 1:
                    new_lines.pop()  # Remove the line we just added

            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"[FIXED] {filepath}: Moved styles to top and removed duplicates")

    except Exception as e:
        print(f"[ERROR] {filepath}: {e}")

print("\nDone!")
