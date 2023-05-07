import click
import configparser
import os

from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain

@click.group()
def cli():
    pass

@click.command()
@click.option('--openaikey', help='Input your OpenAI API key')
def config(openaikey):

    home_directory = os.path.expanduser("~")
    api_key_directory = os.path.join(home_directory, ".gpt")
    if not os.path.exists(api_key_directory):
        os.makedirs(api_key_directory)

    config = configparser.ConfigParser()
    config.add_section('API_KEYS')
    config.set('API_KEYS', 'openai', openaikey)

    with open(f'{api_key_directory}/config.ini', 'w') as f:
        config.write(f)

    click.echo('Successfully stored OpenAI credentials in ~/.gpt')


@click.command()
@click.argument('input_prompt')
def prompt(input_prompt):

    home_directory = os.path.expanduser("~")
    api_key_directory = os.path.join(home_directory, ".gpt")
    if not os.path.exists(api_key_directory):
        click.echo('Please set up your OpenAI API key')

    config = configparser.ConfigParser()
    config.read(f'{api_key_directory}/config.ini')
    OPENAI_API_KEY = config._sections['API_KEYS']['openai']
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    template = """Question: {question}

Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm = OpenAI(temperature=0.1)
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    click.echo(llm_chain.run(input_prompt))



cli.add_command(config)
cli.add_command(prompt)


if __name__ == "__main__":
    cli()