"""_handle_profile_command handler."""

from reymen.sistem.ReYMeN_constants import display_ReYMeN_home
from reymen.reymen_cli.profiles import get_active_profile_name


def _handle_profile_command(cli) -> None:
    """Display active profile name and home directory."""
    display = display_ReYMeN_home()
    profile_name = get_active_profile_name()

    print()
    print(f"  Profile: {profile_name}")
    print(f"  Home:    {display}")
    print()
