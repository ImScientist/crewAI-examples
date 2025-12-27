#!/usr/bin/env python
import yaml
from pydantic import BaseModel, Field
from crewai.flow import Flow, listen, start
from ai_game_builder.crews.builder_crew.builder_crew import BuilderCrew


class GameState(BaseModel):
    game_instructions: str = ""  # Field(description="Game instructions")
    game_code: str = ""  # Field(description="Game code written in python")
    # game_code_final: str = Field(description="Corrected game code written in python")


class GameGenerationFlow(Flow[GameState]):
    """ .. """

    with open('src/ai_game_builder/gamedesign.yaml', 'r', encoding='utf-8') as file:
        game_descriptions = yaml.safe_load(file)
    print(f'Possible game titles: {list(game_descriptions.keys())}')

    @start()
    def get_user_input(self):
        """Get input from the user about the game"""

        print("\n=== Create Your First Game ===\n")

        game_title = input("What game would you like to create?")

        self.state.game_instructions = self.game_descriptions[game_title]

        print(f"\nCreating the game {game_title} ...\n")

        return self.state

    @listen(get_user_input)
    def write_initial_code(self):
        print("Write initial code")

        result = (
            BuilderCrew()
            .crew()
            .kickoff(inputs={"game_instructions": self.state.game_instructions})
        )

        # Store the content
        self.state.game_code = result.raw

    # @listen(generate_poem)
    # def save_poem(self):
    #     print("Saving poem")
    #     with open("poem.txt", "w") as f:
    #         f.write(self.state.poem)


def kickoff():
    """ Run the game generator flow """
    GameGenerationFlow().kickoff()
    print("\n=== Flow Complete ===")


if __name__ == "__main__":
    kickoff()
