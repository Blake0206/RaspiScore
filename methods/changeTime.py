

def main(short_detail):
    _strings = short_detail.split(":")
    strings = _strings[0].split("- ")

    strings[1] = int(strings[1]) - 2  # 3 for PST --- 2 for MST
    if strings[1] <= 0:
        strings[1] = 12 + strings[1]
        if strings[1] != 12:
            _strings[1] = _strings[1].replace("PM", "AM")

    _strings[1] = _strings[1].replace("EST", "")

    #fixed_time = (f"{strings[0]}- {strings[1]}:{_strings[1]}")
    fixed_time = f"{strings[1]}:{_strings[1]}"
    
    return fixed_time

if __name__ == "__main__":
    main()