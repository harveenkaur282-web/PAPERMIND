import gradio as gr
def handle_query(query : str) -> str:
    #this is a temporary placeholder function and later this will send the query to the fastapi backend.
    
    return ("Hello! \n\n"
            "I'm PaperMind \n"
            "The RAG pipeline is still under construction. \n\n"
            f"You asked:\n{query}"
        )
with gr.Blocks(title = "PaperMind") as demo:
    gr.Markdown(
        "Your Research Assistant"
    )
    question = gr.Textbox(
        label = "Ask a question",
        placeholder = "What is Retrieval-Augmented Generation"
    )
    ask_button = gr.Button("Ask")
    answer = gr.Textbox(
        label="Response",
        lines=8
    )

    ask_button.click(
        fn=handle_query,
        inputs=question,
        outputs=answer,
    )
if __name__ == "__main__":
    demo.launch()