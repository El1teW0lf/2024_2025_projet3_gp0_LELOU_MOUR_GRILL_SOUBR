class Skill:
    def __init__(self, name, cost, branch, prerequisites=None):
        self.name = name
        self.cost = cost
        self.branch = branch
        self.prerequisites = prerequisites or []
        self.unlocked = False

    def can_unlock(self, unlocked_skills, current_points):
        if self.unlocked:
            return False
        if current_points < self.cost:
            return False
        return all(prereq in unlocked_skills for prereq in self.prerequisites)

    def unlock(self):
        self.unlocked = True


class SkillTree:
    def __init__(self):
        self.points = 20  # Points de départ
        self.skills = self._create_skills()
        self.unlocked_skills = []

    def _create_skills(self):
        return {
            # Branch: Navigation
            "Sailing": Skill("Sailing", 5, "Navigation"),
            "Map Reading": Skill("Map Reading", 4, "Navigation", ["Sailing"]),
            "Star Navigation": Skill("Star Navigation", 6, "Navigation", ["Map Reading"]),

            # Branch: Resistance
            "Endurance": Skill("Endurance", 4, "Resistance"),
            "Cold Resistance": Skill("Cold Resistance", 5, "Resistance", ["Endurance"]),
            "Fire Resistance": Skill("Fire Resistance", 6, "Resistance", ["Cold Resistance"]),

            # Branch: Conquerance
            "Sword Mastery": Skill("Sword Mastery", 5, "Conquerance"),
            "Tactics": Skill("Tactics", 4, "Conquerance", ["Sword Mastery"]),
            "Combat Resistance": Skill("Combat Resistance", 7, "Conquerance", ["Tactics"]),
        }

    def display_skills(self):
        print(f"\n🎯 Points disponibles : {self.points}")
        print("\n🧠 --- Arbre de Compétences ---")
        branches = ["Navigation", "Resistance", "Conquerance"]
        for branch in branches:
            print(f"\n🌿 [{branch}]")
            for skill in self.skills.values():
                if skill.branch == branch:
                    status = "✅" if skill.unlocked else "🔒"
                    print(f" {status} {skill.name} (Coût: {skill.cost})")

    def unlock_skill(self, name):
        skill = self.skills.get(name)
        if not skill:
            print("❌ Compétence inconnue.")
            return

        if skill.can_unlock(self.unlocked_skills, self.points):
            self.points -= skill.cost
            skill.unlock()
            self.unlocked_skills.append(skill.name)
            print(f"✅ '{skill.name}' débloquée !")
        else:
            print("❌ Conditions non remplies ou pas assez de points.")

    def run(self):
        while True:
            self.display_skills()
            choice = input("\n💡 Tape le nom d'une compétence à débloquer (ou 'quit' pour quitter) : ").strip()
            if choice.lower() == "quit":
                print("\n👋 À bientôt, stratège !")
                break
            self.unlock_skill(choice)


# --- Lancer le programme ---
if __name__ == "__main__":
    tree = SkillTree()
    tree.run()
