import io
import disnake

async def handle_missing_roles(target, error, is_inter: bool = False):
    missing_roles = []
    for r in error.missing_roles:
        role = target.guild.get_role(r) if isinstance(r, int) else r
        missing_roles.append(role.name if role else str(r))

    msg = f":x: You need one of the following roles to run this command: **{', '.join(missing_roles)}**"

    if is_inter:
        # For slash commands, must use interaction response
        if not target.response.is_done():
            await target.response.send_message(msg, ephemeral=True)
        else:
            await target.followup.send(msg, ephemeral=True)
    else:
        await target.reply(msg)


async def handle_generic_error(target, error, is_inter: bool = False):
    error_msg = str(error)
    error_file = disnake.File(fp=io.StringIO(error_msg), filename="error.txt")
    msg = ":warning: **Something went really wrong... If persistent, please contact Management** :warning:"

    if is_inter:
        if not target.response.is_done():
            await target.response.send_message(msg, file=error_file, ephemeral=True)
        else:
            await target.followup.send(msg, file=error_file, ephemeral=True)
    else:
        await target.reply(msg, file=error_file)