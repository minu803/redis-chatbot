# Import necessary libraries
import redis
import json
import random
import time

# Define the Chatbor class
class Chatbot:
    # Initializing the Chatbot with default host as 'redis' and port as 6379
    def __init__(self, host='redis', port=6379):
        self.client = redis.StrictRedis(host=host, port=port)
        self.pubsub = self.client.pubsub()
        self.username = None

    # A method to introduce the bot and its commands
    def introduce(self):
        # Provide an introduction and list of commands
        intro = """
        Here are the commands this bot supports:
        !help: List of commands
        !weather <city>: Weather update
        !fact: Random fun fact
        !whoami: Your user information
        and anything else you enabled your bot to do
        """
        print(intro)

    # A method to store user details in Redis
    def identify(self, username, age, gender, location):
        # Constructing the user key and storing user details as a hash in Redis
        user_key = f"user:{username}"
        self.client.hset(user_key, mapping= {
            "name": username,
            "age": age,
            "gender": gender,
            "location":location
        })
        self.username = username

    # A method to allow the bot to join a channel
    def join_channel(self, channel):
        # Joining a channel by adding the channel to the set associated with the user 
        channel_key = f"channel:{self.username}"
        self.client.sadd(channel_key, channel)
        # Subscribe to the channel
        self.pubsub.subscribe(channel)    

    # A method to allow the bot to leave a channel
    def leave_channel(self, channel):
        # Leaving a channel by removing the channel from the set associated with the user
        channel_key = f"channel:{self.username}"
        self.client.srem(channel_key, channel)
        # Unsubscribe from the channel
        self.pubsub.unsubscribe(channel)

    # A method to send a message to a channel
    def send_message(self, channel, message):
        # Publishing the message to the specified channel
        self.client.publish(channel,message)
        self.client.rpush(f"channel_history:{channel}", json.dumps(message))
                          
    # A method to send a private message to a user
    def send_private_message(self, to_user, message):
        # Publishing the message to the specified user
        message_obj = {
            "from": self.username,
            "message": message
        }
        self.client.publish(to_user, json.dumps(message_obj))  
    
    # A method to get user information from Redis
    def get_user_info(self, username):
        # Fetching all fields and values of the hash stored at the specified user key
        user_key = f"user:{username}"
        return self.client.hgetall(user_key)       

    # A method to read the history of a channel
    def read_channel_history(self, channel):
        # Get all messages from the channel's list
        messages = self.client.lrange(f"channel_history:{channel}", 0, -1)
        return [json.loads(message) for message in messages]
    
    # A method to read a message from a channel
    def read_message(self, channel):
        # Read messages from a channel
        message = self.pubsub.get_message()
        print(message)
        if message:
            # Handle the message
            msg_type = message['type']
            if msg_type == 'message':
                channel = message['channel']
                data = message['data']
                print(f"Received the following message from {channel}: {data}") 

    # A method to store mock data in Redis
    def store_mock_data(self):

        # Storing mock weather data in Redis
        # Define a list of cities and weather conditions
        cities = ["NYC", "LA", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", 
                "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", 
                "Columbus", "San Francisco", "Charlotte", "Indianapolis"]
        conditions = ["Sunny", "Rainy", "Cloudy", "Windy", "Snowy", "Hazy", "Clear", "Humid"]
        
        weather_data = {}

        # Generate random weather data for each city
        for city in cities:
            temperature = random.randint(30, 95)  # Random temperature between 30F and 95F
            condition = random.choice(conditions)
            weather_data[city] = f"{condition} and {temperature}F"

        # Store the weather data in Redis
        for city, weather in weather_data.items():
            self.client.set(f"weather:{city}", weather)

        # Storing fun facts
        fun_facts = [
            "Did you know? Cats have five toes on their front paws, but only four on the back!",
            "Honeybees can recognize human faces.",
            "Did you know? Octopuses have three hearts and blue blood!",
            "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
            "A day on Venus is longer than a year on Venus. It takes about 243 Earth days for Venus to complete one rotation on its axis, but only about 225 Earth days to complete one orbit around the Sun.",
            "Bananas are berries, but strawberries aren’t! In botanical terms, a berry is a fruit produced from the ovary of a single flower with seeds embedded in the flesh. Under this definition, bananas qualify as berries, but strawberries do not because they arise from a flower with multiple ovaries.",
            "The Eiffel Tower can be 15 cm taller during the summer. Due to the iron expanding, the tower can grow by 6 inches."
        ]
        # Clear the previous list (if any) and then insert the new facts
        self.client.delete("funfacts")
        self.client.lpush("funfacts", *fun_facts)
            
    # A method to process specialized commands sent to the bot
    def process_commands(self, message):
        # Handle special chatbot commands: !help
        if message == "!help":
            return self.introduce()
        
        # Handle special chatbot commands: !weather
        elif message.startswith("!weather"):
            # Ask the user for a city
            city = input("Which city's weather would you like to know? ").strip()

            # Fetch weather data from Redis that matches the city
            weather = self.client.get(f"weather:{city}")
            if weather:
                return f"It's {weather.decode()} in {city}!"
            else:
                return f"No weather data available for {city}."
        
        # Handle special chatbot commands: !fact    
        elif message == "!fact":
            # Fetch a random fun fact from Redis
            fact = self.client.lpop("funfacts")
            # Rotate the list
            self.client.rpush("funfacts", fact)  
            return fact.decode()
        
        # Handle special chatbot commands: !whoami
        elif message == "!whoami":
            # Fetch user data from Redis
            if not self.username:
                return "You need to identify first!"
            user_data = self.get_user_info(self.username)
            # If the user exists, return their information
            if user_data:
                return f"Name: {user_data[b'name'].decode()}, Age: {user_data[b'age'].decode()}, Gender: {user_data[b'gender'].decode()}, Location: {user_data[b'location'].decode()}" 
            else:
                return "Unknown command!"        

    # def direct_message(self, message):
    #     # Send a direct message to the chatbot
    #     return self.process_commands(message)

