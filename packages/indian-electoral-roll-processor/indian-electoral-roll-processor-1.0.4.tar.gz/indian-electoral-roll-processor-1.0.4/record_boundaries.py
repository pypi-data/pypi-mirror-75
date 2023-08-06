def get_voter_page_voter_boundaries(i, page_number=2):
    i = i - 1
    row = i // 3
    column = i % 3

    y_index = row
    y_length = 140
    y_offset = (y_index * y_length)

    start_y = 102 if page_number == 2 else 84

    y_top = start_y + y_index * (145 + (0.8 if y_index < 3 else 1.5))
    y_bottom = y_top + 147

    columns = [
        (50, y_top,  428, y_bottom), (426, y_top, 808, y_bottom), (803, y_top, 1183, y_bottom)]

    p = columns[column]
    return p
