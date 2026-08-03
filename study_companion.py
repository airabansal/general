import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import wikipediaapi

# --- BOT SETUP ---
TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"  # Replace with your actual bot token

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# In-memory storage for to-do lists (User ID -> List of tasks)
user_todos = {}

# Initialize Wikipedia API with a custom user-agent (Required by Wikipedia policy)
wiki = wikipediaapi.Wikipedia(
    user_agent="StudyAssistantBot/1.0 (contact@example.com)",
    language="en"
)


@bot.event
async def on_ready():
    # Sync slash commands with Discord globally
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


# --- FEATURE 1: WIKIPEDIA SUMMARY LOOKUP ---
@bot.tree.command(name="wiki", description="Fetch a quick summary from Wikipedia.")
@app_commands.describe(query="The topic or term you want to look up")
async def wiki_summary(interaction: discord.Interaction, query: str):
    await interaction.response.defer()  # Acknowledge command to prevent timeout

    page = wiki.page(query)
    if page.exists():
        summary = page.summary[:1000]  # Limit length for Discord embed limit
        embed = discord.Embed(
            title=f"📚 Wikipedia: {page.title}",
            description=f"{summary}...\n\n[Read more on Wikipedia]({page.fullurl})",
            color=discord.Color.blue(),
        )
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(
            f"❌ Could not find any Wikipedia page matching **{query}**."
        )


# --- FEATURE 2: STUDY TIMER & REMINDER ---
@bot.tree.command(
    name="remind",
    description="Set a study timer/reminder (in minutes).",
)
@app_commands.describe(
    minutes="Time in minutes before the reminder",
    topic="What you are studying or need a reminder for",
)
async def study_reminder(
    interaction: discord.Interaction, minutes: float, topic: str
):
    if minutes <= 0:
        await interaction.response.send_message(
            "Please enter a duration greater than 0 minutes.", ephemeral=True
        )
        return

    seconds = minutes * 60
    await interaction.response.send_message(
        f"⏱️ Study timer set for **{minutes} minute(s)** on **'{topic}'**. Happy studying!"
    )

    # Wait asynchronously without blocking other bot operations
    await asyncio.sleep(seconds)

    # Send reminder ping to the user
    await interaction.channel.send(
        f"🔔 {interaction.user.mention} **Time's up!** Reminder for your study session: **{topic}**"
    )


# --- FEATURE 3: TO-DO LIST MANAGEMENT ---
@bot.tree.command(name="todo_add", description="Add an item to your to-do list.")
@app_commands.describe(task="The task you want to add")
async def todo_add(interaction: discord.Interaction, task: str):
    user_id = interaction.user.id
    if user_id not in user_todos:
        user_todos[user_id] = []

    user_todos[user_id].append(task)
    await interaction.response.send_message(
        f"✅ Added to your to-do list: **{task}**", ephemeral=True
    )


@bot.tree.command(name="todo_list", description="View your current to-do list.")
async def todo_list(interaction: discord.Interaction):
    user_id = interaction.user.id
    tasks = user_todos.get(user_id, [])

    if not tasks:
        await interaction.response.send_message(
            "📋 Your to-do list is empty!", ephemeral=True
        )
        return

    formatted_list = "\n".join(
        [f"**{idx + 1}.** {task}" for idx, task in enumerate(tasks)]
    )
    embed = discord.Embed(
        title=f"📋 {interaction.user.display_name}'s To-Do List",
        description=formatted_list,
        color=discord.Color.green(),
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(
    name="todo_clear", description="Clear all items from your to-do list."
)
async def todo_clear(interaction: discord.Interaction):
    user_id = interaction.user.id
    user_todos[user_id] = []
    await interaction.response.send_message(
        "🗑️ Your to-do list has been cleared.", ephemeral=True
    )


# --- START BOT ---
if __name__ == "__main__":
    bot.run(TOKEN)
