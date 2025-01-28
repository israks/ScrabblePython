
def __str__(self):
        """Return a string representation of the board, suitable for human viewing.
        Uses colors to highlight various squares."""

        rows = []
        for row in range(self.SIZE):
            cols = []
            for col in range(self.SIZE):
                index = self.get_index(row, col)
                cell = self.cells[index]

                cell_string = cell if cell else " "
                if self.is_blank[index]:
                    cell_string = cell.lower()

                if PREMIUM_CELLS[index] == ".":
                    background_color = 47
                    foreground_color = 30
                elif PREMIUM_CELLS[index] == "D":
                    background_color = 101
                    foreground_color = 30
                elif PREMIUM_CELLS[index] == "T":
                    background_color = 41
                    foreground_color = 30
                elif PREMIUM_CELLS[index] == "d":
                    background_color = 106
                    foreground_color = 30
                elif PREMIUM_CELLS[index] == "t":
                    background_color = 44
                    foreground_color = 37
                else:
                    raise InvalidPremiumError()

                if self.is_blank[index]:
                    background_color = 43
                    foreground_color = 30

                # 256-color Xterm code is \033[38;5;Xm or 48 for background.
                # We're using 8-color mode here.
                cell_string = u"\u001b[%d;%dm %s \u001b[0m" % (background_color, foreground_color, cell_string)

                cols.append(cell_string)
            rows.append("".join(cols))
        return "\n".join(rows)
