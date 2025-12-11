#!/usr/bin/env python3
import re
import os

# Screens to update (relative to src/screens/)
screens_to_update = [
    "profile/EditProfileScreen.tsx",
    "profile/ProfileSetupScreen.tsx",
    "settings/PrivacySettingsScreen.tsx",
    "matching/MatchingScreen.tsx",
    "notifications/NotificationsScreen.tsx",
    "verification/VerificationScreen.tsx",
    "auth/LoginScreen.tsx",
    "auth/RegisterScreen.tsx",
]

base_path = "src/screens"

for screen_file in screens_to_update:
    file_path = os.path.join(base_path, screen_file)

    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        continue

    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already updated
    if 'useColors' in content:
        print(f"[OK] Already updated: {screen_file}")
        continue

    print(f"[UPDATE] Updating: {screen_file}")

    # Calculate relative path depth
    depth = screen_file.count('/')
    relative_path = '../' * (depth + 1)

    # Step 1: Add useColors import after other imports
    import_pattern = r"(import { COLORS, SPACING, FONTS } from ['\"].*?config['\"];)"
    import_replacement = r"\1\nimport { useColors } from '" + relative_path + "hooks/useColors';"
    content = re.sub(import_pattern, import_replacement, content)

    # Step 2: Add const colors = useColors(); hook in component
    # Find the component function and add the hook
    component_pattern = r"(export const \w+Screen.*?=.*?\{[\s\S]*?)(const \[|const {|const navigation)"
    def add_colors_hook(match):
        before = match.group(1)
        first_const = match.group(2)
        # Check if colors hook already exists
        if 'const colors = useColors();' not in before:
            return before + "const colors = useColors();\n  " + first_const
        return before + first_const
    content = re.sub(component_pattern, add_colors_hook, content)

    # Step 3: Convert styles to createStyles function
    styles_pattern = r"const styles = StyleSheet\.create\("
    styles_replacement = "const createStyles = (colors: ReturnType<typeof useColors>) => StyleSheet.create("
    content = content.replace(styles_pattern, styles_replacement)

    # Step 4: Add const styles = createStyles(colors); before return statement
    # Find the return statement and add styles instantiation
    return_pattern = r"(\n\s+)(return \([\s\S]*?<SafeAreaView)"
    def add_styles_call(match):
        indent = match.group(1)
        return_stmt = match.group(2)
        return indent + "const styles = createStyles(colors);" + indent + "\n" + indent + return_stmt
    content = re.sub(return_pattern, add_styles_call, content)

    # Step 5: Replace COLORS.xxx with colors.xxx in StyleSheet
    # In the createStyles function and inline
    content = re.sub(r'\bCOLORS\.(\w+)', r'colors.\1', content)

    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[DONE] Updated: {screen_file}")

print("\nDark mode update complete!")
