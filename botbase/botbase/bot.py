from botcity.core import DesktopBot
# Uncomment the line below for integrations with BotMaestro
# Using the Maestro SDK
# from botcity.maestro import *


class Bot(DesktopBot):
    def action(self, execution=None):
        # Fetch the Activity ID from the task:
        # task = self.maestro.get_task(execution.task_id)
        # activity_id = task.activity_id

        # Opens the BotCity website.
        self.browse("https://www.google.com/")
        #para programas
        # self.execute(r'caminho do programa')

        if not self.find( "pesquisar", matching=0.97, waiting_time=10000):
            self.not_found("pesquisar")
        self.click()
        self.paste("cotaçao bitcoin")
        self.key_enter(0)
        
        if not self.find_text("resumo_mercado", matching=0.97, waiting_time=10000):
            self.not_found("resumo_mercado")



        # Uncomment to mark this task as finished on BotMaestro
        # self.maestro.finish_task(
        #     task_id=execution.task_id,
        #     status=AutomationTaskFinishStatus.SUCCESS,
        #     message="Task Finished OK."
        # )

    def not_found(self, label):
        print(f"Element not found: {label}")


if __name__ == '__main__':
    Bot.main()









