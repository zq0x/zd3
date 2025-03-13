from dataclasses import dataclass, fields
import gradio as gr
import time

# Define the InputComponents and InputValues classes
@dataclass
class InputComponents:
    param1: gr.Slider
    param2: gr.Number
    quantity: gr.Slider
    animal: gr.Dropdown
    countries: gr.CheckboxGroup
    place: gr.Radio
    activity_list: gr.Dropdown
    morning: gr.Checkbox
    param0: gr.Textbox
    
    def to_list(self) -> list:
        return [getattr(self, f.name) for f in fields(self)]

@dataclass
class InputValues:
    
    param1: int
    param2: int
    quantity: int
    animal: str
    countries: list
    place: str
    activity_list: list
    morning: bool
    param0: str
    
# Define the prediction function
def predict_with_my_model(*params):
    req_params = InputValues(*params)
    result = f"Processed values: {req_params.param1}, {req_params.param2}, {req_params.quantity}, {req_params.animal}, {req_params.countries}, {req_params.place}, {req_params.activity_list}, {req_params.morning}, {req_params.param0}, {req_params.param0}, {req_params.param0}, {req_params.param0}"
    return result

def slowly_reverse(word, progress=gr.Progress()):
    progress(0, desc="Starting")
    time.sleep(10)
    progress(0.05, desc="Initializing...")

    new_string = ""
    total_letters = len(word)
    for i, letter in enumerate(word):
        time.sleep(5.25)
        new_string = letter + new_string
        progress_percent = (i + 1) / total_letters
        progress(progress_percent, desc=f"Reversing... ({int(progress_percent * 100)}%)")
        yield f"Progress: {int(progress_percent * 100)}%\nReversed so far: {new_string}"

    yield f"Progress: 100%\nReversed word: {new_string}"

def create_app():
    with gr.Blocks() as app:
        gr.Markdown(
            """
            # Welcomaae!
            Select a Hugging Face model and deploy it on a port
            
            **Note**: _[vLLM supported models list](https://docs.vllm.ai/en/latest/models/supported_models.html)_        
            """)

        inp = gr.Textbox(placeholder="Type in a Hugging Face model or tag", show_label=False, autofocus=True)
        
        def toggle_components(vllm_list):
            create_selected = "Create New" in vllm_list
            if create_selected:
                return (
                    gr.Textbox(visible=True),
                    gr.Button(visible=True)
                )
            else:
                return (
                    gr.Textbox(visible=False),
                    gr.Button(visible=False)
                )
        vllms=gr.Radio(["vLLM1", "vLLM2", "Create New"], label="vLLMs", info="Where to deploy?")

        
        textbox = gr.Textbox(
            label="Additional Information for Japan",
            visible=False,
            placeholder="Enter additional information about Japan..."
        )

        
        with gr.Accordion("Slowly Reverse a Word", open=False):
            reverse_input = gr.Textbox(label="Enter a word to reverse", placeholder="Type here...")
            reverse_output = gr.Textbox(label="Progress and Reversed Word")
            reverse_btn = gr.Button("Reverse Slowly")
            reverse_btn.click(
                fn=slowly_reverse,
                inputs=reverse_input,
                outputs=reverse_output
        )

        with gr.Row(visible=False) as vllm_engine_arguments_row:
            with gr.Column(scale=4):
                with gr.Accordion(("Advanced Parameters"), open=True):
                    input_components = InputComponents(
                        param0=gr.Textbox(placeholder="pasdsssda", value="genau", label="Textbox", info="yes a textbox"),
                        param1=gr.Slider(2, 20, value=1, label="Count", info="Choose between 2 and 20"),
                        param2=gr.Number(label="Number Input", value="2", info="Enter a number"),
                        quantity=gr.Slider(2, 20, value=4, label="Count", info="Choose between 2 and 20"),
                        animal=gr.Dropdown(["cat", "dog", "bird"], label="Animal", info="Will add more animals later!"),
                        countries=gr.CheckboxGroup(["USA", "Japan", "Pakistan"], label="Countries", info="Where are they from?"),
                        place=gr.Radio(["park", "zoo", "road"], label="Location", info="Where did they go?"),
                        activity_list=gr.Dropdown(["ran", "swam", "ate", "slept"], value=["swam", "slept"], multiselect=True, label="Activity", info="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed auctor, nisl eget ultricies aliquam, nunc nisl aliquet nunc, eget aliquam nisl nunc vel nisl."),
                        morning=gr.Checkbox(label="Morning", value=True, info="Did they do it in the morning?")
                    )
            with gr.Column(scale=1, visible=False) as vllm_engine_arguments_btn:
                vllm_engine_arguments_show = gr.Button("GENERATE NEW VLLM", variant="primary")
                vllm_engine_arguments_close = gr.Button("CANCEL")


        vllm_engine_arguments_show.click(
            lambda: [gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)], 
            None, 
            [vllm_engine_arguments_show, vllm_engine_arguments_close, vllm_engine_arguments_row]
        )
        
        vllm_engine_arguments_close.click(
            lambda: [gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)], 
            None, 
            [vllm_engine_arguments_show, vllm_engine_arguments_close, vllm_engine_arguments_row]
        )

            


        btn = gr.Button("Searcah")
        output = gr.Textbox(label="Output")


        btn.click(
            predict_with_my_model,
            input_components.to_list(),
            [output]
        )







        vllms.change(
            toggle_components,
            vllms,
            [vllm_engine_arguments_row, vllm_engine_arguments_btn]
        )





    return app

# Launch the app
if __name__ == "__main__":
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860)
    
    # app.launch(server_name=f'{os.getenv("FRONTEND_IP")}', server_port=int(os.getenv("FRONTEND_PORT")))

