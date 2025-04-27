import time
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import AddChatUserRequest  # تم التعديل هنا لاستيراد AddChatUserRequest

def print_menu():
    print("\nPlease choose an option:")
    print("1. Enter API ID")
    print("2. Enter API Hash")
    print("3. Enter Source Group Link")
    print("4. Enter Your Group Link")
    print("5. Exit")

# تعريف المتغيرات للـ API و الـ Links
api_id = None
api_hash = None
phone_number = None
source_group_link = None
my_group_link = None

# وظيفة لتسجيل الدخول وبدء نقل الأعضاء
async def start_process(client):
    try:
        # التأكد من وجود المدخلات
        if not api_id or not api_hash or not phone_number or not source_group_link or not my_group_link:
            print("Error: All fields are required!")
            return
        
        await client.start(phone_number)

        # الحصول على الجروبات
        source_group = await client.get_entity(source_group_link)
        my_group = await client.get_entity(my_group_link)

        participants = await client.get_participants(source_group)

        for participant in participants:
            try:
                # دعوة العضو إلى الجروب باستخدام AddChatUserRequest
                await client(AddChatUserRequest(my_group, participant.id))
                print(f"Successfully added {participant.username or participant.id}")
                time.sleep(2)  # تأخير لتجنب الحظر
            except Exception as e:
                print(f"Failed to add {participant.username or participant.id}: {e}")
                time.sleep(2)  # تأخير لتجنب الحظر

        print("Process completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# تسجيل الدخول وبدء السكربت
def login_and_run():
    global api_id, api_hash, phone_number, source_group_link, my_group_link

    # إدخال الـ API ID و الـ API Hash و رقم الهاتف
    phone_number = input("Enter your phone number: ")
    
    client = TelegramClient('session_name', api_id, api_hash)

    async def main():
        await start_process(client)

    # تشغيل السكربت
    with client:
        client.loop.run_until_complete(main())

# واجهة النصوص
while True:
    print_menu()
    
    choice = input("Select an option (1-5): ").strip()

    if choice == "1":
        api_id = input("Enter your API ID: ").strip()
    elif choice == "2":
        api_hash = input("Enter your API Hash: ").strip()
    elif choice == "3":
        source_group_link = input("Enter the link of the source group: ").strip()
    elif choice == "4":
        my_group_link = input("Enter the link of your group: ").strip()
    elif choice == "5":
        print("Exiting the tool...")
        break
    else:
        print("Invalid option, please try again.")

    # عندما يتم إدخال كل شيء، نبدأ العملية
    if api_id and api_hash and source_group_link and my_group_link:
        start_process_input = input("Do you want to start the process? (y/n): ").strip()
        if start_process_input.lower() == 'y':
            login_and_run()
            break
