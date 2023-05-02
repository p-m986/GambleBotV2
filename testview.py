import discord.ui


class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # self.selected_option = None

        # Create dropdown with options
        # options = [
        #     discord.SelectOption(label='Option 1', value='option1'),
        #     discord.SelectOption(label='Option 2', value='option2')
        # ]
        # self.dropdown = discord.ui.Select(options=options)
        # self.add_item(self.dropdown)

        # Create submit button
        # self.submit_button = discord.ui.Button(
        #     label='Submit', style=discord.ButtonStyle.green)
        # self.add_item(self.submit_button)

    # async def interaction_check(self, interaction: discord.Interaction) -> bool:
    #     # Only allow the original author of the message to interact with the view
    #     return interaction.user == self.message.author

    # @discord.ui.button(label='Submit', style=discord.ButtonStyle.green)
    # async def submit_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     if self.selected_option is not None:
    #         await interaction.response.send_message(f'You selected {self.selected_option}.')
    #     else:
    #         await interaction.response.send_message('Please select an option from the dropdown.')

    # @discord.ui.select(placeholder='Select an option...', options=[
    #     discord.SelectOption(label='Option 1', value='option1'),
    #     discord.SelectOption(label='Option 2', value='option2')
    # ])
    # async def dropdown_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
    #     self.selected_option = select.values[0]
    #     await interaction.response.defer_update()
