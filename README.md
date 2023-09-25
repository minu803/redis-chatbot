# Simple Chatbot using Redis Pub/Sub

## I. Purpose
This project is aimed at building a basic chatbot using Redis's Pub/Sub mechanism. It serves as a practical learning exercise for understanding real-time messaging, integration of Redis with Python, and interaction with Docker containers.

## II. Tasks
### Step 1. Setting up two Docker containers using docker-compose 

First, navigate to the project folder path in the terminal. Then, run the following command to set up the Docker containers:

```
docker-compose up
```
![step1](https://github.com/minu803/redis-chatbot/assets/111295624/566597b0-6a6f-4826-8a1f-7a5847c8439d)


### Step 2. Chatbot Initialization

To initialize the chatbot:

1. Enter the Python Docker container:
```
docker-compose exec python-app bash
```
![python start](https://github.com/minu803/redis-chatbot/assets/111295624/1a329078-c1ba-465e-8de1-e5e14677bdd7)

2. Run the main chabot file:

```
python mp1_template.py
```
![chatbot start](https://github.com/minu803/redis-chatbot/assets/111295624/532241eb-5f2b-48d7-81f0-9a07b499ebb2)

The bot will now be initialized with the introduction.

### Step 3. User Identification

Input your user information by typing username, age, gender, and location when prompted by the chatbot. Repeat this process to add more users. In this example, we add Jack, Emily, and Leo.

![jack code](https://github.com/minu803/redis-chatbot/assets/111295624/ce4c8237-b1b9-4e43-be83-15e580e978a3)

In the backend, each user's information is stored in Redis as a hash. The key for each user is in the format `user:{username}`, and the hash contains fields for the name, age, gender, and location. 

![jack log](https://github.com/minu803/redis-chatbot/assets/111295624/d500a890-7f5c-4d3b-bac6-6667fae062d9)

![emily](https://github.com/minu803/redis-chatbot/assets/111295624/eb800725-8288-41a0-a747-be3c820f19dd)

![leo](https://github.com/minu803/redis-chatbot/assets/111295624/bfa94672-b772-4c20-a884-968913fe8323)

We can see Emily and Leo are correctly added to the Redis server.

### Step 4. Channel

When prompted for a channel name, type the desired channel name. If the channel doesn’t exist, it will be created.

![channel join code](https://github.com/minu803/redis-chatbot/assets/111295624/ad61ff6a-8e91-4229-826a-bbd45c975f4a)

Repeat this process for Emily and Leo. Now we can see all of them joined the channel from the Redis log.

![all join channel](https://github.com/minu803/redis-chatbot/assets/111295624/aa437482-140f-4fde-90b2-bcc28790f56e)

Next, let’s send a message within the channel and read the message. Jack and Emily will send messages, and Leo will receive all the messages.
- Jack sends: "Hey everyone! Did you catch the game last night? The home team played amazingly."

![jack send message](https://github.com/minu803/redis-chatbot/assets/111295624/f8aa9aeb-176e-4f28-ab3d-2aaab3b10be5)

- Emily sends: "Yeah, it was a thrilling match! That last-minute goal was epic."

![emily send message](https://github.com/minu803/redis-chatbot/assets/111295624/6b813537-0b8a-4120-a935-75d03ed2e331)

- Leo receives both messages from Jack and Emily.

![leo receive message](https://github.com/minu803/redis-chatbot/assets/111295624/a6484274-bf8f-40ea-8237-ba0358f89f76)

In the backend, when a message is sent to a channel, it is published to that channel in Redis. Subscribers to the channel, in this case, Leo, will receive messages published to that channel. You can view this in the Redis log, which shows the `publish` command being used to send messages to the channel.

![conversation log](https://github.com/minu803/redis-chatbot/assets/111295624/a5356be7-4110-4106-b697-11ef3372e71d)

To leave a channel, type 2 and the name of the channel when prompted. In this example, Jack leaves the channel.

![jack leaves channel](https://github.com/minu803/redis-chatbot/assets/111295624/eef1177a-a22f-4e83-b707-93a9f1c5a6b1)

In the backend, when a user leaves a channel, the user is unsubscribed from the channel in Redis. The `unsubscribe` command is used to remove the user from the channel's subscribers list. This means the user will no longer receive messages published to that channel. 

![jack leave log](https://github.com/minu803/redis-chatbot/assets/111295624/672b9fac-9462-4446-968b-57dfc746935e)

### Step 5.Special Commands

The implemented special commands are:

- `!help`: Provides a list of available commands.
- `!weather <city>`: Provides a mock weather update for the specified city. The weather data is fetched from a preset database in the Redis environment.
- `!fact`: Provides a random fun fact. The fact is fetched from a preset list of fun facts in the Redis environment.
- `!whoami`: Provides information about the user based on their username.

Now, let's take a  tour to see the output of these commands.

#### Screenshots of Commands in Action:

1. **!help Command**
   
When this command is used, all the available commands will show up, guiding users on the possible actions they can perform with the chatbot.

![!help](https://github.com/minu803/redis-chatbot/assets/111295624/bbbccb56-7387-4edd-ad6b-3b399203f8b0)

2. **!weather Command**

Here is an example with `!weather LA`:

![!weather](https://github.com/minu803/redis-chatbot/assets/111295624/e436a3b3-fe0f-4137-8d37-5dd1f30b705a)

3. **!fact Command**

Using this command, a random fact is fetched from a preset list of fun facts stored in the Redis environment.

![!fact](https://github.com/minu803/redis-chatbot/assets/111295624/4abd7235-5cb5-48e1-be0b-23eccaf2fe5b)

4. **!whoami Command**

The chatbot retrieves and displays the user's information, including username, age, gender, and location, from the data stored in the Redis environment
![!whoami](https://github.com/minu803/redis-chatbot/assets/111295624/e8f6d9e5-72d1-4970-97f9-5404158f8210)


Let's see how these commands look in the backend:

![special command](https://github.com/minu803/redis-chatbot/assets/111295624/aaf88ff2-0532-4011-a684-fdba92320de7)

These screenshots provide a clear and visual demonstration of how each command works and what output to expect when they are used.

## III. Monitoring Redis Log

To monitor the interactions in real-time, you can use the `redis-cli monitor` command. Below are the steps to turn on the `redis-cli` and monitor the log:

1. Ensure you are in the same file path where the project was run. First, run the following command to get into the Redis container using `docker-compose`:

```bash
   docker-compose exec redis redis-cli
```

Or, you can use the docker exec command:

```bash
docker exec -it my-redis redis-cli
```
2. Next, type the following command to start monitoring the Redis log:

```bash
MONITOR
```

This will output the logs of every command processed by the Redis server in real-time, allowing you to observe the interactions and operations happening within Redis as you use the chatbot.

### IV. Use of GenAI

1. **Problem with `read_message()` Function:**
   I encountered difficulties in figuring out the `read_message()` function. While I had some understanding of the `get_message()` method from the Redis library, the printed output was often the object itself, not the actual message. I understood that the right way to access the message involved utilizing dictionary keys and values, but the exact implementation was unclear. Here, GenAI assisted in navigating this challenge, helping me access messages in the correct format.

2. **Formatting Output Messages:**
   GenAI assisted in formatting the `print()` messages upon task completion. This assistance provided a clearer, more understandable output, making it easier to visualize the actions and results of the chatbot operations.

3. **Designing the `main()` Function:**
   Furthermore, GenAI offered insights into designing the `main()` function, particularly regarding the operation of functions within a while loop. This guidance contributed to a more efficient and effective main function design.

While GenAI was utilized in these specific areas, substantial work and thought processing were also my own contributions, ensuring a balanced and informed use of generative artificial intelligence in the development of this chatbot.
