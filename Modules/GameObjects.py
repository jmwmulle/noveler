from Modules.Database import Database

class Trait:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
        self.history = []

    def add_to_history(self, state_change):
        self.history.append(state_change)

    def get_current_state(self):
        return self.history[-1] if self.history else None

    def save_to_db(self, db: Database):
        """Saves the Trait object to the database."""
        db.create_trait(self.id, self.title, self.description)


class BaseCharacter:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.traits = []

    def add_trait(self, trait: Trait):
        self.traits.append(trait)

    def save_to_db(self, db: Database):
        """Saves the Character object to the database."""
        db.create_character(self.id, self.name, self.description)
        for trait in self.traits:
            trait.save_to_db(db)


class BaseLocation:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.traits = []

    def add_trait(self, trait: Trait):
        self.traits.append(trait)

    def save_to_db(self, db: Database):
        """Saves the Location object to the database."""
        db.create_location(self.id, self.name, self.description)
        for trait in self.traits:
            trait.save_to_db(db)