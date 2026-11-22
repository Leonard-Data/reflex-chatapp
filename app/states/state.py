import reflex as rx
import asyncio

class State(rx.State):
    # the current action being ask
    question: str= ""

    #keep track of the question and answer pairs
    chat_history: list[tuple[str, str]] = []

    @rx.event
    def set_question(self, question: str):
        self.question = question

    @rx.event
    async def answer(self):
        # add the question and answer pair to the chat history
        answer="I dont know the answer to that question."
        self.chat_history.append((self.question, answer))
        print(f"Question: {self.question}, Answer: {answer}")
        # clear the current question
        self.question = ""

        yield

        for i in range(len(answer)):
            await asyncio.sleep(0.05)  # adjust the speed of typing here
            # simulate typing by adding one character at a time
            self.chat_history[-1] = (self.chat_history[-1][0], answer[:i+1])
            yield