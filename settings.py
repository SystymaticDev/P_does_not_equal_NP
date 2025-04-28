class Settings:
    def __init__(self):
        self.preferences = {
            "font_size": 10,
            "theme": "light",
            "tab_width": 4
        }

    def get(self, key, default=None):
        return self.preferences.get(key, default)

    def set(self, key, value):
        self.preferences[key] = value
