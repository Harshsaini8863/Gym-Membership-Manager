import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
dataBase = client["Code_to_shape_up"]
collection = dataBase["Clients"]

count = 0


# Functions
def show_Clients():
    print(
        "{:<20}{:<20}{:<20}{:<20}{:<20}{:<20}".format("Id", "Name", "Height", "Weight", "Age", "Calories_to_be_taken"))
    print("-" * 150)
    document = collection.find()
    for doc in document:
        _id = doc["_id"]
        name = doc["name"]
        height = doc["height"]
        weight = doc["weight"]
        age = doc["age"]
        calorie = doc["calorie"]

        print(f"{_id:<20}{name:<20}{height:<20}{weight:<20}{age:<20}{calorie:<20}")


def calorie_count(gender, height, weight, age, goal, days, w):
    bmr = 0
    if gender.lower() == "m":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == "f":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    if goal == "wg":
        calorie = ((w * 7700) / days) + (bmr * 1.5)
    else:
        calorie = (bmr * 1.5) - ((w * 7700) / days)

    if calorie > 8000:
        raise ValueError("Your goal is unrealistic")
    if calorie < 100:
        raise ValueError("Your goal is unrealistic")
    return calorie


def addClients():
    global count
    # Retrieve the count of existing clients from the database
    count = collection.count_documents({})
    while True:
        print("-" * 150)
        name = input("Enter Your Name\nEnter Q/q to Quit or Exit\n:")
        if name.lower() == 'q':
            break
        count += 1  # Increment count for the new client
        _id = f"GYM0{count}"  # Generate the new user ID
        height = float(input("Enter Your Height(cm): "))
        weight = float(input("Enter Your Weight(kg): "))
        age = int(input("Enter Your Age: "))
        gender = input("Gender(M/F):")
        while True:
            goal = input("Weight Gain or Weight Loss(wg/wl): ")
            if goal.lower() == "wg" or goal.lower() == "wl":
                days = int(input("In how many days you want to complete your goal: "))
                w = float(input(f"How much weight you want to {'gain' if goal == 'wg' else 'lose'}: "))
                break
            else:
                print("Choose wg or wl")
        try:
            calorie = calorie_count(gender, height, weight, age, goal, days, w)
        except ValueError as e:
            print(e)
            print("Please enter your details again.")
            continue

        # Construct the item document
        client_details = {
            "_id": _id,
            "name": name,
            "height": height,
            "weight": weight,
            "age": age,
            "calorie": calorie
        }

        # Insert the item into the collection
        collection.insert_one(client_details)
        print("Client Details Added Successfully..")
        print("-" * 150)


def delete():
    while True:
        _id = input("Enter Client's Id or q/Q to exit")
        if _id.lower() == 'q':
            break
        collection.delete_one({"_id": _id})


def update_client():
    while True:
        _id = input("Enter Client's Id or q/Q to exit")
        if _id.lower() == 'q':
            break
        height = float(input("Enter Your Height(cm): "))
        weight = float(input("Enter Your Weight(kg): "))
        age = int(input("Enter Your Age: "))
        gender = input("Gender(M/F):")
        while True:
            goal = input("Weight Gain or Weight Loss(wg/wl): ")
            if goal.lower() == "wg" or goal.lower() == "wl":
                days = int(input("In how many days you want to complete your goal: "))
                w = float(input(f"How much weight : "))
                break
            else:
                print("Choose wg or wl")
        calorie = calorie_count(gender, height, weight, age, goal, days, w)

        # Update operation
        update_client_details = {
            "height": height,
            "weight": weight,
            "age": age,
            "calorie": calorie
        }

        # Update the item in the collection
        collection.update_one({"_id": _id}, {"$set": update_client_details})
        print("Client Details Updated Successfully..")
        print("-" * 150)


def count_clients():
    total_client = [
        {"$group": {"_id": None, "total_clients": {"$sum": 1}}}
    ]

    result = collection.aggregate(total_client)

    for doc in result:
        print("Total Number of Clients:", doc["total_clients"])


while True:
    print("-" * 150)
    print("Code_to_shape-up")
    print("-" * 150)
    print("Enter 1 --> Show Clients")
    print("Enter 2 --> New Client")
    print("Enter 3 --> Change Goal")
    print("Enter 4 --> Delete Membership")
    print("Enter 5 --> Count Total Clients")
    print("Enter 6 --> Quit")
    print("-" * 150)
    choice = int(input("Enter Your Choice: "))
    if choice == 1:
        show_Clients()
    elif choice == 2:
        addClients()
    elif choice == 3:
        update_client()
    elif choice == 4:
        delete()
    elif choice == 5:
        count_clients()
    elif choice == 6:
        break
    else:
        print("Invalid Input")

client.close()
