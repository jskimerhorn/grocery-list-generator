def generate_grocery_list(self):
        grocery_list = {}
        for day, items in self.groceries.items():
            if day in ["Pantry", "General"]:
                continue
            for item in items:
                if item == "\n":
                    # ignore newline characters
                    continue
                if item in grocery_list:
                    grocery_list[item] += 1
                else:
                    grocery_list[item] = 1

        pantry_list = self.groceries.get("Pantry", [])
        for item in pantry_list:
            if item in grocery_list:
                grocery_list[item] -= 1
                if grocery_list[item] == 0:
                    grocery_list.pop(item)

        grocery_result = []
        for item, count in grocery_list.items():
            if count > 0:
                if count > 1:
                    grocery_result.append(f"{item} ({count}x)")
                else:
                    grocery_result.append(item)

        general_list = self.groceries.get("General", [])
        general_count = {}
        for item in general_list:
            if item in general_count:
                general_count[item] += 1
            else:
                general_count[item] = 1

        general_result = []
        for item, count in general_count.items():
            if count > 0:
                if count > 1:
                    general_result.append(f"{item} ({count}x)")
                else:
                    general_result.append(item)
                    
        return grocery_result, general_result