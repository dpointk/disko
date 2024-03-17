from src.disko.sqlite import SQLiteCRUD

# Creating a connection to the database
db = SQLiteCRUD('image_data.db')

# Checking if the image is from Dockerhub
def is_from_dockerhub(image):
    parts = image.split('/')
    if len(parts) == 1:
        return True
    if '.' not in parts[0] and ':' not in parts[0]:
        return True
    if 'docker.io' in parts[0]:
        return True
    return False

# Getting the registry of the image
def calculate_ammount_per_registry(images):
    ammount = {}
    for image_tuple in images:
        image = image_tuple[0]
        parts = image.split('/')
        registry = parts[0]
        if is_from_dockerhub(image):
            if 'Dockerhub' in ammount:
                ammount['Dockerhub'] += 1
            else:
                ammount['Dockerhub'] = 1
        elif registry in ammount:
            ammount[registry] += 1
        else:
            ammount[registry] = 1
    return ammount

# Inserting the registries with the ammount of images
def insert_images_with_ammount():
    ammount = calculate_ammount_per_registry(db.select_column('images', 'image_name'))
    for registry, ammount in ammount.items():
        precentage = (ammount / len(db.select_column('images', 'image_name'))) * 100
        db.insert_data('registries', (registry, ammount, f'{precentage:.0f}%'))

def main():
    # Creating the table for the registries
    insert_images_with_ammount()
    print("Registries are successfully saved in the database.")

if __name__ == '__main__':
    main()


            