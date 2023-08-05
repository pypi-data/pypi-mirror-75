# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['swtor_settings_updater']

package_data = \
{'': ['*']}

install_requires = \
['regex>=2020.7.14']

setup_kwargs = {
    'name': 'swtor-settings-updater',
    'version': '0.0.1',
    'description': 'Star Wars: The Old Republic Settings Updater',
    'long_description': '# Star Wars: The Old Republic Settings Updater\n\nA library to update the `*_PlayerGUIState.ini` settings for all your characters.\n\n## Example of usage\n\n```python\nimport logging\nfrom swtor_settings_updater import *\n\n\ndef my_settings(server_id, character_name, s):\n    # swtor_settings_updater.Chat sets the ChatChannels, Chat_Custom_Channels\n    # and ChatColors settings.\n    chat = Chat()\n    chn = chat.standard_channels\n\n    chn.group.color = chn.ops.color\n\n    chat.panel("General")\n    other = chat.panel("Other")\n\n    # Any channels not explicitly displayed on a panel will be displayed on\n    # the first panel (General).\n    other.display(\n        # chn.trade,\n        # chn.pvp,\n        # chn.general,\n        chn.emote,\n        chn.yell,\n        chn.officer,\n        chn.guild,\n        chn.say,\n        chn.whisper,\n        chn.ops,\n        chn.ops_leader,\n        chn.group,\n        chn.ops_announcement,\n        chn.ops_officer,\n        # chn.combat_information,\n        # chn.conversation,\n        chn.character_login,\n        chn.ops_information,\n        # chn.system_feedback,\n        chn.guild_information,\n        chn.group_information,\n        # chn.server_admin,\n        chn.error,\n    )\n\n    if character_name not in ["Kai Zykken", "Plagueis"]:\n        chat.custom_channel("Gsf")\n\n        if server_id == "he4000":\n            chat.custom_channel("Redleader")\n            chat.custom_channel("Narwhal")\n\n            myguild = chat.custom_channel("Myguild")\n            myguild.color = chn.guild.color\n            other.display(myguild)\n\n        elif server_id in ["he3000", "he3001"]:\n            chat.custom_channel("Endgame")\n\n    chat.apply(s)\n\n    s["Show_Chat_TimeStamp"] = "true"\n    s["GUI_Current_Profile"] = "myprofile"\n    s["GUI_WelcomeWindowIsOpen"] = "false"\n    s["GUI_ShowCompletedReputations"] = "false"\n    s["GUI_ShowUnstartedReputations"] = "false"\n    s["GUI_ShowAlignment"] = "true"\n    s["GUI_InvitesAsSocialMessage"] = "true"\n    s["GUI_ShowCooldownText"] = "true"\n    s["GUI_CooldownStyle"] = "3"\n    s["GUI_GCDStyle"] = "1"\n    s["GUI_MiniMapZoom"] = "0.842999994755"\n    s["GUI_MapFadeTo"] = "50.0"\n    s["GUI_GCConfirmOpenPack"] = "false"\n    s["GUI_ConfirmAmplifierCharge"] = "false"\n    s["GUI_InventoryAutoCloseBank"] = "false"\n    s["GUI_InventoryAutoCloseVendor"] = "false"\n    s["GUI_QuickslotLockState"] = "true"\n    s["GUI_WhoListNumberInChat"] = "0"\n    s["GroupFinder_Operation_InProgress"] = "true"\n\n\nif __name__ == "__main__":\n    logging.basicConfig(level=logging.INFO)\n    Character().update_all(SETTINGS_DIR, my_settings)\n```\n',
    'author': 'Johan Kiviniemi',
    'author_email': 'devel@johan.kiviniemi.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ion1/swtor-settings-updater',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
