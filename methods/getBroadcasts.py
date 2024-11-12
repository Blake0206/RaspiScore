
def main(event):
    for competition in event["competitions"]:
        broadcast_networks = []
        for broadcast in competition["geoBroadcasts"]:
            broadcast_network = broadcast["media"]["shortName"]
            media_type = broadcast["type"]["shortName"]
            if media_type == "TV":
                broadcast_networks.append(broadcast_network)

        network_info = "/".join(broadcast_networks) if broadcast_networks else "No Broadcast Info"    
    return f"{network_info}"


if __name__ == "__main__":
    main()