# Defining the main function to run the chatbot    
def main():
    # Step 1: Initialize the Chatbot and introduce its commands
    bot = Chatbot()
    bot.introduce()

    # Step 2: Prompt user for identification details and store them
    username = input("Enter your username: ")
    age = input("Enter your age: ")
    gender = input("Enter your gender: ")
    location = input("Enter your location: ")
    
    bot.identify(username, age, gender, location)
    print(f"Identified as {username}!")
    
    # Step 3: Storing mock data for weather and fun facts
    bot.store_mock_data()
    while True:
        print("\nOptions:")
        print("1. Join a channel")
        print("2. Leave a channel")
        print("3. Send a message to a channel")
        print("4. Read a message from a channel")
        print("5. Add a private message to a user")
        print("6. Get info about a user")
        print("7. Exit")

        # Step 4: Taking user choice for further actions
        choice = input("Enter your choice: ")

        # Step 5: Performing actions based on user choice
        if choice == "1":
                channel = input("Enter channel name to join: ")
                bot.join_channel(channel)  # Joining a channel
                print(f"Joined {channel}!")
                
        elif choice == "2":
            channel = input("Enter channel name to leave: ")
            bot.leave_channel(channel) # Leaving a channel
            print(f"Left {channel}!")
            
        elif choice == "3":
            channel = input("Enter channel name: ")
            message = input("Enter your message: ")
            bot.send_message(channel, message) # Sending message to a channel
            print("Message sent!")
        
        elif choice == "4":
            channel = input("Enter channel name to read from: ")
            message = bot.read_message(channel) # Reading message from a channel
            if message:
                print(message)
            else:
                print("No new messages.")
            
        elif choice == "5":
            message = input("Enter your private message to the bot: ")
            response = bot.direct_message(message) # Sending direct message to the bot
            print(response)
            
        elif choice == "6":
            response = bot.process_commands("!whoami") # Getting info about the user
            print(response)

        # Step 6: Exiting the program    
        elif choice == "7":
            print("Goodbye!")
            break
        
        # Handling invalid choices
        else:
            response = bot.process_commands(choice)
            print(response or "Unknown command!")         

import time
if __name__ == "__main__":
    main()
