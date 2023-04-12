from player import player

cs_player = player('s1mple')

print("PLAYER NAME: " + cs_player.get_player_name() +"\n")

print("LIQUIPEDIA URL: " + cs_player.get_url() + "\n")

print("PLAYER INFO: \n")
print(cs_player.get_player_info())
print("\n")

print("PLAYER LINKS: \n")
print(cs_player.get_links())
print("\n")

print("PLAYER HISTORY: \n")
print(cs_player.get_history())
print("\n")

print("PLAYER ACHIEVEMENTS: \n")
print(cs_player.get_achieve())
print("\n")