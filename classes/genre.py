# Note: This class is no longer used, but wanted to show possible solution using custom classes
class Genre(object):
    def __init__(self, genre_id, genre_name):
        self.genre_id = genre_id
        self.genre_name = genre_name

    # In order to use set, had to set up Equality and Hash
    def __eq__(self, other):
        return isinstance(other, Genre) and self.genre_id == other.genre_id
        # Note: Updated from old recommendation to new
        # if isinstance(other, Genre):
        #     return self.genre_id == other.genre_id
        # else:
        #     return NotImplemented

    def __hash__(self):
        return hash(self.genre_id)
