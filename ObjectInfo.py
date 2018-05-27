class ObjectInfo:

    def __init__(self, width_frame, height_frame, number_of_sections):

        self.height_frame = int(height_frame)
        self.width_frame = int(width_frame)
        self.current_position = None
        self.previous_position = None
        self.section = 1
        self.destination = ((int(width_frame / 2), 0), (int(width_frame / 2), int(height_frame)))
        self.number_of_sections = number_of_sections

    def add_position(self, position):

        if not self.current_position:  # First position
            self.current_position = position
            self.destination = ((int(self.current_position[0]), 0), (int(self.current_position[0]), self.height_frame))

        else:
            self.difference_between_positions(position)
        return self.destination

    def difference_between_positions(self, position):

        section_point = self.get_section(position)

        if  section_point > self.section:
            self.section = section_point
            self.previous_position = self.current_position
            self.current_position = position
            self.get_destination()

        elif section_point < self.section:
            self.section = section_point
            self.current_position = None
            self.previous_position = None

    def get_section(self, position):

        for x in range(1, self.number_of_sections + 1):
            if position[1] < (self.height_frame / self.number_of_sections) * x:
                return x


    def get_destination(self):

        # h = mw + b

        try:
            m = (self.current_position[1] - self.previous_position[1]) / (
                        self.current_position[0] - self.previous_position[0])
            b = self.current_position[1] - m * self.current_position[0]

            max_w = int((self.height_frame - b) / m)
            min_w = int((0 - b) / m)

            self.destination = ((min_w, 0), (max_w, int(self.height_frame)))

        except ZeroDivisionError:
            print("**** Zero Division Error ***")
            print(" Previous ->", self.previous_position)
            print(" Current ->", self.current_position)