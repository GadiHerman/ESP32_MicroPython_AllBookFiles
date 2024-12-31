import MD_YX5300

def display_menu(menu_items):
    print("==== MD_YX5300 Test Menu ====")
    for i, item in enumerate(menu_items, 1):
        print(f"{i}. {item}")
    print("=============================")

def get_user_choice(menu_items):
    while True:
        try:
            choice = int(input("Enter the number of your choice (0 to exit): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(menu_items):
                return menu_items[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    menu_items = [
        "Play Next Track",
        "Play Previous Track",
        "Play Track by ID",
        "Play First Track",
        "Volume Up",
        "Volume Down",
        "Set Volume",
        "Sleep Module",
        "Wakeup Module",
        "Reset Module",
        "Pause",
        "Resume",
        "Stop"
    ]

    player = MD_YX5300.MD_YX5300()

    while True:
        display_menu(menu_items)
        choice = get_user_choice(menu_items)

        if choice is None:
            print("Exiting the test menu. Goodbye!")
            break

        if choice == "Play Next Track":
            player.play_next()
        elif choice == "Play Previous Track":
            player.play_previous()
        elif choice == "Play Track by ID":
            track_id = int(input("Enter the track ID to play: "))
            player.play_track(track_id)
        elif choice == "Play First Track":
            player.play()
        elif choice == "Volume Up":
            player.volume_up(2)
        elif choice == "Volume Down":
            player.volume_down(2)
        elif choice == "Set Volume":
            volume_level = int(input("Enter the volume level (0-30): "))
            player.set_volume(volume_level)
        elif choice == "Sleep Module":
            player.sleep_module()
        elif choice == "Wakeup Module":
            player.wakeup_module()
        elif choice == "Reset Module":
            player.reset_module()
        elif choice == "Pause":
            player.pause()
        elif choice == "Resume":
            player.resume()
        elif choice == "Stop":
            player.stop()

if __name__ == "__main__":
    main()
